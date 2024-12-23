# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets/icon.ico', 'assets')],
    hiddenimports=['PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter', 'unittest', 'email', 'html', 'http', 'xml',
        'pydoc', 'doctest', 'pip', 'setuptools', 'PIL', 
        'numpy', 'pandas', 'scipy', 'matplotlib', 'PyQt6.QtNetwork',
        'PyQt6.QtMultimedia', 'PyQt6.QtDBus', 'PyQt6.QtWebEngine',
        'PyQt6.QtWebEngineCore', 'PyQt6.QtWebEngineWidgets',
        'PyQt6.QtPositioning', 'cryptography', 'lib2to3',
        '_decimal', 'win32com', 'pythoncom', 'pywintypes',
        'pkg_resources', 'IPython', 'jedi', 'colorama',
        'asyncio', 'concurrent', 'distutils', 'logging', 'multiprocessing',
        'pdb', 'pickle', 'tty', 'webbrowser', 'xml', 'xmlrpc',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# 删除不需要的二进制文件
a.binaries = [x for x in a.binaries if not x[0].startswith('opengl32')]
a.binaries = [x for x in a.binaries if not x[0].startswith('Qt6OpenGL')]
a.binaries = [x for x in a.binaries if not x[0].startswith('Qt6Pdf')]
a.binaries = [x for x in a.binaries if not x[0].startswith('Qt6Quick')]
a.binaries = [x for x in a.binaries if not x[0].startswith('Qt6Qml')]
a.binaries = [x for x in a.binaries if not x[0].startswith('Qt6Network')]
a.binaries = [x for x in a.binaries if not x[0].startswith('Qt6Svg')]
a.binaries = [x for x in a.binaries if not x[0].startswith('Qt6Test')]
a.binaries = [x for x in a.binaries if not x[0].startswith('Qt6Designer')]
a.binaries = [x for x in a.binaries if not x[0].startswith('Qt6Help')]
a.binaries = [x for x in a.binaries if not x[0].startswith('Qt6Location')]
a.binaries = [x for x in a.binaries if not x[0].startswith('Qt6Multimedia')]
a.binaries = [x for x in a.binaries if not x[0].startswith('Qt6WebEngine')]
a.binaries = [x for x in a.binaries if not x[0].startswith('Qt6Positioning')]
a.binaries = [x for x in a.binaries if not x[0].startswith('Qt6DBus')]
a.binaries = [x for x in a.binaries if not x[0].startswith('Qt6PrintSupport')]
a.binaries = [x for x in a.binaries if not x[0].startswith('imageformats/qtga')]
a.binaries = [x for x in a.binaries if not x[0].startswith('imageformats/qtiff')]
a.binaries = [x for x in a.binaries if not x[0].startswith('imageformats/qwebp')]
a.binaries = [x for x in a.binaries if not x[0].startswith('imageformats/qpdf')]
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='WiFi热点管理工具',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',
    version='file_version_info.txt',
    uac_admin=True,
) 