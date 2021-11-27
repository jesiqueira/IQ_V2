from indicadores.indicadores import Indicadores
from trader.trader import Trader
from math import ceil
from time import sleep


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

    def entrada(self, candleAtual, timeAtual, smaRapida=7, smaLenta=100, qtdVelas=110):
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
        qtd_candle_p_max_min = 20

        # smaLenta = Indicador.sma(smaLenta)
        if candleAtual < smaRapida <smaLenta:
            # realizar venda ou PUT
            trader = Trader(self.api)
            # print(f'Minima close: {self.minima(candles)}')
            # if candles[-2]['open'] > candles[-2]['close'] > candles[-1]['min'] < self.minima(candles):
            print('put')
            # print(f'Open 2: {candles[-3]["open"]}')
            # print(f'close 2: {candles[-3]["close"]}')
            # print(f'Open 1: {candles[-2]["open"]}')
            # print(f'close 1: {candles[-2]["close"]}')
            print(f"Máxima: {self.maxima(qtd_candle_p_max_min, timeAtual)}")
            print(f"Minima: {self.minima(qtd_candle_p_max_min, timeAtual)}")
            print(f"candle[-1] {candles[-2]['close']}")
            if candleAtual < self.minima(qtd_candle_p_max_min, timeAtual):
                print('Esperando 7 segundos')
                sleep(7)
            # if candles[-2]['open'] > candles[-2]['close'] and candles[-1]['open'] > candles[-1]['close'] and candles[-1]['open'] < smaRapida > candles[-1]['close'] and candles[-1]['min'] < self.minima(candles):
            if candles[-3]['open'] > candles[-3]['close'] and candles[-2]['open'] > candles[-2]['close'] and candles[-1]['open'] < smaRapida \
                and candles[-1]['close'] < self.minima(qtd_candle_p_max_min, timeAtual) and candleAtual < candles[-2]['close'] \
                and candleAtual < self.minima(qtd_candle_p_max_min, timeAtual):
                print('Compra Efetuada')
                status, id = trader.put(1, self.par, 3)
                if status:
                    resutado, lucro = self.api.check_win_v3(id)
                    print(f'Resultado: {resutado}, lucro: {lucro}')
                    sleep(20)

        elif candleAtual > smaRapida > smaLenta:
            # Realizar compra ou CALL
            trader = Trader(self.api)
            # print(f'Max close: {self.maxima(candles)}')
            # if candles[-2]['open'] < candles[-2]['close'] < candles[-1]['max'] > self.maxima(candles):
            print('call')
            # print(f'Open 2: {candles[-3]["open"]}')
            # print(f'close 2: {candles[-3]["close"]}')
            # print(f'Open 1: {candles[-2]["open"]}')
            # print(f'close 1: {candles[-2]["close"]}')
            print(f"Máxima: {self.maxima(qtd_candle_p_max_min, timeAtual)}")
            print(f"Minima: {self.minima(qtd_candle_p_max_min, timeAtual)}")
            print(f"candle[-1] {candles[-2]['close']}")
            if candleAtual > self.maxima(qtd_candle_p_max_min, timeAtual):
                print('Esperando 7 segundos')
                sleep(7)
            # if candles[-2]['open'] < candles[-2]['close'] and candles[-1]['open'] < candles[-1]['close'] and candles[-1]['open'] > smaRapida < candles[-1]['close'] and candles[-1]['max'] > self.maxima(candles):
            if candles[-3]['open'] < candles[-3]['close'] and candles[-2]['open'] < candles[-2]['close'] and candles[-1]['open'] > smaRapida \
                and candles[-1]['close'] > self.maxima(qtd_candle_p_max_min, timeAtual) and candleAtual > candles[-2]['close'] \
                and candleAtual > self.maxima(qtd_candle_p_max_min, timeAtual):
                print('Compra Efetuada')
                status, id = trader.call(1, self.par, 3)
                if status:
                    resutado, lucro = self.api.check_win_v3(id)
                    print(f'Resultado: {resutado}, lucro: {lucro}')
                    sleep(20)
        else:
            print('Preço entre as médias')
            # print(f'Open 2: {candles[-3]["open"]}')
            # print(f'close 2: {candles[-3]["close"]}')
            # print(f'Open 1: {candles[-2]["open"]}')
            # print(f'close 1: {candles[-2]["close"]}')

    def maxima(self, qtd_velas, time_atual):
        candles = self.candles(qtd_velas, time_atual)
        maxima = []
        for candle in candles[ : -1]:
            maxima.append(candle['close'])
        return max(maxima)

    def minima(self, qtd_velas, time_atual):
        candles = self.candles(qtd_velas, time_atual)
        minima = []
        for candle in candles[ : -1]:
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
