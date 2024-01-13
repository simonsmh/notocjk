# Changelog v24

- Fixes for Magisk Canary(26404) support. Dropping copies of fonts from internal mirror mount point. [#48](https://github.com/simonsmh/notocjk/issues/48)

> The fonts have been modified by subset_noto_cjk.py to remove cmap entries for characters that should default to emoji style in Android.
> The fonts have been modified to have chws table. See https://github.com/kojiishi/east_asian_spacing for more details.
