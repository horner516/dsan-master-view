#!/usr/bin/env python3
"""Desktop shells and update support for D’San Master View."""

from __future__ import annotations

import json
import os
import ssl
import subprocess
import sys
import tempfile
import threading
import urllib.error
import urllib.request
import webbrowser
from pathlib import Path

import webview
import certifi

from app import LOCAL_PORT, create_server


APP_VERSION = "0.3.0"
UPDATE_REPOSITORY = os.environ.get("DSAN_UPDATE_REPO", "horner516/dsan-master-view")


def update_ssl_context() -> ssl.SSLContext:
    # Frozen Python cannot rely on certificate paths from the build machine.
    context = ssl.create_default_context()
    context.load_verify_locations(cafile=certifi.where())
    return context


def version_tuple(value: str) -> tuple[int, ...]:
    cleaned = value.strip().lstrip("v")
    try:
        return tuple(int(part) for part in cleaned.split("."))
    except ValueError:
        return (0,)


class DesktopApi:
    def __init__(self, is_widget: bool) -> None:
        self.window: webview.Window | None = None
        self.is_widget = is_widget
        self.on_top = is_widget
        self.pending_asset: str | None = None
        self.server_port = LOCAL_PORT

    def open_browser_fullscreen(self) -> dict[str, str]:
        url = f"http://127.0.0.1:{self.server_port}/"
        if not webbrowser.open(url, new=1):
            raise RuntimeError("Could not open your browser.")
        return {"message": "Setup page opened in your browser."}

    def app_state(self) -> dict[str, bool]:
        return {"is_widget": self.is_widget, "on_top": self.on_top}

    def check_for_updates(self) -> dict[str, object]:
        self.pending_asset = None
        request = urllib.request.Request(
            f"https://api.github.com/repos/{UPDATE_REPOSITORY}/releases/latest",
            headers={"Accept": "application/vnd.github+json", "User-Agent": "DSan-Master-View"},
        )
        try:
            with urllib.request.urlopen(request, timeout=15, context=update_ssl_context()) as response:
                release = json.load(response)
        except urllib.error.HTTPError as error:
            message = "GitHub is temporarily limiting update checks. Please try again later." if error.code in (403, 429) else f"Update service returned HTTP {error.code}. Please try again later."
            return {"update_available": False, "message": message}
        except (urllib.error.URLError, OSError, ValueError) as error:
            reason = getattr(error, "reason", error)
            return {"update_available": False, "message": f"Could not reach the update service: {reason}"}

        version = str(release.get("tag_name", "")).lstrip("v")
        assets = release.get("assets", [])
        suffix = "-setup.exe" if sys.platform == "win32" else "-macos.dmg"
        installer = next((asset for asset in assets if str(asset.get("name", "")).lower().endswith(suffix)), None)
        if not version or version_tuple(version) == (0,):
            return {"update_available": False, "message": "Could not read the latest release version. Please try again."}
        if version_tuple(version) <= version_tuple(APP_VERSION):
            return {"update_available": False, "message": "you are running the latest version you filthy animal"}
        if not installer:
            return {"update_available": False, "message": f"Version {version} is available, but has no installer."}
        self.pending_asset = str(installer["browser_download_url"])
        return {
            "update_available": True,
            "version": version,
            "message": f"Version {version} is available. Install it now?",
        }

    def install_update(self) -> dict[str, str]:
        if not self.pending_asset or not self.pending_asset.startswith("https://github.com/"):
            return {"message": "No verified update is ready to install."}
        extension = ".exe" if sys.platform == "win32" else ".dmg"
        destination = Path(tempfile.gettempdir()) / f"DSanMasterView-Update{extension}"
        try:
            request = urllib.request.Request(self.pending_asset, headers={"User-Agent": "DSan-Master-View"})
            with urllib.request.urlopen(request, timeout=60, context=update_ssl_context()) as response, destination.open("wb") as output:
                output.write(response.read())
            if sys.platform == "win32":
                os.startfile(destination)  # type: ignore[attr-defined]
            else:
                subprocess.Popen(["open", str(destination)])
            return {"message": "The update installer is starting."}
        except (OSError, urllib.error.URLError, TimeoutError):
            return {"message": "The update could not be downloaded."}

    def toggle_on_top(self) -> dict[str, bool]:
        self.on_top = not self.on_top
        if self.window is not None:
            self.window.on_top = self.on_top
        return {"on_top": self.on_top}

    def close_widget(self) -> None:
        if self.window is not None:
            self.window.destroy()


def run_desktop(*, widget: bool) -> None:
    if "--check-update" in sys.argv:
        print(json.dumps(DesktopApi(widget).check_for_updates()), flush=True)
        return
    server = create_server()
    server.desktop_bridge = True
    threading.Thread(target=server.serve_forever, name="local-web-server", daemon=True).start()
    api = DesktopApi(is_widget=widget)
    api.server_port = server.server_port
    api.window = webview.create_window(
        "D’San Master View",
        f"http://127.0.0.1:{server.server_port}",
        js_api=api,
        width=1280,
        height=720,
        min_size=(900, 540),
        frameless=widget,
        easy_drag=not widget,
        on_top=widget,
        shadow=True,
    )
    try:
        webview.start(debug=False)
    finally:
        server.shutdown()
        server.server_close()


def main() -> None:
    run_desktop(widget=True)


if __name__ == "__main__":
    main()
