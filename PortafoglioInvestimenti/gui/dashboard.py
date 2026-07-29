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


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        self.crea_interfaccia()

        self.refresh()

    # --------------------------------------------------

    def crea_interfaccia(self):

        layout = QVBoxLayout(self)

        titolo = QLabel("Dashboard")

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

        griglia.addWidget(
            self.crea_card(
                "Strumenti",
                self.lblStrumenti
            ),
            0,
            0
        )

        griglia.addWidget(
            self.crea_card(
                "Operazioni",
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
                "Performance",
                self.lblPerformance
            ),
            2,
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

        gain = valore - investito

        rendimento = 0.0

        if investito > 0:

            rendimento = (gain / investito) * 100

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

    # --------------------------------------------------

    def aggiorna(self):

        self.refresh()