from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QGroupBox,
    QPushButton
)

from PySide6.QtCore import Qt

from database import (
    numero_operazioni,
    totale_commissioni
)

from services.portfolio_service import PortfolioService


class Dashboard(QWidget):

    def __init__(self):

        super().__init__()

        self.service = PortfolioService()

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


        self.btnAggiorna = QPushButton(
            "Aggiorna quotazioni"
        )

        self.btnAggiorna.clicked.connect(
            self.aggiorna_quotazioni
        )

        layout.addWidget(
            self.btnAggiorna
        )


        griglia = QGridLayout()


        self.lblStrumenti = QLabel()
        self.lblOperazioni = QLabel()
        self.lblInvestito = QLabel()
        self.lblValore = QLabel()
        self.lblCommissioni = QLabel()
        self.lblPerformance = QLabel()
        self.lblMigliore = QLabel()
        self.lblPeggiore = QLabel()


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
        griglia.addWidget(
            self.crea_card(
                "Migliore posizione",
                self.lblMigliore
            ),
            3,
            0
        )


        griglia.addWidget(
            self.crea_card(
                "Peggiore posizione",
                self.lblPeggiore
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

        label.setAlignment(
            Qt.AlignCenter
        )

        label.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
            padding:20px;
        """)

        layout.addWidget(label)

        return box


    # --------------------------------------------------

    def refresh(self):

        riepilogo = self.service.riepilogo()


        self.lblStrumenti.setText(
            str(riepilogo["positions"])
        )


        self.lblOperazioni.setText(
            str(numero_operazioni())
        )


        self.lblInvestito.setText(
            f'{riepilogo["invested"]:,.2f} €'
        )


        self.lblValore.setText(
            f'{riepilogo["market_value"]:,.2f} €'
        )


        self.lblCommissioni.setText(
            f'{totale_commissioni():,.2f} €'
        )


        self.lblPerformance.setText(
            f'{riepilogo["gain"]:,.2f} €\n'
            f'({riepilogo["gain_percent"]:,.2f}%)'
        )


        migliore = self.service.engine.best_position()

        peggiore = self.service.engine.worst_position()


        if migliore:

            self.lblMigliore.setText(
                f"{migliore.ticker}\n"
                f"{migliore.gain_percent:,.2f}%"
            )

        else:

            self.lblMigliore.setText("-")


        if peggiore:

            self.lblPeggiore.setText(
                f"{peggiore.ticker}\n"
                f"{peggiore.gain_percent:,.2f}%"
            )

        else:

            self.lblPeggiore.setText("-")


    # --------------------------------------------------

    def aggiorna_quotazioni(self):

        self.service.aggiorna_quotazioni()

        self.refresh()


    # --------------------------------------------------

    def aggiorna(self):

        self.refresh()
