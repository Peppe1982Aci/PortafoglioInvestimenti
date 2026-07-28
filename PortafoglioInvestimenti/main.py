import sys

from PySide6.QtWidgets import QApplication

from database import inizializza_database
from gui.main_window import MainWindow


def main():

    # -------------------------------------------------
    # Inizializza database
    # -------------------------------------------------

    inizializza_database()

    # -------------------------------------------------
    # Avvio applicazione
    # -------------------------------------------------

    app = QApplication(sys.argv)

    app.setApplicationName("Portfolio Investimenti")
    app.setOrganizationName("Portfolio Investimenti")
    app.setApplicationVersion("2.1.0")

    finestra = MainWindow()
    finestra.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()