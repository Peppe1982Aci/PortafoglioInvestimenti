"""
Motore di calcolo del portafoglio.

Tutta la logica finanziaria verrà spostata qui,
lasciando il database come semplice livello dati.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Position:

    ticker: str
    quantity: float
    average_price: float
    current_price: float = 0.0

    @property
    def invested(self) -> float:
        return self.quantity * self.average_price

    @property
    def market_value(self) -> float:
        return self.quantity * self.current_price

    @property
    def gain(self) -> float:
        return self.market_value - self.invested

    @property
    def gain_percent(self) -> float:

        if self.invested == 0:
            return 0.0

        return (self.gain / self.invested) * 100


class PortfolioEngine:

    def __init__(self):

        self.positions: List[Position] = []

    def clear(self):

        self.positions.clear()

    def add_position(
        self,
        ticker,
        quantity,
        average_price,
        current_price
    ):

        self.positions.append(

            Position(
                ticker=ticker,
                quantity=float(quantity),
                average_price=float(average_price),
                current_price=float(current_price),
            )

        )

    @property
    def invested(self):

        return sum(
            p.invested
            for p in self.positions
        )

    @property
    def market_value(self):

        return sum(
            p.market_value
            for p in self.positions
        )

    @property
    def gain(self):

        return self.market_value - self.invested

    @property
    def gain_percent(self):

        if self.invested == 0:
            return 0.0

        return self.gain / self.invested * 100

    def weight(self, ticker):

        totale = self.market_value

        if totale == 0:
            return 0.0

        for posizione in self.positions:

            if posizione.ticker == ticker:

                return (
                    posizione.market_value
                    / totale
                    * 100
                )

        return 0.0

    def best_position(self):

        if not self.positions:
            return None

        return max(
            self.positions,
            key=lambda p: p.gain_percent
        )

    def worst_position(self):

        if not self.positions:
            return None

        return min(
            self.positions,
            key=lambda p: p.gain_percent
        )

    def summary(self):

        return {
            "positions": len(self.positions),
            "invested": self.invested,
            "market_value": self.market_value,
            "gain": self.gain,
            "gain_percent": self.gain_percent,
        }