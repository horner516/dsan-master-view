# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ["desktop.py"],
    pathex=[],
    binaries=[],
    datas=[("index.html", "."), ("assets/dsan-master-view.ico", "assets")],
    hiddenimports=["webview.platforms.edgechromium"],
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
    a.binaries,
    a.datas,
    [],
    name="DSanMasterView",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon="assets/dsan-master-view.ico",
)
