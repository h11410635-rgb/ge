# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for RedirectVPNspoof.

Build:
    pyinstaller --clean -y RedirectVPNspoof.spec

Produces dist/RedirectVPNspoof(.exe) — single-file executable that
contains Python, Flask, Werkzeug, requests, waitress and HTML templates.
At runtime it stores its SQLite database in a `data/` folder next to the
executable.
"""
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

hiddenimports = []
hiddenimports += collect_submodules("waitress")
hiddenimports += collect_submodules("werkzeug")
hiddenimports += collect_submodules("flask")

datas = [
    ("app/templates", "app/templates"),
]

a = Analysis(
    ["run.py"],
    pathex=["."],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["tkinter", "pytest", "unittest"],
    noarchive=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="RedirectVPNspoof",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=True,      # оставляем консоль, чтобы видеть URL и логи
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
