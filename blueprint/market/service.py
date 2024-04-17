from models.database import User, db


import blueprint.market.exchange.binance
import blueprint.market.exchange.coinbase



def main():
    binanceList = exchange.binance.getFunding()
    coinbaseList = exchange.coinbase.getFunding()


    result = {
        "binance": binanceList,
        "coinbase": coinbaseList,
    }

    print(result)
    return result

def getExchanges():
    
    return 



if __name__ == "__main__":
    main()
