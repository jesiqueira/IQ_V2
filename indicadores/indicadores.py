
class Indicadores:
    def __init__(self, candles):
        self.candle = candles

    def sma(self, periodo) -> float:
        """Calcular SMA de n período, deve receber um array de candle e um pediodo"""
        # df = pd.DataFrame(self.candle).sort_index(ascending=False)
        close = []
        for i in range(1, periodo + 1):
            close.append(self.candle[-i]['close'])

        return sum(close) / periodo

    def ema(self, periodo) -> float:
        """Calcular EMA de n período, deve receber um array de candle e um pediodo"""
        close = []
        for i in range(1, periodo + 1):
            close.append(self.candle[-i]['close'])

        sma = sum(close) / periodo
        print(close)
        return (2 / (periodo + 1)) * (self.candle[-1]['close'] - sma) + sma
