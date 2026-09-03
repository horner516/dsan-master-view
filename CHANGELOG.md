# Changelog

## 0.2.4 — 2026-09-03

- Made Network access a compact, full-width strip above the clock and cue panels, with links that wrap on smaller screens.
- Includes the port-conflict launch fix from 0.2.3.

## 0.2.3 — 2026-09-03

- Fixed a launch crash when another process already occupies the dashboard port.
- Desktop and browser servers now select an available port when the preferred port is busy; the dashboard and copied links show the actual port.
- Device connections start only after the web server successfully opens its port.

## 0.2.2 — 2026-09-03

- Added a visible Check for updates button on Mac and Windows, with the latest release page available from the browser viewer.
- Fixed copied network links so each address appears on its own line.
- Added ready-to-open, one-click LAN access links in the Network access card.
- Added copy buttons for the dashboard server port and URL list.
- Network access URLs now render as clickable `http://<ip>:<port>` links for remote configuration from other computers.

## 0.2.1 — 2026-09-03

- Enabled dashboard viewing and configuration from other computers on the same trusted network.
- The browser-only, Windows, and macOS applications now listen on all local network interfaces at port `53971`.
- Added optional username-and-password authentication for remote dashboard viewing and configuration; it is off by default for trusted networks.
- Passwords are stored as salted PBKDF2 hashes and are never returned to the dashboard.
- Added a touch-friendly Mobile view with the countdown, Limitimer status and lights, timer details, separate PerfectCue arrows, and Settings access.
- Added stable latest-release download links for Windows and macOS to the README.

## 0.2.0 — 2026-09-03

- Added a full macOS application with a standard window and D’S Dock icon.
- Added automated macOS DMG and Windows installer builds.
- Moved the local application service to port `53971`.

## 0.1.0 — 2026-09-03

- Initial Limitimer and PerfectCue viewer.
- Added configurable device addresses and ports, full-screen viewing, countdown options, clock fonts, and indicator-light controls.
