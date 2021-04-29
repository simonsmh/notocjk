# NotoCJK
[![Upload zip](https://github.com/simonsmh/notocjk/workflows/Upload%20zip/badge.svg)](https://github.com/simonsmh/notocjk/actions)
[![Download](https://img.shields.io/github/downloads/simonsmh/notocjk/total.svg)](https://github.com/simonsmh/notocjk/releases)

NotoSansCJK & NotoSerifCJK full weight patch for Android devices.

* NotoSansCJK VF support as full weight patch applies to Android O+
* NotoSerifCJK full weight patch applies to Android P+

Fonts are provided by [Google](https://github.com/googlefonts/noto-cjk).

## Maintenance
Currently, this module is still maintained. It was used to be stored at official repo but got removed in repo cleanup. Now you can download it directly in this repo's [release tabs](https://github.com/simonsmh/notocjk/releases).

[John Wu's Twitter for details](https://twitter.com/topjohnwu/status/1229896206584664065)

## NOTICE

* You should use latest Magisk Manager to install this module. If you meet any problem under installation from Magisk Manager, please try to install it from recovery.

* New features:

Support [Contextual Half-width Spacing](https://docs.microsoft.com/en-us/typography/opentype/spec/features_ae#tag-chws).

[Try](https://kojiishi.github.io/chws/test.html) 

(Scrolling down to the 35. Install [Firefox](https://play.google.com/store/apps/details?id=org.mozilla.firefox) for serif testing.)

![Contextual Half-width Spacing in Sans](https://github.com/simonsmh/notocjk/blob/master/pics/Screenshot_20210415-005721_Firefox.png?raw=true)
![Contextual Half-width Spacing in Serif](https://github.com/simonsmh/notocjk/blob/master/pics/Screenshot_20210415-005701_Firefox.png?raw=true)

Before:

![No Support for Contextual Half-width Spacing in Sans](https://github.com/simonsmh/notocjk/blob/master/pics/Screenshot_20210415-010033_Firefox.png?raw=true)
![No Support for Contextual Half-width Spacing in Serif](https://github.com/simonsmh/notocjk/blob/master/pics/Screenshot_20210415-010042_Firefox.png?raw=true)

* Recent fixes:

From upstream: [Variable font version could not display some symbols · Issue #296 · adobe-fonts/source-han-sans](https://github.com/adobe-fonts/source-han-sans/issues/296) (Thanks to [@AokiFuru](https://github.com/AokiFuru) [#25](https://github.com/simonsmh/notocjk/issues/25))

Some Emoji doesn't display by Noto Color Emoji. [#21](https://github.com/simonsmh/notocjk/issues/21)

* Known issues:

HK fonts style is pending & waiting for Google solution in later android versions.

Android 12 may crash in some app after installed version 10 and above with Magisk Hide enabled. See: (Chinese only, more details of logs in comments) https://t.me/magiskalpha/297

## Credit & Support

* Copyright (C) 2017-2021 simonsmh <simonsmh@gmail.com>
* Any issue or pull request is welcomed.
* Star this module at [GitHub](https://github.com/simonsmh/notocjk).
