from django.conf import settings
import requests
from datetime import datetime, timedelta
from dateutil import parser
from collections import defaultdict

URL = "https://api.cieloecommerce.cielo.com.br/1/sales"

STATUS_PAGO = 2


def buscar_pagamentos_cielo():
    headers = {
        "MerchantID": settings.CIELO_MERCHANT_ID,
        "MerchantKey": settings.CIELO_MERCHANT_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(URL, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return []

    pagamentos = response.json()
    hoje = datetime.now().date()

    pagamentos_hoje = []

    for p in pagamentos:
        data = p.get("Payment", {}).get("ReceiveDate")

        if not data:
            continue

        try:
            data_pagamento = parser.parse(data).date()
        except Exception:
            continue

        if data_pagamento == hoje:
            pagamentos_hoje.append(p)

    return pagamentos_hoje


def extrair_dados_pagamento(pagamento):

    payment = pagamento.get("Payment", {})

    transacao = payment.get("PaymentId")
    if not transacao:
        return None

    amount = payment.get("Amount") or 0
    valor = round(amount / 100, 2)

    status = payment.get("Status")
    nome = payment.get("Name")

    cartao = payment.get("CreditCard", {})
    numero_cartao = cartao.get("CardNumber")

    return {
        "transacao": transacao,
        "nome": nome,
        "valor": valor,
        "status": status,
        "data": payment.get("ReceiveDate"),
        "data_obj": parser.parse(payment.get("ReceiveDate")) if payment.get("ReceiveDate") else None,
        "cartao_final": numero_cartao[-4:] if numero_cartao else None,
        "bandeira": cartao.get("Brand"),
        "titular": cartao.get("Holder"),
        "raw": pagamento
    }


def verificar_duplicados_por_criterio(pagamentos, tolerancia_minutos=5):

    grupos = defaultdict(list)
    duplicados = []

    for p in pagamentos:

        dados = extrair_dados_pagamento(p)
        if not dados:
            continue

        if not dados["data_obj"] or not dados["cartao_final"]:
            continue

        chave = (dados["valor"], dados["cartao_final"])
        grupos[chave].append(dados)

    for lista in grupos.values():

        lista.sort(key=lambda x: x["data_obj"])

        for i in range(1, len(lista)):
            diff = lista[i]["data_obj"] - lista[i - 1]["data_obj"]

            if diff <= timedelta(minutes=tolerancia_minutos):
                duplicados.append(lista[i])

    return duplicados