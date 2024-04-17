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
    
    spots = getSpot()
    sorted_result_filtered = {key:value for key, value in sorted_result.items() if key in spots}

    # print(sorted_result_filtered)


    return sorted_result_filtered


def getSpot():
    # "https://api.binance.com/api/v3/exchangeInfo"
    
    url = "https://api.binance.com/api/v3/exchangeInfo"
    response = requests.get(url)

    parsed_response = json.loads(response.text)

    pairs = [pair["symbol"] for pair in parsed_response["symbols"]]

    return pairs
    


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


