# D’San Master View

A local browser dashboard that reads a Limitimer controller and PerfectCue network adapter at the same time. Each device has its own configurable IP address and TCP port.

## Download the latest release

- [Download for Windows](https://github.com/horner516/dsan-master-view/releases/latest/download/DSanMasterView-Windows-Setup.exe)
- [Download for macOS](https://github.com/horner516/dsan-master-view/releases/latest/download/DSanMasterView-macOS.dmg)

## Start

Double-click `start.command`, then open <http://127.0.0.1:53971> if the dashboard does not open automatically.

The first launch is preconfigured for the Limitimer at `10.21.0.119:6120`. Open **Settings** to change its address or add the PerfectCue adapter. Settings are saved locally in `viewer-config.json`.

Use **Full screen** for a clean 16:9 output with a centered countdown and separate Previous/Next indicators beneath it. Press Escape to leave full-screen mode. Under **Settings**, choose the clock font, show or hide Limitimer lights, and set the countdown to stop visually at `00:00` or show negative overtime.

## Windows widget

The Windows installer is built automatically by GitHub Actions. Run the installed **D’San Master View** shortcut to open an always-on-top, frameless widget. Drag its header to move it. Right-click anywhere in the widget to check for updates, toggle always-on-top, or close it.

To publish an update, change `APP_VERSION` in `desktop.py` and `MyAppVersion` in `installer.iss`, then push a matching tag such as `v0.1.1`. The release installer is used by the widget’s update checker.

## macOS application

Download the macOS `.dmg`, drag **D’San Master View** into Applications, and launch it like a normal Mac app. It uses a standard resizable application window and keeps the D’S logo visible in the Dock. The same right-click menu can check for updates or optionally keep the viewer above other windows.

The browser-only viewer and both installed desktop applications use the uncommon local port `53971` to minimize conflicts. Device TCP ports remain independently configurable under **Settings**.

## Configure from another computer

While D’San Master View is running, another computer on the same network can open `http://HOST-COMPUTER-IP:53971` to view the dashboard and change Settings. Replace `HOST-COMPUTER-IP` with the LAN address of the Mac or Windows computer running the app.

Remote access intentionally has no PIN or password and should be used only on a trusted network. The operating system may ask whether to allow incoming network connections on first launch.

The first unsigned build may require Control-clicking the app and choosing **Open**. A future Apple Developer ID signature can remove this Gatekeeper warning.

## Supported data

- Limitimer: selected countdown, total, elapsed, remaining, sum-up threshold, run state, signal color, timer direction, and checksum validation.
- PerfectCue: green Next (`0x0F`), red Previous (`0x1F`), Blank/yellow-off (`0x2F`), and Blank/yellow-on (`0x3F`). Directional cues remain visible for two seconds; repeated same-direction cues flash for half a second.

Device data is not sent to an internet service. The dashboard is served directly by the host computer to trusted devices on the same network.
