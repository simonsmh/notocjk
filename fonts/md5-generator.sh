#!/sbin/sh

FONTPATH=`pwd`/fonts
FONT=NotoSansCJK.ttc

if [ -f "$FONTPATH/$FONT" ]; then
	MD5=`md5sum "$FONTPATH/$FONT" | cut -d ' ' -f1`
	if [ -f "$FONTPATH/$FONT.md5" ]; then
		OLDMD5=`cat "$FONTPATH/$FONT.md5"`
		if [ "$MD5" = "$OLDMD5" ]; then
			echo "No change of $FONT"
			exit 0
		fi
	fi

	echo "$MD5" > "$FONTPATH/$FONT.md5"
	echo >> "$FONTPATH/$FONT.md5"
	rm "$FONTPATH/$FONT.part"*
	split -b 100M "$FONTPATH/$FONT" -d -a 1 "$FONTPATH/$FONT.part" >&1

else
	echo "No $FONT, skipping"
fi
