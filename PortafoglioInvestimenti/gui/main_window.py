from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTabWidget,
    QApplication,
    QMessageBox,
    QFileDialog
)

from PySide6.QtGui import (
    QAction,
    QIcon
)

from PySide6.QtCore import Qt

from gui.dashboard import Dashboard
from gui.portafoglio import Portafoglio
from gui.operazioni import Operazioni
from gui.dividendi import Dividendi
from gui.statistiche import Statistiche

from services.backup import (
    crea_backup,
    ripristina_backup
)

from database import inizializza_database


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        inizializza_database()

        self.setWindowTitle(
            "Portafoglio Investimenti"
        )

        self.resize(1400, 850)

        self.crea_menu()

        self.crea_interfaccia()

    # --------------------------------------------------

    def crea_interfaccia(self):

        centrale = QWidget()

        self.setCentralWidget(centrale)

        layout = QVBoxLayout(centrale)

        self.tabs = QTabWidget()

        self.dashboard = Dashboard()

        self.portafoglio = Portafoglio()

        self.operazioni = Operazioni()

        self.dividendi = Dividendi()

        self.statistiche = Statistiche()

        self.tabs.addTab(
            self.dashboard,
            "Dashboard"
        )

        self.tabs.addTab(
            self.portafoglio,
            "Portafoglio"
        )

        self.tabs.addTab(
            self.operazioni,
            "Operazioni"
        )

        self.tabs.addTab(
            self.dividendi,
            "Dividendi"
        )

        self.tabs.addTab(
            self.statistiche,
            "Statistiche"
        )

        layout.addWidget(self.tabs)

        self.tabs.currentChanged.connect(
            self.aggiorna_schermata
        )
    # --------------------------------------------------

    def crea_menu(self):

        menu_file = self.menuBar().addMenu("&File")

        actBackup = QAction(
            "Crea Backup",
            self
        )

        actRipristina = QAction(
            "Ripristina Backup",
            self
        )

        actEsci = QAction(
            "Esci",
            self
        )

        menu_file.addAction(actBackup)

        menu_file.addAction(actRipristina)

        menu_file.addSeparator()

        menu_file.addAction(actEsci)

        actBackup.triggered.connect(
            self.backup
        )

        actRipristina.triggered.connect(
            self.ripristina
        )

        actEsci.triggered.connect(
            self.close
        )

        # -----------------------------------------

        menu_visualizza = self.menuBar().addMenu(
            "&Visualizza"
        )

        actAggiorna = QAction(
            "Aggiorna",
            self
        )

        menu_visualizza.addAction(
            actAggiorna
        )

        actAggiorna.triggered.connect(
            self.aggiorna_tutto
        )

        # -----------------------------------------

        menu_aiuto = self.menuBar().addMenu(
            "&Aiuto"
        )

        actInfo = QAction(
            "Informazioni",
            self
        )

        menu_aiuto.addAction(
            actInfo
        )

        actInfo.triggered.connect(
            self.informazioni
        )

    # --------------------------------------------------

    def aggiorna_schermata(self):

        indice = self.tabs.currentIndex()

        if indice == 0:

            self.dashboard.refresh()

        elif indice == 1:

            self.portafoglio.refresh()

        elif indice == 2:

            self.operazioni.refresh()

        elif indice == 3:

            self.dividendi.refresh()

        elif indice == 4:

            self.statistiche.refresh()

    # --------------------------------------------------

    def aggiorna_tutto(self):

        self.dashboard.refresh()

        self.portafoglio.refresh()

        self.operazioni.refresh()

        self.dividendi.refresh()

        self.statistiche.refresh()
    # --------------------------------------------------

    def backup(self):

        file, _ = QFileDialog.getSaveFileName(

            self,

            "Salva Backup",

            "backup_portafoglio.db",

            "Database SQLite (*.db)"

        )

        if not file:

            return

        try:

            crea_backup(file)

            QMessageBox.information(

                self,

                "Backup",

                "Backup creato correttamente."

            )

        except Exception as e:

            QMessageBox.critical(

                self,

                "Errore",

                str(e)

            )

    # --------------------------------------------------

    def ripristina(self):

        file, _ = QFileDialog.getOpenFileName(

            self,

            "Ripristina Backup",

            "",

            "Database SQLite (*.db)"

        )

        if not file:

            return

        risposta = QMessageBox.question(

            self,

            "Ripristino",

            "Il database corrente verrà sostituito.\n\nContinuare?",

            QMessageBox.Yes | QMessageBox.No

        )

        if risposta != QMessageBox.Yes:

            return

        try:

            ripristina_backup(file)

            self.aggiorna_tutto()

            QMessageBox.information(

                self,

                "Ripristino",

                "Backup ripristinato correttamente."

            )

        except Exception as e:

            QMessageBox.critical(

                self,

                "Errore",

                str(e)

            )

    # --------------------------------------------------

    def informazioni(self):

        QMessageBox.about(

            self,

            "Portafoglio Investimenti",

            """
<b>Portafoglio Investimenti</b>

Versione 2.2

Applicazione desktop sviluppata con:

• Python
• PySide6
• SQLite

Funzioni disponibili:

• Gestione Portafoglio
• Gestione Operazioni
• Gestione Dividendi
• Dashboard
• Statistiche
• Backup e Ripristino
• Import / Export

© 2026
            """

        )

    # --------------------------------------------------

    def closeEvent(self, event):

        event.accept()