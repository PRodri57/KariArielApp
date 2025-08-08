from __future__ import annotations

import sys
from PySide6.QtWidgets import QApplication, QDialog
from mainGUI_qt import AppPrincipalQt, apply_dark_palette
from login_qt import LoginDialogQt


def main() -> int:
    app = QApplication(sys.argv)
    apply_dark_palette(app)

    login = LoginDialogQt()
    result = login.exec()
    if result == QDialog.Accepted:
        window = AppPrincipalQt()
        window.show()
        return app.exec()
    return 0


if __name__ == "__main__":
    sys.exit(main())


