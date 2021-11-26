from io import BufferedReader
from iqoptionapi.stable_api import IQ_Option
from config import Config
import time
from padroes.sinais import Sinais
from indicadores.indicadores import Indicadores
import json


# PRACTICE / REAL
api = IQ_Option(Config.LOGIN, Config.PASSWORD, active_account_type='PRACTICE')

PAR = 'EURUSD-OTC'
# PAR = 'EURUSD'
ENTRADA = 'call'  # put/call
TIMEFRAME = 60  # time em segunddo, 60 segundo igual 1 minuto

api.connect()

if api.check_connect():
    print('Conectado com sucesso')
else:
    print('Falha na conexão verificar login/senha')

# status, id = api.buy(1, ATIVO, ENTRADA, 1)

# if status:
#     print(f'Entrada realzada com sucesso {ATIVO}')
# else:
#     print('Falha ao abrir operação')

# candle = api.full_realtime_get_candle(ATIVO, TIMEFRAME, 50)
# time.sleep(10)


# candle = api.get_candles(PAR, TIMEFRAME, 10, time.time())
# print(candle[-2]['close'])
sinais = Sinais(PAR, api, TIMEFRAME)
# candles = sinais.candles(api, PAR, TIMEFRAME, 50, time.time())
# indicador = Indicadores(candles)
# print(f'SMA9: {indicador.sma(9)}')
# print(f'SMA25: {indicador.sma(25)}')


# Pegar velas em tempo real #########################


# while True:
# vela = api.get_realtime_candles(PAR, 60)
# candles = sinais.candles(PAR, TIMEFRAME, 50, time.time())
# indicador = Indicadores(candles)
# smaRapida = indicador.sma(9)
# smaLenta = indicador.sma(25)
# for velas in vela:
#     try:
#     # print(f'smaRapida: {smaRapida}')
#     # print(f'smaLenta: {smaLenta}')
#     # print(vela[velas]['close'])
#     	sinais.entrada(smaRapida, smaLenta, vela[velas]['close'])
#     except RuntimeError:
#         print('Erro')

# time.sleep(1)
# print(api.get_positions)

api.start_candles_stream(PAR, 60, 1)
time.sleep(1)
while True:
    with open('startStop.json', 'r') as file:
        data = json.load(file)
        if not int(data['ligado']):
            break
        else:
            try:
                vela = api.get_realtime_candles(PAR, 60)
                # candles = sinais.candles(50, time.time())
                # indicador = Indicadores(candles)
                # smaRapida = indicador.sma(9)
                # smaLenta = indicador.sma(25)

                for velas in vela:
                    try:
                        # print(f'smaRapida: {smaRapida}')
                        # print(f'smaLenta: {smaLenta}')
                        # print(vela[velas]['close'])
                        # sinais.entrada(smaRapida, smaLenta, vela[velas]['close'])
                        # sinais.entrada(PAR, vela[velas]['close'], time.time())
                        sinais.entrada(vela[velas]['close'], time.time())
                    except RuntimeError:
                        print('Erro')
            except RuntimeError:
                pass
api.stop_candles_stream(PAR, 60)
