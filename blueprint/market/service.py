from models.database import Exchange
import importlib

class Funding:
    def __init__(self):
        self.exchange = ""
        self.pairs = {}


    def addExchange(self, exchange):
        self.exchange = exchange

    def addPairs(self):
        self.pairs = getPairs(self.exchange)
        

def getExchanges():
    # exchanges = []
    # for ex in Exchange.query.all():
    #     exchanges.append(ex.as_dict()["name"])

    exchanges = ["binance", "coinbase"]

    return exchanges


def getPairs(exchange):
    exchanges = importlib.import_module(f"blueprint.market.exchange.{exchange}")
    return exchanges.getFunding()

    
if __name__ == "__main__":

    for exchange in getExchanges():
        funding = Funding()
        funding.addExchange(exchange)
        funding.addPairs()

        print(funding.pairs)
