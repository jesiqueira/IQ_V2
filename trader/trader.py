class Trader:
    def __init__(self, api):
        self.api = api

    def put(self, valor, ativo, timeExperideEntrada):
        return self.api.buy(valor, ativo, 'put', timeExperideEntrada)

    def call(self, valor, ativo, timeExperideEntrada):
        return self.api.buy(valor, ativo, 'call', timeExperideEntrada)
