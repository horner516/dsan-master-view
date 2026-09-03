# Changelog

## 0.3.1 — 2026-09-03

- Added Settings network discovery with a user-selected local subnet and up to four configurable TCP ports.
- Lists all reachable endpoints with separate Use for Limitimer and Use for PerfectCue buttons; selecting a result fills the fields without connecting until Save and connect.
- Preserved manual entry and skips probing devices already connected by this app. Reachable ports are labeled as unverified rather than guessing device types.

## 0.3.0 — 2026-09-03

- Added presenter messages for all full-screen and `/full` displays, with text color, gentle flashing, and Show/Clear controls.
- Presenter messages start blank on host startup and are not saved between sessions.
- Added overall clock color and configurable green, yellow, and red status colors, with an override to keep the clock one color.
- Added Helvetica, Verdana, Georgia, Comic Sans MS, Trebuchet MS, Arial Black, and Impact font choices with local fallbacks.
- Retained the original full-screen clock sizing; removed the preview's maximum-size option.

## 0.2.9 — 2026-09-03

- Added `/full` and `/full/` URLs for TV browsers to load directly into the clock-and-arrow display with no setup controls or fullscreen prompt.
- The display fills the browser viewport without requiring the browser Fullscreen API. Remote authentication still applies when enabled.

## 0.2.8 — 2026-09-03

- Bundled trusted certificates for HTTPS update checks and installer downloads, instead of relying on certificate files on the build machine.
- Update failures now show the connection error or GitHub service status.
- The desktop browser button opens the normal setup page with no fullscreen query tag or automatic fullscreen request.

## 0.2.7 — 2026-09-03

- Fixed the page security policy blocking the desktop bridge used by update checks, installation, and opening the browser display.
- Enabled the required bridge scripting only for loopback requests to the desktop server; remote viewers and browser-only servers keep the stricter policy.

## 0.2.6 — 2026-09-03

- Update checks now open a persistent pop-up with progress, results, errors, and an Install update button.
- When current, the app says: "you are running the latest version you filthy animal".
- Desktop Full screen opens the clock and cue display in the default browser using the selected server port. If the browser blocks automatic fullscreen, click Enter full screen once.

## 0.2.5 — 2026-09-03

- Confirmed automatic startup port selection for both Windows and Mac, with explicit handling of Windows socket error 10048 (port already in use).
- Both desktop apps try port 53971 first, then use an available port if it is occupied. The Network access strip and copied links show the selected port.
- Includes the compact full-width Network access strip and Mac launch fix.

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
