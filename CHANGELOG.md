# Unreleased


* Thanks to [Manu](https://github.com/manutortosa-collab)'s tremendous work, the theme now supports 93 new systems, including plenty of new collections with high-quality fanarts.
* Add translations of all the UI and the systems metadata in 18 languages (spanish translation by [Manu](https://github.com/manutortosa-collab)).
* Add video previews to the game details page (when available).
* Add option to enable loading logos from SVG files for sharper and scalable graphics (thanks [Manu](https://github.com/manutortosa-collab)).
* Add the `Logo Region` option (Europe, USA, Japan) to load regional SVG logos (`<system>/<region>.svg`, `<system>/<scheme>-<region>.svg` or `<system>-<region>.svg`), with a fallback to other regions and to generic logos.
* SVG logos can now have separate versions for each color scheme: when enabled, `_inc/logos-svg/<system>/light.svg` or `dark.svg` take precedence over `_inc/logos-svg/<system>.svg`, which in turn takes precedence over the bitmap logo.
* Add the Retrobox distribution option to the theme settings.
* Add controllers status icons in carrousel (thanks [Manu](https://github.com/manutortosa-collab)).
* Simplfy the customization of theme backgrounds (thanks [Manu](https://github.com/manutortosa-collab)).
* Fix automatic collections not dynamically populating the games list (thanks [Manu](https://github.com/manutortosa-collab)).



# 1.0.1 (2025-02-07)

* Fix some systems not recognized by Batocera due to misnaming.
* Reduce detailed description text cut-off.

# 1.0.0 (2025-02-06)

* Add views for list of systems (`carousel`) and games (`detailed`, `grid` and `basic`).
* Add support for `16:9`, `16:10`, `3:2`, `4:3` and `1:1` aspect ratios.
* Add `light` and `dark` color schemes.
