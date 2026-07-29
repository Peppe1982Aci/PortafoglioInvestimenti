from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QDoubleSpinBox,
    QDateEdit,
    QDialogButtonBox
)

from PySide6.QtCore import QDate


class DialogOperazione(QDialog):

    def __init__(self, parent=None, dati=None, ticker_list=None):
        super().__init__(parent)

        if dati is None:
            self.setWindowTitle("Nuova operazione")
        else:
            self.setWindowTitle("Modifica operazione")

        self.setMinimumWidth(450)

        layout = QVBoxLayout(self)

        form = QFormLayout()

        # ------------------------------------------
        # Data
        # ------------------------------------------

        self.data = QDateEdit()

        self.data.setCalendarPopup(True)

        self.data.setDisplayFormat("dd/MM/yyyy")

        self.data.setDate(QDate.currentDate())

        # ------------------------------------------
        # Ticker
        # ------------------------------------------

        self.ticker = QComboBox()

        if ticker_list:

            self.ticker.addItems(sorted(ticker_list))

        self.ticker.setEditable(True)

        # ------------------------------------------
        # Tipo
        # ------------------------------------------

        self.tipo = QComboBox()

        self.tipo.addItems([
            "Acquisto",
            "Vendita"
        ])

        # ------------------------------------------
        # Quantità
        # ------------------------------------------

        self.quantita = QDoubleSpinBox()

        self.quantita.setDecimals(6)

        self.quantita.setMaximum(100000000)

        # ------------------------------------------
        # Prezzo
        # ------------------------------------------

        self.prezzo = QDoubleSpinBox()

        self.prezzo.setDecimals(6)

        self.prezzo.setMaximum(1000000)

        self.prezzo.setSuffix(" €")

        # ------------------------------------------
        # Commissioni
        # ------------------------------------------

        self.commissioni = QDoubleSpinBox()

        self.commissioni.setDecimals(2)

        self.commissioni.setMaximum(100000)

        self.commissioni.setSuffix(" €")

        # ------------------------------------------
        # Cambio
        # ------------------------------------------

        self.cambio = QDoubleSpinBox()

        self.cambio.setDecimals(6)

        self.cambio.setValue(1)

        self.cambio.setMaximum(1000)

        # ------------------------------------------
        # Note
        # ------------------------------------------

        self.note = QTextEdit()

        self.note.setMaximumHeight(90)

        # ------------------------------------------
        # Layout
        # ------------------------------------------

        form.addRow("Data", self.data)

        form.addRow("Ticker", self.ticker)

        form.addRow("Tipo", self.tipo)

        form.addRow("Quantità", self.quantita)

        form.addRow("Prezzo", self.prezzo)

        form.addRow("Commissioni", self.commissioni)

        form.addRow("Cambio", self.cambio)

        form.addRow("Note", self.note)

        layout.addLayout(form)

        # ------------------------------------------
        # Carica dati
        # ------------------------------------------

        if dati is not None:

            self.data.setDate(
                QDate.fromString(
                    dati["data"],
                    "yyyy-MM-dd"
                )
            )

            indice = self.ticker.findText(
                dati["ticker"]
            )

            if indice >= 0:
                self.ticker.setCurrentIndex(indice)
            else:
                self.ticker.setCurrentText(
                    dati["ticker"]
                )

            indice = self.tipo.findText(
                dati["tipo"]
            )

            if indice >= 0:
                self.tipo.setCurrentIndex(indice)

            self.quantita.setValue(
                float(dati["quantita"])
            )

            self.prezzo.setValue(
                float(dati["prezzo"])
            )

            self.commissioni.setValue(
                float(dati["commissioni"])
            )

            self.cambio.setValue(
                float(dati["cambio"])
            )

            self.note.setPlainText(
                dati["note"]
            )

        # ------------------------------------------
        # Pulsanti
        # ------------------------------------------

        pulsanti = QDialogButtonBox(
            QDialogButtonBox.Ok |
            QDialogButtonBox.Cancel
        )

        pulsanti.accepted.connect(
            self.accept
        )

        pulsanti.rejected.connect(
            self.reject
        )

        layout.addWidget(pulsanti)

    # -------------------------------------------------

    def dati(self):

        return {

            "data": self.data.date().toString(
                "yyyy-MM-dd"
            ),

            "ticker": self.ticker.currentText().strip().upper(),

            "tipo": self.tipo.currentText(),

            "quantita": self.quantita.value(),

            "prezzo": self.prezzo.value(),

            "commissioni": self.commissioni.value(),

            "cambio": self.cambio.value(),

            "note": self.note.toPlainText().strip()

        }