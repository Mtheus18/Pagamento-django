from django.conf import settings
import requests
from datetime import datetime


URL = "https://api.cieloecommerce.cielo.com.br/1/sales"

def buscar_pagamentos_cielo():

    headers = {
        "MerchantID": settings.CIELO_MERCHANT_ID,
        "MerchantKey": settings.CIELO_MERCHANT_KEY,
        "Content-Type": "application/json"
    }

    response = requests.get(URL, headers=headers)

    if response.status_code == 200:
        pagamentos = response.json()

        hoje = datetime.now().date()

        pagamentos_hoje = []

        for p in pagamentos:

            data = p.get("Payment", {}).get("ReceiveDate")

            if data:
                data_pagamento = datetime.fromisoformat(data).date()

                if data_pagamento == hoje:
                    pagamentos_hoje.append(p)

        return pagamentos_hoje

    return []
