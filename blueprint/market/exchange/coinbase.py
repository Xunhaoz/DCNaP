#'https://www.coinbase.com/unauthed/api/v3/brokerage/products?product_type=FUTURE&contract_expiry_type=PERPETUAL&product_venue=FCM'

import requests
import json

def getFunding():
    url = "https://www.coinbase.com/unauthed/api/v3/brokerage/products?product_type=FUTURE&contract_expiry_type=PERPETUAL"

    response = requests.get(url)
    parsed_response = json.loads(response.text)


    # print(json.dumps(parsed_response["products"], indent=4))


    # print(parsed_response["products"][0]["future_product_details"]["perpetual_details"]["funding_rate"])

    result = {str(pair["future_product_details"]["contract_code"]+pair["quote_name"]):"{:.4f}".format(eval(pair["future_product_details"]["perpetual_details"]["funding_rate"])*100) for pair in parsed_response["products"]}

    sorted_result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))

    print(sorted_result)


    # return sorted_result

if __name__ == "__main__":
    getFunding()



