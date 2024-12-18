# Changelog v27

* Added an installation warning for Android 15+
* Removed an old font that prevent MinikinFont from loading with an NPE when Magisk/KernelSU triggers unmounting.

> The fonts were modified by `subset_noto_cjk.py` to remove cmap entries for characters that should default to the emoji style on Android.
> The fonts have been modified to include a `chws` table.
> See https://github.com/WordlessEcho/patch-noto-cjk-for-android for more details.
