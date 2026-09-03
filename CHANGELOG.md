# Changelog

## 0.2.1 — 2026-09-03

- Enabled dashboard viewing and configuration from other computers on the same trusted network.
- The browser-only, Windows, and macOS applications now listen on all local network interfaces at port `53971`.
- Added optional username-and-password authentication for remote dashboard viewing and configuration; it is off by default for trusted networks.
- Passwords are stored as salted PBKDF2 hashes and are never returned to the dashboard.
- Added stable latest-release download links for Windows and macOS to the README.

## 0.2.0 — 2026-09-03

- Added a full macOS application with a standard window and D’S Dock icon.
- Added automated macOS DMG and Windows installer builds.
- Moved the local application service to port `53971`.

## 0.1.0 — 2026-09-03

- Initial Limitimer and PerfectCue viewer.
- Added configurable device addresses and ports, full-screen viewing, countdown options, clock fonts, and indicator-light controls.
