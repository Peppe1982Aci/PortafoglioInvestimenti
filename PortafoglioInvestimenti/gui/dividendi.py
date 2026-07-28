from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QMessageBox,
    QTableView,
    QHeaderView,
    QInputDialog
)

from PySide6.QtGui import (
    QStandardItemModel,
    QStandardItem
)

from database import (
    get_connection
)


class Dividendi(QWidget):

    def __init__(self):
        super().__init__()

        self.crea_tabella()

        self.carica()

    # --------------------------------------------------

    def crea_tabella(self):

        layout = QVBoxLayout(self)

        titolo = QLabel("Dividendi")

        titolo.setStyleSheet("""

            font-size:24px;

            font-weight:bold;

            padding:8px;

        """)

        layout.addWidget(titolo)

        barra = QHBoxLayout()

        self.btnNuovo = QPushButton("➕ Nuovo")

        self.btnElimina = QPushButton("🗑️ Elimina")

        self.btnAggiorna = QPushButton("🔄 Aggiorna")

        barra.addWidget(self.btnNuovo)

        barra.addWidget(self.btnElimina)

        barra.addWidget(self.btnAggiorna)

        barra.addStretch()

        layout.addLayout(barra)

        self.modello = QStandardItemModel()

        self.modello.setHorizontalHeaderLabels([

            "ID",

            "Data",

            "Ticker",

            "Importo",

            "Valuta",

            "Note"

        ])

        self.tabella = QTableView()

        self.tabella.setModel(self.modello)

        self.tabella.setColumnHidden(0, True)

        self.tabella.setAlternatingRowColors(True)

        self.tabella.setSelectionBehavior(
            QTableView.SelectRows
        )

        self.tabella.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(self.tabella)

        self.lblTotale = QLabel()

        self.lblTotale.setStyleSheet("""

            font-size:16px;

            font-weight:bold;

            padding:8px;

        """)

        layout.addWidget(self.lblTotale)

        self.btnNuovo.clicked.connect(
            self.nuovo
        )

        self.btnElimina.clicked.connect(
            self.elimina
        )

        self.btnAggiorna.clicked.connect(
            self.carica
        )

    # --------------------------------------------------

    def crea_tabella_database(self):

        conn = get_connection()

        cur = conn.cursor()

        cur.execute("""

            CREATE TABLE IF NOT EXISTS dividendi(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                data TEXT,

                ticker TEXT,

                importo REAL,

                valuta TEXT,

                note TEXT

            )

        """)

        conn.commit()

        conn.close()

    # --------------------------------------------------

    def carica(self):

        self.crea_tabella_database()

        self.modello.removeRows(
            0,
            self.modello.rowCount()
        )

        conn = get_connection()

        cur = conn.cursor()

        cur.execute("""

            SELECT *

            FROM dividendi

            ORDER BY data DESC

        """)

        totale = 0

        for r in cur.fetchall():

            totale += float(r["importo"])

            self.modello.appendRow([

                QStandardItem(str(r["id"])),

                QStandardItem(str(r["data"])),

                QStandardItem(str(r["ticker"])),

                QStandardItem(f'{float(r["importo"]):,.2f}'),

                QStandardItem(str(r["valuta"])),

                QStandardItem(str(r["note"]))

            ])

        conn.close()

        self.lblTotale.setText(

            f"Dividendi incassati: {totale:,.2f} €"

        )

    # --------------------------------------------------

    def nuovo(self):

        data, ok = QInputDialog.getText(

            self,

            "Data",

            "Data (YYYY-MM-DD)"

        )

        if not ok:

            return

        ticker, ok = QInputDialog.getText(

            self,

            "Ticker",

            "Ticker"

        )

        if not ok:

            return

        importo, ok = QInputDialog.getDouble(

            self,

            "Importo",

            "Importo",

            0,

            0,

            1000000,

            2

        )

        if not ok:

            return

        conn = get_connection()

        cur = conn.cursor()

        cur.execute("""

            INSERT INTO dividendi

            (

                data,

                ticker,

                importo,

                valuta,

                note

            )

            VALUES

            (?, ?, ?, ?, ?)

        """, (

            data,

            ticker.upper(),

            importo,

            "EUR",

            ""

        ))

        conn.commit()

        conn.close()

        self.carica()

    # --------------------------------------------------

    def elimina(self):

        indice = self.tabella.currentIndex()

        if not indice.isValid():

            QMessageBox.warning(

                self,

                "Dividendi",

                "Seleziona un dividendo."

            )

            return

        id_dividendo = self.modello.item(

            indice.row(),

            0

        ).text()

        risposta = QMessageBox.question(

            self,

            "Conferma",

            "Eliminare il dividendo?"

        )

        if risposta != QMessageBox.Yes:

            return

        conn = get_connection()

        cur = conn.cursor()

        cur.execute(

            "DELETE FROM dividendi WHERE id=?",

            (id_dividendo,)

        )

        conn.commit()

        conn.close()

        self.carica()

    # --------------------------------------------------

    def refresh(self):

        self.carica()

    # --------------------------------------------------

    def aggiorna(self):

        self.carica()