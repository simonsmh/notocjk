# otc2otf.py v1.0 Jan 14 2014

__help__ = """
AFDKOPython otc2otf.py  [-w] <font.ttc>

example:
 AFDKOPython otc2otf.py  -w  temp.ttc

Report tags and offsets. Optionally extract all OpenType fonts from the parent OpenType Collection font.

-w  Optional. Extract and write all sfnt fonts as separate font files.
"""


import sys
import os
import struct

class OTCError(TypeError):
	pass

class FontEntry:

	def __init__(self, sfntType, searchRange, entrySelector, rangeShift):
		self.sfntType = sfntType
		self.searchRange = searchRange
		self.entrySelector = entrySelector
		self.rangeShift = rangeShift
		self.tableList = []
		self.fileName = "temp.tmp.otf"
		self.psName = "PSNameUndefined"
		
	def append(self, tableEntry):
		self.tableList.append(tableEntry)

class TableEntry:
	
	def __init__(self, tag, checkSum, length):
		self.tag = tag
		self.checksum = checkSum
		self.length = length
		self.data = None
		self.offset = None
		self.isPreferred = False

ttcHeaderFormat = ">4sLL"
ttcHeaderFormatDoc = """
		> # big endian
		TTCTag:                  4s # "ttcf"
		Version:                 L  # 0x00010000 or 0x00020000
		numFonts:                L  # number of fonts
		# OffsetTable[numFonts]: L  # array with offsets from beginning of file
		# ulDsigTag:             L  # version 2.0 only
		# ulDsigLength:          L  # version 2.0 only
		# ulDsigOffset:          L  # version 2.0 only
"""


ttcHeaderSize = struct.calcsize(ttcHeaderFormat)

offsetFormat = ">L"
offsetSize = struct.calcsize(">L")

sfntDirectoryFormat = ">4sHHHH"
sfntDirectoryFormatDoc = """
		> # big endian
		sfntVersion:    4s
		numTables:      H    # number of tables
		searchRange:    H    # (max2 <= numTables)*16
		entrySelector:  H    # log2(max2 <= numTables)
		rangeShift:     H    # numTables*16-searchRange
"""

sfntDirectorySize = struct.calcsize(sfntDirectoryFormat)

sfntDirectoryEntryFormat = ">4sLLL"
sfntDirectoryEntryFormatDoc = """
		> # big endian
		tag:            4s
		checkSum:       L
		offset:         L
		length:         L
"""

sfntDirectoryEntrySize = struct.calcsize(sfntDirectoryEntryFormat)


nameRecordFormat = ">HHHHHH"
nameRecordFormatDoc = """
		>	# big endian
		platformID:	H
		platEncID:	H
		langID:		H
		nameID:		H
		length:		H
		offset:		H
"""
nameRecordSize = struct.calcsize(nameRecordFormat)

		
def parseArgs(args):
	writeOTF = False
	fontPath = None
	argn = len(args)
	i = 0
	while i < argn:
		arg  = args[i]
		i += 1
		
		if arg[0] != '-':
			fontPath = arg
		elif arg == "-w":
			writeOTF = True
		elif (arg == "-u") or (arg == "-h"):
			print __help__
			raise OTCError()
		else:
			raise OTCError("Unknown option '%s'." % (arg))
			
	if fontPath == None:
		raise OTCError("You must specify an OpenType Collection font as the input file..")
	
	allOK = True
	if not os.path.exists(fontPath):
		raise OTCError("Cannot find '%s'." % (fontPath))
		
	fp = file(fontPath, "rb")
	data = fp.read(4)
	fp.close()
	
	if data != 'ttcf':
		raise OTCErrr("File is not an OpenType Collection file: '%s'." % (fontPath))

	return fontPath, writeOTF

