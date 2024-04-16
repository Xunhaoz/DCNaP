import requests
import json



def getFunding():
    # https://www.binance.com/fapi/v1/premiumIndex?symbol=BTCUSDT
    url = "https://www.binance.com/fapi/v1/premiumIndex"

    # symbols = getSymbol()
    #
    # result = {}
    # for symbol in symbols:
    #
    #     try:
    #         response = requests.get(url+ "?symbol=" + symbol)
    #         # print(json.dumps(json.loads(response.text), indent=4))
    #
    #         fundingRate = json.loads(response.text)["lastFundingRate"]
    #         result[symbol] = fundingRate
    #     except Exception:
    #         pass
    #
    # print(result)

    response = requests.get(url)

    parsed_response = json.loads(response.text)

    result = {pair["symbol"]:eval(pair["lastFundingRate"])*100 for pair in parsed_response}
    sorted_result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
    print(sorted_result)

    return sorted_result

def getSymbol():
    # https://www.binance.com/bapi/futures/v1/public/future/common/symbol-config-info

    # curl 'https://www.binance.com/bapi/futures/v1/public/future/common/symbol-config-info' -X POST -H 'Content-Type: application/json' --data-raw '{}'
    
    url = "https://www.binance.com/bapi/futures/v1/public/future/common/symbol-config-info"
    headers = {"Content-Type": "application/json"}
    data = {}
    response = requests.post(url=url, json=data, headers=headers) 

    parsed_response = json.loads(response.text)
    
    # print(json.dumps(parsed_response, indent=4j)
    symbol_list = [pair_info["symbol"] for pair_info in parsed_response["data"]["configInfoList"]]
    
    return symbol_list


if __name__ == "__main__":
    getFunding()


