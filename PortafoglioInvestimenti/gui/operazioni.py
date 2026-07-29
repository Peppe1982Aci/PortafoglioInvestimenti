from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QTableView,
    QLineEdit,
    QHeaderView,
    QMessageBox
)

from PySide6.QtGui import (
    QStandardItemModel,
    QStandardItem
)

from gui.dialog_operazione import DialogOperazione

from database import (
    leggi_operazioni,
    leggi_operazione,
    aggiungi_operazione,
    modifica_operazione,
    elimina_operazione,
    cerca_operazioni,
    leggi_strumenti,
    aggiorna_portafoglio,
    numero_operazioni,
    totale_commissioni
)


class Operazioni(QWidget):

    def __init__(self):
        super().__init__()

        self.crea_interfaccia()

        self.carica_tabella()

    # --------------------------------------------------

    def crea_interfaccia(self):

        layout = QVBoxLayout(self)

        titolo = QLabel("Operazioni")

        titolo.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
            padding:6px;
        """)

        layout.addWidget(titolo)

        # ---------------------------------------------
        # Barra strumenti
        # ---------------------------------------------

        barra = QHBoxLayout()

        self.btnNuova = QPushButton("➕ Nuova")

        self.btnModifica = QPushButton("✏️ Modifica")

        self.btnElimina = QPushButton("🗑️ Elimina")

        self.btnAggiorna = QPushButton("🔄 Aggiorna")

        self.ricerca = QLineEdit()

        self.ricerca.setPlaceholderText(
            "Cerca operazione..."
        )

        barra.addWidget(self.btnNuova)

        barra.addWidget(self.btnModifica)

        barra.addWidget(self.btnElimina)

        barra.addWidget(self.btnAggiorna)

        barra.addStretch()

        barra.addWidget(self.ricerca)

        layout.addLayout(barra)

        # ---------------------------------------------
        # Tabella
        # ---------------------------------------------

        self.modello = QStandardItemModel()

        self.modello.setHorizontalHeaderLabels([

            "ID",

            "Data",

            "Ticker",

            "Tipo",

            "Quantità",

            "Prezzo",

            "Commissioni",

            "Cambio",

            "Note"

        ])

        self.tabella = QTableView()

        self.tabella.setModel(self.modello)

        self.tabella.setColumnHidden(0, True)

        self.tabella.setAlternatingRowColors(True)

        self.tabella.setSortingEnabled(True)

        self.tabella.setSelectionBehavior(
            QTableView.SelectRows
        )

        self.tabella.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(self.tabella)

        self.lblTotale = QLabel()

        self.lblTotale.setStyleSheet("""
            font-size:15px;
            font-weight:bold;
            padding:8px;
        """)

        layout.addWidget(self.lblTotale)

        self.btnNuova.clicked.connect(
            self.nuova_operazione
        )

        self.btnModifica.clicked.connect(
            self.modifica_operazione_gui
        )

        self.btnElimina.clicked.connect(
            self.elimina_operazione_gui
        )

        self.btnAggiorna.clicked.connect(
            self.carica_tabella
        )

        self.ricerca.textChanged.connect(
            self.filtra_tabella
        )
    # --------------------------------------------------

    def carica_tabella(self):

        self.modello.removeRows(
            0,
            self.modello.rowCount()
        )

        operazioni = leggi_operazioni()

        for op in operazioni:

            riga = [

                QStandardItem(str(op["id"])),

                QStandardItem(str(op["data"])),

                QStandardItem(str(op["ticker"])),

                QStandardItem(str(op["tipo"])),

                QStandardItem(f'{float(op["quantita"]):,.4f}'),

                QStandardItem(f'{float(op["prezzo"]):,.4f}'),

                QStandardItem(f'{float(op["commissioni"]):,.2f}'),

                QStandardItem(f'{float(op["cambio"]):,.4f}'),

                QStandardItem(str(op["note"]))

            ]

            self.modello.appendRow(riga)

        self.lblTotale.setText(

            f"Operazioni: {numero_operazioni()}    "
            f"Commissioni: {totale_commissioni():,.2f} €"

        )

    # --------------------------------------------------

    def ticker_disponibili(self):

        lista = []

        for s in leggi_strumenti():

            lista.append(s["ticker"])

        return lista

    # --------------------------------------------------

    def nuova_operazione(self):

        dialog = DialogOperazione(

            self,

            ticker_list=self.ticker_disponibili()

        )

        if dialog.exec():

            dati = dialog.dati()

            aggiungi_operazione(

                dati["data"],

                dati["ticker"],

                dati["tipo"],

                dati["quantita"],

                dati["prezzo"],

                dati["commissioni"],

                dati["cambio"],

                dati["note"]

            )

            aggiorna_portafoglio()

            self.carica_tabella()

    # --------------------------------------------------

    def riga_selezionata(self):

        indice = self.tabella.currentIndex()

        if not indice.isValid():

            return None

        return self.modello.item(

            indice.row(),

            0

        ).text()
    # --------------------------------------------------

    def modifica_operazione_gui(self):

        id_operazione = self.riga_selezionata()

        if id_operazione is None:

            QMessageBox.warning(

                self,

                "Operazioni",

                "Seleziona un'operazione."

            )

            return

        operazione = leggi_operazione(id_operazione)

        dialog = DialogOperazione(

            self,

            dati=operazione,

            ticker_list=self.ticker_disponibili()

        )

        if dialog.exec():

            dati = dialog.dati()

            modifica_operazione(

                id_operazione,

                dati["data"],

                dati["ticker"],

                dati["tipo"],

                dati["quantita"],

                dati["prezzo"],

                dati["commissioni"],

                dati["cambio"],

                dati["note"]

            )

            aggiorna_portafoglio()

            self.carica_tabella()

    # --------------------------------------------------

    def elimina_operazione_gui(self):

        id_operazione = self.riga_selezionata()

        if id_operazione is None:

            QMessageBox.warning(

                self,

                "Operazioni",

                "Seleziona un'operazione."

            )

            return

        risposta = QMessageBox.question(

            self,

            "Conferma",

            "Eliminare l'operazione selezionata?",

            QMessageBox.Yes | QMessageBox.No

        )

        if risposta != QMessageBox.Yes:

            return

        elimina_operazione(id_operazione)

        aggiorna_portafoglio()

        self.carica_tabella()

    # --------------------------------------------------

    def filtra_tabella(self):

        testo = self.ricerca.text().strip()

        if testo == "":

            self.carica_tabella()

            return

        self.modello.removeRows(

            0,

            self.modello.rowCount()

        )

        risultati = cerca_operazioni(testo)

        for op in risultati:

            riga = [

                QStandardItem(str(op["id"])),

                QStandardItem(str(op["data"])),

                QStandardItem(str(op["ticker"])),

                QStandardItem(str(op["tipo"])),

                QStandardItem(f'{float(op["quantita"]):,.4f}'),

                QStandardItem(f'{float(op["prezzo"]):,.4f}'),

                QStandardItem(f'{float(op["commissioni"]):,.2f}'),

                QStandardItem(f'{float(op["cambio"]):,.4f}'),

                QStandardItem(str(op["note"]))

            ]

            self.modello.appendRow(riga)
    # --------------------------------------------------

    def refresh(self):

        self.carica_tabella()

    # --------------------------------------------------

    def aggiorna(self):

        self.carica_tabella()

    # --------------------------------------------------

    def totale_operazioni(self):

        totale = 0.0

        for riga in range(self.modello.rowCount()):

            quantita = float(
                self.modello.item(riga, 4).text().replace(",", "")
            )

            prezzo = float(
                self.modello.item(riga, 5).text().replace(",", "")
            )

            commissioni = float(
                self.modello.item(riga, 6).text().replace(",", "")
            )

            totale += (quantita * prezzo) + commissioni

        return totale

    # --------------------------------------------------

    def totale_commissioni_tabella(self):

        totale = 0.0

        for riga in range(self.modello.rowCount()):

            totale += float(
                self.modello.item(riga, 6).text().replace(",", "")
            )

        return totale

    # --------------------------------------------------

    def numero_righe(self):

        return self.modello.rowCount()

    # --------------------------------------------------

    def operazione_selezionata(self):

        indice = self.tabella.currentIndex()

        if not indice.isValid():
            return None

        return leggi_operazione(

            self.modello.item(
                indice.row(),
                0
            ).text()

        )

    # --------------------------------------------------

    def clear(self):

        self.modello.removeRows(
            0,
            self.modello.rowCount()
        )

        self.lblTotale.setText(
            "Operazioni: 0    Commissioni: 0,00 €"
        )