def getPSName(data):
	format, n, stringOffset = struct.unpack(">HHH", data[:6])
	expectedStringOffset = 6 + n * nameRecordSize
	if stringOffset != expectedStringOffset:
		# XXX we need a warn function
		print "Warning: 'name' table stringOffset incorrect.",
		print "Expected: %s; Actual: %s" % (expectedStringOffset, stringOffset)
	stringData = data[stringOffset:]
	data = data[6:]
	psName = "PSNameUndefined"
	for i in range(n):
		if len(data) < 12:
			# compensate for buggy font
			break
		platformID, platEncID, langID, nameID, length, offset = struct.unpack(nameRecordFormat, data[:nameRecordSize])
		data = data[nameRecordSize:]
		if not ((platformID, platEncID, langID, nameID) == (1, 0, 0, 6)):
			continue
			
		psName = stringData[offset:offset+length]
		assert len(psName) == length

	return psName

def readFontFile(fontOffset, data):
	sfntType, numTables, searchRange, entrySelector, rangeShift = struct.unpack(sfntDirectoryFormat, data[fontOffset:fontOffset + sfntDirectorySize])
	fontEntry = FontEntry(sfntType, searchRange, entrySelector, rangeShift)
	entryData = data[fontOffset + sfntDirectorySize:]
	i = 0
	seenGlyf = False
	while i < numTables:
		tag, checksum, offset, length = struct.unpack(sfntDirectoryEntryFormat, entryData[:sfntDirectoryEntrySize])
		tableEntry = TableEntry(tag, checksum, length)
		tableEntry.offset = offset
		tableEntry.data = data[offset:offset+length]
		fontEntry.tableList.append(tableEntry)
		if tag == "name":
			fontEntry.psName = getPSName(tableEntry.data)
		elif tag == "glyf":
			seenGlyf = True
		entryData =  entryData[sfntDirectoryEntrySize:]
		i += 1
	if seenGlyf:
			fontEntry.fileName = fontEntry.psName + ".ttf"
	else:
			fontEntry.fileName = fontEntry.psName + ".otf"
		
	print "%s" % (fontEntry.psName)
	for tableEntry in fontEntry.tableList:
		print "\t%s checksum: 0x%08X, offset: 0x%08X, length: 0x%08X" % (tableEntry.tag, tableEntry.checksum, tableEntry.offset, tableEntry.length)
	return fontEntry


def writeOTFFont(fontEntry):

	dataList = []
	numTables = len(fontEntry.tableList)
	# Build the SFNT header
	data = struct.pack(sfntDirectoryFormat, fontEntry.sfntType, numTables, fontEntry.searchRange, fontEntry.entrySelector, fontEntry.rangeShift)
	dataList.append(data)
	
	fontOffset = sfntDirectorySize + numTables*sfntDirectoryEntrySize
	print fontOffset
	# Set the offsets in the tables.
	for tableEntry in fontEntry.tableList:
		tableEntry.offset = fontOffset
		fontOffset += tableEntry.length
	
	# build table entries in sfnt directory
	for tableEntry in fontEntry.tableList:
		tableData = struct.pack(sfntDirectoryEntryFormat, tableEntry.tag, tableEntry.checksum, tableEntry.offset, tableEntry.length)
		dataList.append(tableData)
	
	# add table data to font.
	for tableEntry in fontEntry.tableList:
		tableData = tableEntry.data
		dataList.append(tableData)
	
	fontData = "".join(dataList)
	
	fp = file(fontEntry.fileName, "wb")
	fp.write(fontData)
	fp.close()
	return

def run(args):
	fontPath, writeOTF = parseArgs(args)
	print "Input font:", fontPath
	

	fp = file(fontPath, "rb")
	data = fp.read()
	fp.close()

	TTCTag, version, numFonts = struct.unpack(ttcHeaderFormat, data[:ttcHeaderSize])
	offsetdata = data[ttcHeaderSize:]
	print "Version: %s.  numFonts: %s." % (version, numFonts)
	
	fontList = []
	i = 0
	while i < numFonts:
		offset = struct.unpack(offsetFormat, offsetdata[:offsetSize])[0]
		print "font %s offset: %s/0x%08X." % (i, offset,offset),
		fontEntry = readFontFile(offset, data)
		fontList.append(fontEntry)
		offsetdata = offsetdata[offsetSize:]
		i += 1
		
	if writeOTF:		
		for fontEntry in fontList:
			writeOTFFont(fontEntry)
	print "Done"

if __name__ == "__main__":
	try:
		run(sys.argv[1:])
	except (OTCError), e:
		print e.message
		
