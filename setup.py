from setuptools import setup

OPTIONS = {
    "argv_emulation": False,
    "packages": ["rumps", "pyperclip"],
    "iconfile": "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/ExecutableBinaryIcon.icns",
    "plist": {
        "LSUIElement": True,
    },
}

setup(
    name="ClipboardManager",
    app=["main.py"],
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)

