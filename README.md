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

Upgrade Noto Serif CJK to 2.000(R) that supports variable fonts.

![Noto Serif CJK variable test](https://github.com/simonsmh/notocjk/blob/master/extra/serif-variable-test.mp4?raw=true)

* Recent fixes:

Remove cmap and add chws for Noto Serif CJK.

* Known issues:

HK fonts style is pending & waiting for Google solution in later android versions.

Font weight in Firefox is not current (all be thin) if force it to use Noto Sans CJK VF. ([#28](https://github.com/simonsmh/notocjk/issues/28))

Android 12 may crash in some app after installed version 10 and above with Magisk Hide enabled. See: (Chinese only, more details of logs in comments) https://t.me/magiskalpha/297

## Credit & Support

* Copyright (C) 2017-2021 simonsmh <simonsmh@gmail.com>
* Any issue or pull request is welcomed.
* Star this module at [GitHub](https://github.com/simonsmh/notocjk).
