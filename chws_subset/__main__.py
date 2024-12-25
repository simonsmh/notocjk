import argparse
import concurrent.futures

from . import download_file, download_and_patch_noto_cjk_font

DEFAULT_DOWNLOADING_FONTS = {
    "NotoSerifCJK-VF.otf.ttc": "https://github.com/notofonts/noto-cjk/raw/refs/heads/main/Serif/Variable/OTC/NotoSerifCJK-VF.otf.ttc",
    "NotoSansCJK-VF.otf.ttc": "https://github.com/notofonts/noto-cjk/raw/refs/heads/main/Sans/Variable/OTC/NotoSansCJK-VF.otf.ttc",
}


def main():
    parser = argparse.ArgumentParser(
        description="Download and patch Noto fonts with CHWS"
    )
    parser.add_argument("--url", help="URL to download and patch", default=None)
    args = parser.parse_args()
    if args.url:
        download_and_patch_noto_cjk_font(args.url)
    else:
        ## Download and patch all default fonts
        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(
                download_and_patch_noto_cjk_font, DEFAULT_DOWNLOADING_FONTS.values()
        )
        ## Download module_installer.sh
        download_file(
            "https://github.com/topjohnwu/Magisk/raw/master/scripts/module_installer.sh",
            "META-INF/com/google/android/update-binary",
        )


if __name__ == "__main__":
    main()
