from database import leggi_strumenti

from services.portfolio_engine import PortfolioEngine
from services.quotes import QuoteService


class PortfolioService:

    def __init__(self):

        self.engine = PortfolioEngine()

        self.quotes = QuoteService()


    # --------------------------------------------------

    def carica_portafoglio(self):

        self.engine.clear()

        strumenti = leggi_strumenti()

        for s in strumenti:

            quota = self.quotes.get_quote(
                s["ticker"]
            )

            self.engine.add_position(

                s["ticker"],

                s["quantita"],

                s["prezzo_medio"],

                quota.price

            )

        return self.engine


    # --------------------------------------------------

    def aggiorna_quotazioni(self):

        strumenti = leggi_strumenti()

        risultati = []

        for s in strumenti:

            quota = self.quotes.refresh_quote(
                s["ticker"]
            )

            risultati.append(quota)

        self.carica_portafoglio()

        return risultati


    # --------------------------------------------------

    def valore_portafoglio(self):

        self.carica_portafoglio()

        return self.engine.market_value


    # --------------------------------------------------

    def rendimento(self):

        self.carica_portafoglio()

        return {

            "gain": self.engine.gain,

            "gain_percent": self.engine.gain_percent

        }


    # --------------------------------------------------

    def riepilogo(self):

        self.carica_portafoglio()

        return self.engine.summary()
