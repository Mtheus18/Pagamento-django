from django.conf import settings
import requests


URL = "https://api.cieloecommerce.cielo.com.br/1/sales"

def buscar_pagamentos_cielo():

    headers = {
        "MerchantID": settings.CIELO_MERCHANT_ID,
        "MerchantKey": settings.CIELO_MERCHANT_KEY,
        "Content-Type": "application/json"
    }

    response = requests.get(URL, headers=headers)

    if response.status_code == 200:
        return response.json()

    return []
