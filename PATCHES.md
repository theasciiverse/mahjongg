# Changes from upstream

This is the Asciiverse packaging of [Mahjongg](https://github.com/radha/mahjongg)
by radha (GPL-3.0-or-later), a terminal clone of GNOME Mahjongg in Rust and
Ratatui, built from upstream's main as of 2026-10-07 (commit `cc3d4a7`,
version 0.1.0; upstream has no tags). Upstream is the `upstream` remote; the
`asciiverse` branch carries the changes below. The code change is worth
offering upstream.

## Code

- **Settings, scores and the saved game work on Windows.** They were stored
  under `$XDG_CONFIG_HOME`/`$XDG_DATA_HOME`, falling back to `$HOME`, which
  Windows does not set, so nothing was ever saved there. With neither set,
  settings now go under `%APPDATA%\tui-mahjongg` and scores and the saved
  game under `%LOCALAPPDATA%\tui-mahjongg`. Linux and macOS are unchanged.

## Packaging (new files)

- `.github/workflows/release.yml`: av archives for Linux (static), macOS
  and Windows, each x86-64 and ARM64, plus SHA256SUMS, and .deb, .rpm,
  .apk and Arch packages.
- `asciiverse/nfpm.yaml`: the system packages.
- `asciiverse/record-preview.py`: records the catalog preview (a Turtle
  game played with the mouse, nine pairs found with Hint).
