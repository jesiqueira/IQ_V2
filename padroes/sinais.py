from indicadores.indicadores import Indicadores

class Sinais:
    
    def __init__(self, api):
        self.api = api
    
    def candles(self, par, timeframe, qtdVelas, realtime):
        ''' 
            Par = moeda negociada;
            timeframe = o time frame das velas em segundos 60 segundos igual 1 minuto;
            qtdVelas = quantidade de velas a carregar;
            realtime = é o minuto corrente em timestamp;
        '''
        return self.api.get_candles(par, timeframe, qtdVelas, realtime)
        # print(candle[-2]['close'])

    
    def entrada(self, smaRapida, smaLenta, candleAtual):
        if candleAtual < smaRapida < smaLenta:
            print('put') 
        elif candleAtual > smaRapida > smaLenta:
            print('call')

        

