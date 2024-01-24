from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.test import EMA


class EMACross(Strategy):
    fast = 13
    slow = 26

    def init(self):
        close = self.data.Close
        self.ema_fast = self.I(EMA, close, self.fast)
        self.ema_slow = self.I(EMA, close, self.slow)

    def next(self):
        if crossover(self.ema_fast, self.ema_slow):
            self.buy()
        elif crossover(self.ema_slow, self.ema_fast):
            self.sell()
