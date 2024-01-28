from backtesting.backtesting import Strategy
from backtesting.lib import crossover
import pandas_ta
import talib


class RSIReversion(Strategy):
    def init(self):
        self.rsi = self.I(pandas_ta.rsi, self.data.df.Close, 14)

    def next(self):
        print(self.rsi[0])
        if crossover(self.rsi, 70):
            self.buy()
        elif crossover(30, self.rsi):
            self.sell()


class MACDCross(Strategy):
    fast_window = 12
    slow_window = 26

    def init(self):
        close = self.data.df.Close
        self.macd_fast = self.I(pandas_ta.macd, close, self.fast_window)
        self.macd_slow = self.I(pandas_ta.macd, close, self.slow_window)

    def next(self):
        if crossover(self.macd_fast, self.macd_slow):
            self.buy()
        elif crossover(self.macd_slow, self.macd_fast):
            self.sell()


class VWAPCross(Strategy):
    ema_window = 5
    sl = 0.01
    tp = 0.05

    def init(self):
        df = self.data.df
        self.vwap = self.I(pandas_ta.vwap, df.High, df.Low, df.Close, df.Volume)
        self.ema = self.I(talib.EMA, df.Close, self.ema_window)

    def next(self):
        close = self.data.Close
        if crossover(self.ema, self.vwap):
            self.buy(sl=close * (1 - self.sl), tp=close * (1 + self.tp))
        elif crossover(self.vwap, self.ema):
            self.sell(sl=close * (1 + self.sl), tp=close * (1 - self.tp))


class EMACross(Strategy):
    fast_window = 25
    slow_window = 50

    def init(self):
        close = self.data.Close
        self.ema_fast = self.I(talib.EMA, close, self.fast_window)
        self.ema_slow = self.I(talib.EMA, close, self.slow_window)

    def next(self):
        if self.position:
            if (self.position.is_long and crossover(self.ema_slow, self.ema_fast)) or (
                self.position.is_short and crossover(self.ema_fast, self.ema_slow)
            ):
                self.position.close()
        if crossover(self.ema_fast, self.ema_slow):
            self.buy()
        elif crossover(self.ema_slow, self.ema_fast):
            self.sell()


class BBandReversion(Strategy):
    band_window = 50

    def init(self):
        df = self.data.df
        self.bband = self.I(pandas_ta.bbands, df.Close, self.band_window)
        self.lower = self.bband[0]
        self.mid = self.bband[1]
        self.upper = self.bband[2]

    def next(self):
        close = self.data.Close
        if crossover(close, self.upper):
            self.buy()
        elif crossover(self.lower, close):
            self.sell()


class SupertrendStrategy(Strategy):
    def supertrend(self, df, length):
        supertrend = pandas_ta.supertrend(df.High, df.Low, df.Close, length=length)
        return supertrend.to_numpy().T[1]

    def init(self):
        df = self.data.df
        self.dir = self.I(self.supertrend, df, 10)

    def next(self):
        if self.dir[-1] * self.dir[-2] > 0:
            return

        if self.dir[-1] > 0:
            self.buy()
        elif self.dir[-1] < 0:
            self.sell()
