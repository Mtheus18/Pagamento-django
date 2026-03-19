from datetime import datetime

STATUS_PAGO = 2


def filtrar_pagamentos_hoje(pagamentos):

    hoje = datetime.now().date()
    resultado = []

    for p in pagamentos:
        data = p.get("Payment", {}).get("ReceiveDate")

        if not data:
            continue

        if data.startswith(str(hoje)):
            resultado.append(p)

    return resultado


def identificar_faltantes(dados_processados, pagamentos_banco):

    faltantes = []

    for dados in dados_processados:

        if (
            dados["transacao"] not in pagamentos_banco
            and dados["status"] == STATUS_PAGO
        ):
            faltantes.append(dados)

    return faltantes