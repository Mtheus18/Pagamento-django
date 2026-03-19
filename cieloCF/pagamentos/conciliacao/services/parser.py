from dateutil import parser


def extrair_dados_pagamento(pagamento):

    payment = pagamento.get("Payment", {})

    transacao = payment.get("PaymentId")
    if not transacao:
        return None

    amount = payment.get("Amount") or 0
    valor = round(amount / 100, 2)

    cartao = payment.get("CreditCard", {})
    numero_cartao = cartao.get("CardNumber")

    data_str = payment.get("ReceiveDate")

    try:
        data_obj = parser.parse(data_str) if data_str else None
    except Exception:
        data_obj = None

    return {
        "transacao": transacao,
        "nome": payment.get("Name"),
        "valor": valor,
        "status": payment.get("Status"),
        "data": data_str,
        "data_obj": data_obj,
        "cartao_final": numero_cartao[-4:] if numero_cartao else None,
        "bandeira": cartao.get("Brand"),
        "titular": cartao.get("Holder"),
    }