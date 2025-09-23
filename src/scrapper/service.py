import requests
from bs4 import BeautifulSoup


def getBcvTasa():
    url = "https://www.bcv.org.ve"
    try:
        response = requests.get(url, verify=False, timeout=10)
        if response.status_code != 200:
            return {
                "msg": f"Failed to retrieve data from BCV, response status {response.status}",
                "error": True,
            }

        soup = BeautifulSoup(response.content, "html.parser")
        elementDollarTasa = soup.find("div", id="dolar")
        amountDollarTasa = elementDollarTasa.find("strong")
        return {
            "price": f"{amountDollarTasa.get_text(strip=True)}",
            "error": False,
            "msg": "",
        }
    except Exception as e:
        return {"msg": str(e), "error": True}


def getBinanceTasa():
    url = "https://p2p.binance.com/bapi/c2c/v2/public/c2c/adv/quoted-price"
    payload = {
        "assets": ["USDT"],
        "fiatCurrency": "VES",
        "tradeType": "SELL",
        "fromUserRole": "USER",
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()
        if data["success"] is False:
            return {
                "msg": f"Failed to retrieve data from Binance. Error msg: {data['message']}",
                "error": True,
            }
        return {
            "price": f"{data['data'][0]['referencePrice']}",
            "msg": "",
            "error": False,
        }
    except Exception as e:
        return {"msg": str(e), "error": True}

def getBinanceTasaV2():
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    payload = {
       "additionalKycVerifyFilter": 0,
       "asset": "USDT",
       "classifies": ["mass", "profession", "fiat_trade"],
       "countries": [],
       "fiat": "VES",
       "filterType": "all",
       "followed": False,
       "page": 1,
       "payTypes": [],
       "periods": [],
       "proMerchantAds": False,
       "publisherType": "merchant",
       "rows": 2,
       "shieldMerchantAds": False,
       "tradeType": "BUY",
       "tradedWith": False
    }
    try:
        response = requests.post(url, json=payload,  timeout=10)
        data=response.json()
        if data["success"] is False:
            return {
                "msg": f"Failed to retrieve data from Binance. Error msg: {data['message']}",
                "error": True,
            }
        return {
            "price": f"{data['data'][1]['adv']['price']}",
            "msg": "",
            "error": False,
        }

    except Exception as e:
        return {"msg": str(e), "error": True}

   