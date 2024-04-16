import requests
import json

import exchange.binance
import exchange.coinbase



def main():
    binanceList = exchange.binance.getFunding()
    coinbaseList = exchange.coinbase.getFunding()


    result = {
        "binance": binanceList,
        "coinbase": coinbaseList,
    }

    print(result)
    return result



if __name__ == "__main__":
    main()
