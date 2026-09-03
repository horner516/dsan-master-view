# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ["mac_app.py"],
    pathex=[],
    binaries=[],
    datas=[("index.html", ".")],
    hiddenimports=["webview.platforms.cocoa"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="DSanMasterView",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=True, name="DSanMasterView")
app = BUNDLE(
    coll,
    name="D'San Master View.app",
    icon="assets/dsan-master-view.icns",
    bundle_identifier="show.stg.dsan-master-view",
    info_plist={
        "CFBundleDisplayName": "D'San Master View",
        "CFBundleShortVersionString": "0.2.4",
        "CFBundleVersion": "0.2.4",
        "LSUIElement": False,
        "NSHighResolutionCapable": True,
    },
)
