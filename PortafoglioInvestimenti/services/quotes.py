"""
services/quotes.py

Gestione quotazioni strumenti finanziari.

Versione iniziale (Sprint 2.3.1).

Le funzioni sono già predisposte per essere collegate
ad un provider dati (es. Yahoo Finance, AlphaVantage,
TwelveData ecc.).

Per il momento restituiscono dati simulati così tutta
l'applicazione può essere sviluppata senza dipendere
da Internet.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import random


@dataclass
class Quote:

    symbol: str
    price: float
    previous_close: float
    currency: str
    timestamp: datetime

    @property
    def variation(self):

        if self.previous_close == 0:
            return 0.0

        return (
            (self.price - self.previous_close)
            / self.previous_close
            * 100
        )


class QuoteService:

    def __init__(self):

        self._cache = {}

    def get_quote(self, symbol: str) -> Quote:

        symbol = symbol.upper()

        if symbol in self._cache:
            return self._cache[symbol]

        base = random.uniform(20, 300)

        quote = Quote(
            symbol=symbol,
            price=round(base, 2),
            previous_close=round(base * random.uniform(0.98, 1.02), 2),
            currency="EUR",
            timestamp=datetime.now(),
        )

        self._cache[symbol] = quote

        return quote

    def refresh_quote(self, symbol: str):

        self._cache.pop(symbol.upper(), None)

        return self.get_quote(symbol)

    def refresh_all(self, symbols):

        quotes = {}

        for symbol in symbols:
            quotes[symbol] = self.refresh_quote(symbol)

        return quotes

    def clear_cache(self):

        self._cache.clear()