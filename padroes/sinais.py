from os import path
from indicadores.indicadores import Indicadores


class Sinais:

    def __init__(self, par, api, timeframe):
        self.par = par
        self.api = api
        self.timeframe = timeframe

    def candles(self, qtdVelas, timeAtual):
        ''' 
            Pegar histórico dos candles
            Par = moeda negociada;
            timeframe = o time frame das velas em segundos 60 segundos igual 1 minuto;
            qtdVelas = quantidade de velas a carregar;
            realtime = é o minuto corrente em timestamp => time.time();
        '''
        return self.api.get_candles(self.par, self.timeframe, qtdVelas, timeAtual)
        # print(candle[-2]['close'])

    def entrada(self, candleAtual, timeAtual, smaRapida=9, smaLenta=34, qtdVelas=50):
        '''
            Recebe os parametros e verifica se atende os padões de entrada;
            candleAtual -> Ultimo clandle;
            timeAtual -> ultimo time ou minuto atual, time.time()
            sma... -> para calcula a média
            qtdVelas = quantas velas vão ser carregadas no histórico
        '''
        candles = self.candles(qtdVelas, timeAtual)
        Indicador = Indicadores(candles)
        smaRapida = Indicador.sma(smaRapida)
        smaLenta = Indicador.sma(smaLenta)
        if candleAtual < smaRapida < smaLenta:
            # realizar venda ou PUT
            print('put')
        elif candleAtual > smaRapida > smaLenta:
            # Realizar compra ou CALL
            # print(candles[-2])
            print(candles[-2]['close'])
            maior = []
            for candle in candles[-50 : -2]:
                maior.append(candle['close'])
                # print(f"vela: {n}, maxima: {l['close']}")
            ma = max(maior)
            print(f'Max close: {ma}')
        else:
            print('Preço entre as médias')