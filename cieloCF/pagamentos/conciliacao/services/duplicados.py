from collections import defaultdict
from datetime import timedelta


def verificar_duplicados_por_criterio(dados_processados, tolerancia_minutos=5):

    grupos = defaultdict(list)
    duplicados = []

    for dados in dados_processados:

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