import ctypes
import sys
from pathlib import Path

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

APP_ID = "nan.image_resizer.desktop"

if __package__ in (None, ""):
    project_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(project_root))
    from src.ui.main_window import MainWindow
else:
    project_root = Path(__file__).resolve().parent.parent
    from .ui.main_window import MainWindow


def _set_windows_app_id() -> None:
    if sys.platform != "win32":
        return
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)
    except Exception:
        pass


def main() -> int:
    _set_windows_app_id()

    app = QApplication(sys.argv)
    app.setApplicationName("Image Resizer")
    app.setApplicationDisplayName("Image Resizer")

    icon_candidates = [
        project_root / "assets" / "app_icon.ico",
        project_root / "assets" / "app_icon.png",
        project_root / "assets" / "app_icon.svg",
    ]
    icon_path = next((path for path in icon_candidates if path.exists()), None)
    if icon_path is not None:
        app.setWindowIcon(QIcon(str(icon_path)))

    window = MainWindow()
    if icon_path is not None:
        window.setWindowIcon(QIcon(str(icon_path)))
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
