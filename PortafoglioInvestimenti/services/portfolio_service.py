from database import leggi_strumenti

from services.portfolio_engine import PortfolioEngine
from services.quotes import QuoteService


class PortfolioService:

    def __init__(self):
        self.engine = PortfolioEngine()
        self.quotes = QuoteService()

    def carica_portafoglio(self):

        self.engine.clear()

        for s in leggi_strumenti():

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

    def riepilogo(self):

        self.carica_portafoglio()

        return self.engine.summary()
