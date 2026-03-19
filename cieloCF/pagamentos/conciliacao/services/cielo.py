from django.conf import settings
import requests

URL = "https://api.cieloecommerce.cielo.com.br/1/sales"


def buscar_pagamentos_cielo():
    headers = {
        "MerchantID": settings.CIELO_MERCHANT_ID,
        "MerchantKey": settings.CIELO_MERCHANT_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(URL, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return []
