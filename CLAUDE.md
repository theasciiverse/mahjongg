# Mahjongg (Asciiverse packaging)

Mahjong solitaire in the terminal, a clone of GNOME Mahjongg by radha, in
Rust and Ratatui; packaged for the Asciiverse catalog and as system
packages. Not our code: keep changes small, list every one in PATCHES.md,
and offer fixes upstream.

- Remotes: `upstream` is github.com/radha/mahjongg, `origin` is
  github.com/theasciiverse/mahjongg.
- Branch `asciiverse` = upstream main plus our commits.
- Release: tag `v<version>-av.<n>` and push it.
- Local static build: `docker run --rm -v "$PWD":/src -w /src
  rust:1-alpine sh -c 'apk add musl-dev && cargo build --release
  --target-dir target-musl'`.
- Preview: `python3 asciiverse/record-preview.py` (needs asciinema 3.x and
  pyte) plays a fresh game with mouse clicks into a throwaway home.
- Files: settings in `$XDG_CONFIG_HOME/tui-mahjongg/`, scores and the saved
  game in `$XDG_DATA_HOME/tui-mahjongg/` (`%APPDATA%`/`%LOCALAPPDATA%` on
  Windows), outside the install folder, so an av update keeps them.
