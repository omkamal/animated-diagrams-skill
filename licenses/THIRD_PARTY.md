# Third-party components

This project's own code, themes, templates and documentation are licensed
under **Apache-2.0** ([`../LICENSE`](../LICENSE)). The components below are
bundled (or, for GSAP, fetched into the repo by `scripts/setup.sh`) and each
remains under its **own** license. None of them is copyleft over this
project's source — this is a normal mixed-license aggregate. See
[`../NOTICE`](../NOTICE) for the short-form summary.

## Fonts — `assets/fonts/*.woff2`

All bundled fonts are under the **SIL Open Font License v1.1** (full text:
[`OFL.txt`](OFL.txt)). The OFL requires that the license and copyright notice
accompany the font files (satisfied by this directory) and that the fonts are
not sold on their own. It does **not** impose any condition on documents,
videos, or images produced with the fonts, nor on this project's code.

| File | Family | Copyright | Upstream |
|---|---|---|---|
| `Inter-Variable.woff2` | Inter | © The Inter Project Authors | https://github.com/rsms/inter |
| `Archivo-Variable.woff2` | Archivo | © The Archivo Project Authors (Omnibus-Type) | https://github.com/Omnibus-Type/Archivo |
| `Nunito-Variable.woff2` | Nunito | © The Nunito Project Authors | https://github.com/googlefonts/nunito |
| `SpaceGrotesk-Variable.woff2` | Space Grotesk | © Florian Karsten | https://github.com/floriankarsten/space-grotesk |
| `Caveat-Variable.woff2` | Caveat | © The Caveat Project Authors (Pablo Impallari) | https://github.com/googlefonts/caveat |
| `Fraunces-Variable.woff2` | Fraunces | © The Fraunces Project Authors (Undercase Type) | https://github.com/undercasetype/Fraunces |
| `IBMPlexMono-Regular.woff2` | IBM Plex Mono | © IBM Corp. | https://github.com/IBM/plex |
| `JetBrainsMono-Regular.woff2` | JetBrains Mono | © JetBrains s.r.o. | https://github.com/JetBrains/JetBrainsMono |
| `Cairo-Arabic.woff2`, `Cairo-Latin.woff2` | Cairo | © The Cairo Project Authors | https://github.com/googlefonts/cairo |
| `Amiri-Arabic.woff2` | Amiri | © Khaled Hosny, The Amiri Project | https://github.com/aliftype/amiri |
| `Tajawal-Arabic.woff2`, `Tajawal-Arabic-Bold.woff2` | Tajawal | © Boutros International | https://github.com/google/fonts (ofl/tajawal) |
| `ReemKufi-Arabic.woff2` | Reem Kufi | © Khaled Hosny | https://github.com/aliftype/reem-kufi |

## Icons — `assets/icons/fa6-common.svg`

| Component | License | Attribution | Source |
|---|---|---|---|
| Font Awesome 6 Free (26-icon subset) | Icons: **CC-BY 4.0** | © Fonticons, Inc. — attribution required | https://fontawesome.com |

CC-BY 4.0 license text: https://creativecommons.org/licenses/by/4.0/legalcode

The other files in `assets/icons/` (`generic.svg`, `cloud-aws.svg`,
`cloud-gcp.svg`, `cloud-azure.svg`) are original stylized line glyphs authored
for this project and are covered by the project's Apache-2.0 license. Vendor
cloud names are trademarks of their owners and are used nominatively (to label
the corresponding services) only.

## Animation runtime — `assets/vendor/gsap/*.js`

| Component | License | Attribution | Source |
|---|---|---|---|
| GSAP + DrawSVGPlugin + MotionPathPlugin + MorphSVGPlugin | GSAP Standard "No Charge" License (free, incl. commercial use) | © GreenSock, Inc. | https://gsap.com |

License text: https://gsap.com/community/standard-license/. These files are
installed from the npm `gsap` package by `scripts/setup.sh`; they retain
GreenSock's license, not Apache-2.0.

## Not bundled — fetched at authoring time

`scripts/fetch_clipart.mjs` downloads icons/emojis from the
[Iconify](https://iconify.design) API **into the user's working project
directory** when the author chooses to use them. They are not part of this
repository. Each icon set has its own license (Apache-2.0, MIT, CC-BY 4.0,
CC-BY-SA 4.0, ISC, …); the verified per-set table lives in
[`../references/concept-illustrations.md`](../references/concept-illustrations.md).
Attribution and ShareAlike obligations for any fetched assets fall on whoever
produces and distributes the resulting artifact.
