# Changelog v28

* Fonts patching on the fly. See [chws_subset](../chws_subset/__init__.py)
* Removed old fonts that prevent MinikinFont from loading with an NPE when Magisk/KernelSU triggers unmounting.

> Fonts files are provided by [noto-cjk](https://github.com/googlefonts/noto-cjk) from Google.
> The fonts have been modified using [chws_subset](../chws_subset/__init__.py). For more details, please visit https://github.com/WordlessEcho/patch-noto-cjk-for-android  