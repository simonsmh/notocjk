import logging
import shutil
from os import PathLike
from pathlib import Path

import chws_tool
import httpx
from fontTools import ttLib
from nototools import font_data, tool_utils
from tqdm import tqdm

## BEGIN: https://android.googlesource.com/platform/external/noto-fonts.git/+/refs/heads/android15-release/scripts/subset_noto_cjk.py
# Characters supported in Noto CJK fonts that UTR #51 recommends default to
# emoji-style.
EMOJI_IN_CJK = {
    0x26BD,  # ⚽ SOCCER BALL
    0x26BE,  # ⚾ BASEBALL
    0x1F18E,  # 🆎 NEGATIVE SQUARED AB
    0x1F191,  # 🆑 SQUARED CL
    0x1F192,  # 🆒 SQUARED COOL
    0x1F193,  # 🆓 SQUARED FREE
    0x1F194,  # 🆔 SQUARED ID
    0x1F195,  # 🆕 SQUARED NEW
    0x1F196,  # 🆖 SQUARED NG
    0x1F197,  # 🆗 SQUARED OK
    0x1F198,  # 🆘 SQUARED SOS
    0x1F199,  # 🆙 SQUARED UP WITH EXCLAMATION MARK
    0x1F19A,  # 🆚 SQUARED VS
    0x1F201,  # 🈁 SQUARED KATAKANA KOKO
    0x1F21A,  # 🈚 SQUARED CJK UNIFIED IDEOGRAPH-7121
    0x1F22F,  # 🈯 SQUARED CJK UNIFIED IDEOGRAPH-6307
    0x1F232,  # 🈲 SQUARED CJK UNIFIED IDEOGRAPH-7981
    0x1F233,  # 🈳 SQUARED CJK UNIFIED IDEOGRAPH-7A7A
    0x1F234,  # 🈴 SQUARED CJK UNIFIED IDEOGRAPH-5408
    0x1F235,  # 🈵 SQUARED CJK UNIFIED IDEOGRAPH-6E80
    0x1F236,  # 🈶 SQUARED CJK UNIFIED IDEOGRAPH-6709
    0x1F238,  # 🈸 SQUARED CJK UNIFIED IDEOGRAPH-7533
    0x1F239,  # 🈹 SQUARED CJK UNIFIED IDEOGRAPH-5272
    0x1F23A,  # 🈺 SQUARED CJK UNIFIED IDEOGRAPH-55B6
    0x1F250,  # 🉐 CIRCLED IDEOGRAPH ADVANTAGE
    0x1F251,  # 🉑 CIRCLED IDEOGRAPH ACCEPT
}
# Characters we have decided we are doing as emoji-style in Android,
# despite UTR #51's recommendation
ANDROID_EMOJI = {
    0x2600,  # ☀ BLACK SUN WITH RAYS
    0x2601,  # ☁ CLOUD
    0x260E,  # ☎ BLACK TELEPHONE
    0x261D,  # ☝ WHITE UP POINTING INDEX
    0x263A,  # ☺ WHITE SMILING FACE
    0x2660,  # ♠ BLACK SPADE SUIT
    0x2663,  # ♣ BLACK CLUB SUIT
    0x2665,  # ♥ BLACK HEART SUIT
    0x2666,  # ♦ BLACK DIAMOND SUIT
    0x270C,  # ✌ VICTORY HAND
    0x2744,  # ❄ SNOWFLAKE
    0x2764,  # ❤ HEAVY BLACK HEART
}
# We don't want support for ASCII control chars.
CONTROL_CHARS = set(tool_utils.parse_int_ranges("0000-001F"))
EXCLUDED_CODEPOINTS = frozenset(sorted(EMOJI_IN_CJK | ANDROID_EMOJI | CONTROL_CHARS))


def remove_codepoints_from_ttc(ttc_path, out_dir):
    """Removes a set of characters from a TTC font file's cmap table."""
    logging.info("Loading %s", ttc_path)
    ttc = ttLib.TTCollection(ttc_path)
    logging.info("Subsetting %d fonts in the collection", len(ttc))
    for font in ttc:
        font_data.delete_from_cmap(font, EXCLUDED_CODEPOINTS)
    out_path = out_dir / ttc_path.name
    logging.info("Saving to %s", out_path)
    ttc.save(out_path)
    logging.info(
        "Size: %d --> %d, delta=%d",
        ttc_path.stat().st_size,
        out_path.stat().st_size,
        out_path.stat().st_size - ttc_path.stat().st_size,
    )


## END: https://android.googlesource.com/platform/external/noto-fonts.git/+/refs/heads/android15-release/scripts/subset_noto_cjk.py


def download_file(
    url: str, save_path_file_name: str | bytes | PathLike[str] | PathLike[bytes]
) -> bool:
    with open(save_path_file_name, "wb") as f:
        with httpx.stream("GET", url, follow_redirects=True) as response:
            if response.status_code != 200:
                logging.error(f"Failed to download {url}")
                return False
            with tqdm(
                total=int(response.headers.get("content-length", 0)),
                unit="B",
                unit_divisor=1024,
                unit_scale=True,
            ) as progress:
                num_bytes_downloaded = response.num_bytes_downloaded
                for chunk in response.iter_bytes():
                    f.write(chunk)
                    progress.update(
                        response.num_bytes_downloaded - num_bytes_downloaded
                    )
                    num_bytes_downloaded = response.num_bytes_downloaded
    return True


def download_and_patch_noto_cjk_font(url):
    base_file_name = url.split("/")[-1]
    ## Download
    logging.info(f"Downloading {url}...")
    input_dir = Path("temp/input")
    input_dir.mkdir(parents=True, exist_ok=True)
    input_file = input_dir / base_file_name
    if not download_file(url, input_file):
        logging.error("Failed to download")
        return

    ## CHWS Patch
    logging.info("Applying CHWS patch...")
    output_path = Path("temp/chws_output")
    output_path.mkdir(exist_ok=True)
    output_file = output_path / base_file_name
    chws_tool.add_chws(input_file, output_file)

    ## Subset
    logging.info("Subsetting...")
    result_path = Path("system/fonts")
    result_path.mkdir(parents=True, exist_ok=True)
    remove_codepoints_from_ttc(output_file, result_path)
    logging.info("Done!")
    shutil.rmtree(Path("temp"))
