from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QFileDialog,
    QMessageBox,
    QTableView,
    QHeaderView
)

from PySide6.QtGui import (
    QStandardItemModel,
    QStandardItem
)

from gui.dialog_strumento import DialogStrumento

from database import (
    leggi_strumenti,
    leggi_strumento,
    aggiungi_strumento,
    modifica_strumento,
    elimina_strumento,
    cerca_strumenti,
    numero_strumenti,
    valore_portafoglio,
    prezzo_corrente,
    variazione_corrente
)

from services.import_export import (
    esporta_excel,
    esporta_csv,
    importa_excel,
    importa_csv
)


class Portafoglio(QWidget):

    def __init__(self):
        super().__init__()

        self.crea_interfaccia()

        self.carica_tabella()

    # --------------------------------------------------

    def crea_interfaccia(self):

        layout = QVBoxLayout(self)

        titolo = QLabel("Portafoglio")

        titolo.setStyleSheet("""

            font-size:24px;

            font-weight:bold;

            padding:6px;

        """)

        layout.addWidget(titolo)

        # ---------------------------------------------
        # Toolbar
        # ---------------------------------------------

        barra = QHBoxLayout()

        self.btnNuovo = QPushButton("➕ Nuovo")

        self.btnModifica = QPushButton("✏️ Modifica")

        self.btnElimina = QPushButton("🗑️ Elimina")

        self.btnImporta = QPushButton("📥 Importa")

        self.btnEsporta = QPushButton("📤 Esporta")

        self.btnAggiorna = QPushButton("🔄 Aggiorna")

        self.ricerca = QLineEdit()

        self.ricerca.setPlaceholderText(
            "Cerca titolo..."
        )

        barra.addWidget(self.btnNuovo)

        barra.addWidget(self.btnModifica)

        barra.addWidget(self.btnElimina)

        barra.addSpacing(20)

        barra.addWidget(self.btnImporta)

        barra.addWidget(self.btnEsporta)

        barra.addSpacing(20)

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

            "Ticker",

            "Nome",

            "Quantità",

            "Prezzo Medio",

            "Prezzo Attuale",
            "Var %",
            "Valore Mercato",

            "Valuta",

            "Settore",

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

        self.tabella.setSelectionMode(
            QTableView.SingleSelection
        )

        self.tabella.horizontalHeader().setStretchLastSection(True)

        self.tabella.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(self.tabella)

        # ---------------------------------------------
        # Riepilogo
        # ---------------------------------------------

        self.lblRiepilogo = QLabel()

        self.lblRiepilogo.setStyleSheet("""

            font-size:15px;

            font-weight:bold;

            padding:8px;

        """)

        layout.addWidget(self.lblRiepilogo)

        # ---------------------------------------------
        # Eventi
        # ---------------------------------------------

        self.btnNuovo.clicked.connect(
            self.nuovo_strumento
        )

        self.btnModifica.clicked.connect(
            self.modifica_strumento_gui
        )

        self.btnElimina.clicked.connect(
            self.elimina_strumento_gui
        )

        self.btnImporta.clicked.connect(
            self.importa
        )

        self.btnEsporta.clicked.connect(
            self.esporta
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

        strumenti = leggi_strumenti()

        for s in strumenti:

            riga = [

                QStandardItem(str(s["id"])),

                QStandardItem(str(s["ticker"])),

                QStandardItem(str(s["nome"])),

                QStandardItem(f'{float(s["quantita"]):,.4f}'),

                QStandardItem(f'{float(s["prezzo_medio"]):,.4f}'),

                QStandardItem(f'{prezzo_corrente(s["ticker"]):,.4f}'),
                QStandardItem(f'{variazione_corrente(s["ticker"]):.2f}%'),
                QStandardItem(f'{float(s["quantita"])*prezzo_corrente(s["ticker"]):,.2f}'),

                QStandardItem(str(s["valuta"])),

                QStandardItem(str(s["settore"])),

                QStandardItem(str(s["note"]))

            ]

            self.modello.appendRow(riga)

        self.aggiorna_riepilogo()
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

    def nuovo_strumento(self):

        dialog = DialogStrumento(self)

        if dialog.exec():

            dati = dialog.dati()

            aggiungi_strumento(

                dati["ticker"],

                dati["nome"],

                dati["quantita"],

                dati["prezzo"],

                dati["valuta"],

                dati["settore"],

                dati["note"]

            )

            self.carica_tabella()

    # --------------------------------------------------

    def modifica_strumento_gui(self):

        id_strumento = self.riga_selezionata()

        if id_strumento is None:

            QMessageBox.warning(

                self,

                "Portafoglio",

                "Seleziona uno strumento."

            )

            return

        strumento = leggi_strumento(id_strumento)

        dialog = DialogStrumento(

            self,

            dati=strumento

        )

        if dialog.exec():

            dati = dialog.dati()

            modifica_strumento(

                id_strumento,

                dati["ticker"],

                dati["nome"],

                dati["quantita"],

                dati["prezzo"],

                dati["valuta"],

                dati["settore"],

                dati["note"]

            )

            self.carica_tabella()

    # --------------------------------------------------

    def elimina_strumento_gui(self):

        id_strumento = self.riga_selezionata()

        if id_strumento is None:

            QMessageBox.warning(

                self,

                "Portafoglio",

                "Seleziona uno strumento."

            )

            return

        risposta = QMessageBox.question(

            self,

            "Conferma",

            "Eliminare lo strumento selezionato?",

            QMessageBox.Yes | QMessageBox.No

        )

        if risposta != QMessageBox.Yes:

            return

        elimina_strumento(id_strumento)

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

        risultati = cerca_strumenti(testo)

        for s in risultati:

            riga = [

                QStandardItem(str(s["id"])),

                QStandardItem(str(s["ticker"])),

                QStandardItem(str(s["nome"])),

                QStandardItem(f'{float(s["quantita"]):,.4f}'),

                QStandardItem(f'{float(s["prezzo_medio"]):,.4f}'),

                QStandardItem(f'{prezzo_corrente(s["ticker"]):,.4f}'),
                QStandardItem(f'{variazione_corrente(s["ticker"]):.2f}%'),
                QStandardItem(f'{float(s["quantita"])*prezzo_corrente(s["ticker"]):,.2f}'),

                QStandardItem(str(s["valuta"])),

                QStandardItem(str(s["settore"])),

                QStandardItem(str(s["note"]))

            ]

            self.modello.appendRow(riga)

        self.aggiorna_riepilogo()

    # --------------------------------------------------

    def importa(self):

        file, _ = QFileDialog.getOpenFileName(

            self,

            "Importa portafoglio",

            "",

            "Excel (*.xlsx);;CSV (*.csv)"

        )

        if not file:

            return

        try:

            if file.lower().endswith(".xlsx"):

                dati = importa_excel(file)

            else:

                dati = importa_csv(file)

            for s in dati:

                aggiungi_strumento(

                    s["ticker"],

                    s["nome"],

                    s["quantita"],

                    s["prezzo"],

                    s["valuta"],

                    s["settore"],

                    s["note"]

                )

            self.carica_tabella()

            QMessageBox.information(

                self,

                "Importazione",

                "Importazione completata."

            )

        except Exception as e:

            QMessageBox.critical(

                self,

                "Errore",

                str(e)

            )

    # --------------------------------------------------

    def esporta(self):

        file, filtro = QFileDialog.getSaveFileName(

            self,

            "Esporta portafoglio",

            "",

            "Excel (*.xlsx);;CSV (*.csv)"

        )

        if not file:

            return

        strumenti = leggi_strumenti()

        try:

            if filtro.startswith("Excel"):

                if not file.lower().endswith(".xlsx"):

                    file += ".xlsx"

                esporta_excel(strumenti, file)

            else:

                if not file.lower().endswith(".csv"):

                    file += ".csv"

                esporta_csv(strumenti, file)

            QMessageBox.information(

                self,

                "Esportazione",

                "Esportazione completata."

            )

        except Exception as e:

            QMessageBox.critical(

                self,

                "Errore",

                str(e)

            )
    # --------------------------------------------------

    def aggiorna_riepilogo(self):

        self.lblRiepilogo.setText(

            f"Strumenti: {numero_strumenti()}    "
            f"Valore Portafoglio: {valore_portafoglio():,.2f} €"

        )

    # --------------------------------------------------

    def refresh(self):

        self.carica_tabella()

    # --------------------------------------------------

    def aggiorna(self):

        self.carica_tabella()

    # --------------------------------------------------

    def numero_righe(self):

        return self.modello.rowCount()

    # --------------------------------------------------

    def strumento_selezionato(self):

        id_strumento = self.riga_selezionata()

        if id_strumento is None:

            return None

        return leggi_strumento(id_strumento)

    # --------------------------------------------------

    def clear(self):

        self.modello.removeRows(

            0,

            self.modello.rowCount()

        )

        self.aggiorna_riepilogo()

    # --------------------------------------------------

    def resizeEvent(self, event):

        super().resizeEvent(event)

        self.tabella.resizeColumnsToContents()

    # --------------------------------------------------

    def showEvent(self, event):

        super().showEvent(event)

        self.carica_tabella()

    # --------------------------------------------------

    def hideEvent(self, event):

        super().hideEvent(event)

    # --------------------------------------------------

    def closeEvent(self, event):

        event.accept()