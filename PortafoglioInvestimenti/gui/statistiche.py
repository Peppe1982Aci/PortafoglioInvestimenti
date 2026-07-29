from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QGroupBox
)

from PySide6.QtCore import Qt

from database import (
    numero_strumenti,
    numero_operazioni,
    valore_portafoglio,
    capitale_investito,
    totale_commissioni
)


class Statistiche(QWidget):

    def __init__(self):
        super().__init__()

        self.crea_interfaccia()

        self.refresh()

    # --------------------------------------------------

    def crea_interfaccia(self):

        layout = QVBoxLayout(self)

        titolo = QLabel("Statistiche")

        titolo.setAlignment(Qt.AlignLeft)

        titolo.setStyleSheet("""

            font-size:26px;

            font-weight:bold;

            padding:8px;

        """)

        layout.addWidget(titolo)

        griglia = QGridLayout()

        self.lblStrumenti = QLabel()

        self.lblOperazioni = QLabel()

        self.lblInvestito = QLabel()

        self.lblValore = QLabel()

        self.lblCommissioni = QLabel()

        self.lblPerformance = QLabel()

        self.lblProfitto = QLabel()

        self.lblMedia = QLabel()

        griglia.addWidget(
            self.crea_card(
                "Numero Strumenti",
                self.lblStrumenti
            ),
            0,
            0
        )

        griglia.addWidget(
            self.crea_card(
                "Numero Operazioni",
                self.lblOperazioni
            ),
            0,
            1
        )

        griglia.addWidget(
            self.crea_card(
                "Capitale Investito",
                self.lblInvestito
            ),
            1,
            0
        )

        griglia.addWidget(
            self.crea_card(
                "Valore Portafoglio",
                self.lblValore
            ),
            1,
            1
        )

        griglia.addWidget(
            self.crea_card(
                "Commissioni",
                self.lblCommissioni
            ),
            2,
            0
        )

        griglia.addWidget(
            self.crea_card(
                "Performance %",
                self.lblPerformance
            ),
            2,
            1
        )

        griglia.addWidget(
            self.crea_card(
                "Profitto / Perdita",
                self.lblProfitto
            ),
            3,
            0
        )

        griglia.addWidget(
            self.crea_card(
                "Investimento Medio",
                self.lblMedia
            ),
            3,
            1
        )

        layout.addLayout(griglia)

        layout.addStretch()

    # --------------------------------------------------

    def crea_card(self, titolo, label):

        box = QGroupBox(titolo)

        layout = QVBoxLayout(box)

        label.setAlignment(Qt.AlignCenter)

        label.setStyleSheet("""

            font-size:22px;

            font-weight:bold;

            color:#1565C0;

            padding:20px;

        """)

        layout.addWidget(label)

        return box

    # --------------------------------------------------

    def refresh(self):

        strumenti = numero_strumenti()

        operazioni = numero_operazioni()

        investito = capitale_investito()

        valore = valore_portafoglio()

        commissioni = totale_commissioni()

        profitto = valore - investito

        if investito > 0:

            rendimento = (profitto / investito) * 100

        else:

            rendimento = 0

        if strumenti > 0:

            medio = investito / strumenti

        else:

            medio = 0

        self.lblStrumenti.setText(
            str(strumenti)
        )

        self.lblOperazioni.setText(
            str(operazioni)
        )

        self.lblInvestito.setText(
            f"{investito:,.2f} €"
        )

        self.lblValore.setText(
            f"{valore:,.2f} €"
        )

        self.lblCommissioni.setText(
            f"{commissioni:,.2f} €"
        )

        self.lblPerformance.setText(
            f"{rendimento:,.2f} %"
        )

        if profitto >= 0:

            self.lblProfitto.setStyleSheet("""

                font-size:22px;

                font-weight:bold;

                color:green;

                padding:20px;

            """)

        else:

            self.lblProfitto.setStyleSheet("""

                font-size:22px;

                font-weight:bold;

                color:red;

                padding:20px;

            """)

        self.lblProfitto.setText(
            f"{profitto:,.2f} €"
        )

        self.lblMedia.setText(
            f"{medio:,.2f} €"
        )

    # --------------------------------------------------

    def aggiorna(self):

        self.refresh()

    # --------------------------------------------------

    def clear(self):

        self.lblStrumenti.setText("0")

        self.lblOperazioni.setText("0")

        self.lblInvestito.setText("0,00 €")

        self.lblValore.setText("0,00 €")

        self.lblCommissioni.setText("0,00 €")

        self.lblPerformance.setText("0,00 %")

        self.lblProfitto.setText("0,00 €")

        self.lblMedia.setText("0,00 €")