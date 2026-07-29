from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QDialogButtonBox
)


class DialogStrumento(QDialog):

    def __init__(self, parent=None, dati=None):
        super().__init__(parent)

        self.dati_originali = dati

        self.setWindowTitle(
            "Nuovo strumento"
            if dati is None
            else "Modifica strumento"
        )

        self.setMinimumWidth(450)

        self.crea_interfaccia()

        if dati is not None:
            self.carica_dati()

    # --------------------------------------------------

    def crea_interfaccia(self):

        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.ticker = QLineEdit()
        self.nome = QLineEdit()

        self.quantita = QLineEdit()
        self.prezzo = QLineEdit()

        self.valuta = QComboBox()
        self.valuta.addItems([
            "EUR",
            "USD",
            "GBP",
            "CHF"
        ])

        self.settore = QLineEdit()

        self.note = QTextEdit()
        self.note.setMaximumHeight(90)

        form.addRow("Ticker", self.ticker)
        form.addRow("Nome", self.nome)
        form.addRow("Quantità", self.quantita)
        form.addRow("Prezzo medio", self.prezzo)
        form.addRow("Valuta", self.valuta)
        form.addRow("Settore", self.settore)
        form.addRow("Note", self.note)

        layout.addLayout(form)

        pulsanti = QDialogButtonBox(
            QDialogButtonBox.Ok |
            QDialogButtonBox.Cancel
        )

        pulsanti.accepted.connect(self.accept)
        pulsanti.rejected.connect(self.reject)

        layout.addWidget(pulsanti)

    # --------------------------------------------------

    def carica_dati(self):

        d = self.dati_originali

        self.ticker.setText(str(d["ticker"]))
        self.nome.setText(str(d["nome"]))
        self.quantita.setText(str(d["quantita"]))
        self.prezzo.setText(str(d["prezzo_medio"]))

        indice = self.valuta.findText(str(d["valuta"]))

        if indice >= 0:
            self.valuta.setCurrentIndex(indice)

        self.settore.setText(str(d["settore"]))
        self.note.setPlainText(str(d["note"]))

    # --------------------------------------------------

    def dati(self):

        return {

            "ticker": self.ticker.text().strip().upper(),

            "nome": self.nome.text().strip(),

            "quantita": self.quantita.text().replace(",", "."),

            "prezzo": self.prezzo.text().replace(",", "."),

            "valuta": self.valuta.currentText(),

            "settore": self.settore.text().strip(),

            "note": self.note.toPlainText().strip()

        }