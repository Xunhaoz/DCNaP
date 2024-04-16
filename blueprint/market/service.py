import requests
import json

import exchange.binance




def main():
    binanceList = exchange.binance.getList()

    result = {
        "binance": binanceList,
    }

    return result



if __name__ == "__main__":
    main()
