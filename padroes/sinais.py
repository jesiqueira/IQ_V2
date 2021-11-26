from typing import Match
from indicadores.indicadores import Indicadores
from trader.trader import Trader
from math import ceil


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

        # smaLenta = Indicador.sma(smaLenta)
        if candleAtual < smaRapida:
            # realizar venda ou PUT
            trader = Trader(self.api)
            print('put')
            # print(candles[-2]['close'])
            # print(candles)
            # print(f'Minima close: {self.minima(candles)}')
            # if candles[-2]['open'] > candles[-2]['close'] > candles[-1]['min'] < self.minima(candles):
            if candles[-2]['open'] > candles[-2]['close'] > candles[-1]['min'] and self.tendenciaAlta(candles):
                status, id = trader.put(1, self.par, 5)
                if status:
                    resutado, lucro = self.api.check_win_v3(id)
                    print(f'Resultado: {resutado}, lucro: {lucro}')

        elif candleAtual > smaRapida > smaLenta:
            # Realizar compra ou CALL
            # print(candles[-2])
            trader = Trader(self.api)
            print('call')
            # print(candles[-2]['close'])
            # print(candles)
            # print(f'Max close: {self.maxima(candles)}')
            if candles[-2]['open'] < candles[-2]['close'] < candles[-1]['max'] > self.maxima(candles):
                status, id = trader.call(1, self.par, 5)
                if status:
                    resutado, lucro = self.api.check_win_v3(id)
                    print(f'Resultado: {resutado}, lucro: {lucro}')
        else:
            print('Preço entre as médias')

    def maxima(self, candles):
        maxima = []
        for candle in candles[: -1]:
            maxima.append(candle['close'])
        return max(maxima)

    def minima(self, candles):
        minima = []
        for candle in candles[: -1]:
            minima.append(candle['close'])
        return min(minima)

    def barraElefante(self, candles):
        _close = candles[-2]['close']
        _open = candles[-2]['open']
        print(f'close: {_close}')
        print(f'open: {_open}')
        tamanho = abs(candles[-2]['close'] - candles[-2]['open'])
        print(f'tamanho: {tamanho}')
        print(f'tamanho: {ceil(tamanho)}')

    def tendenciaAlta(self, candles, sma):
        if candles[-2]['open'] < candles[-2]['close'] and candles[-2]['min'] > sma < candles[-2]['close']:
            return True

    def tendenciaBaixa(elf, candles, sma):
        if candles[-2]['open'] > candles[-2]['close'] and candles[-2]['min'] < sma > candles[-2]['close']:
            return True
