"""
src/telemetria.py — Geração de dados simulados de telemetria do AgroSat.

Parâmetros monitorados:
  - ndvi_saude     : Saúde do sensor multiespectral/NDVI (0–100%)
  - temperatura    : Temperatura do payload óptico (°C)
  - armazenamento  : Capacidade de armazenamento usada (%)
  - energia        : Nível de energia dos painéis solares (%)
  - downlink       : Qualidade do link de downlink (%)
"""

import random
from datetime import datetime


# Ranges normais de operação
RANGES_NORMAIS = {
    "ndvi_saude":    (70, 100),
    "temperatura":   (15, 45),
    "armazenamento": (10, 80),
    "energia":       (40, 100),
    "downlink":      (60, 100),
}

# Histórico das últimas leituras (mantido em memória)
_historico: list[dict] = []


def coletar() -> dict:
    """
    Gera uma leitura simulada de telemetria do AgroSat.
    Introduz variações aleatórias, incluindo possíveis anomalias.
    Retorna dicionário com os valores atuais e timestamp.
    """
    # Chance de 20% de simular alguma anomalia em um parâmetro aleatório
    anomalia_ativa = random.random() < 0.20
    parametro_anomalo = random.choice(list(RANGES_NORMAIS.keys())) if anomalia_ativa else None

    dados = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

    for param, (minimo, maximo) in RANGES_NORMAIS.items():
        if param == parametro_anomalo:
            # Gera valor fora do range normal
            if random.random() < 0.5:
                valor = round(random.uniform(0, minimo * 0.6), 1)      # abaixo do mínimo
            else:
                valor = round(random.uniform(maximo * 1.1, maximo * 1.5), 1)  # acima do máximo
        else:
            valor = round(random.uniform(minimo, maximo), 1)

        # Garante limites físicos absolutos
        valor = max(0, valor)
        if param in ("ndvi_saude", "armazenamento", "energia", "downlink"):
            valor = min(100, valor)

        dados[param] = valor

    # Armazena no histórico (mantém últimas 20 leituras)
    _historico.append(dados)
    if len(_historico) > 20:
        _historico.pop(0)

    return dados


def obter_historico() -> list[dict]:
    """Retorna a lista de leituras armazenadas nesta sessão."""
    return list(_historico)


def formatar_leitura(dados: dict) -> str:
    """Formata uma leitura de telemetria como texto legível."""
    return (
        f"📅 Timestamp     : {dados['timestamp']}\n"
        f"🌿 NDVI / Sensor : {dados['ndvi_saude']}%\n"
        f"🌡️  Temperatura   : {dados['temperatura']}°C\n"
        f"💾 Armazenamento : {dados['armazenamento']}%\n"
        f"⚡ Energia       : {dados['energia']}%\n"
        f"📡 Downlink      : {dados['downlink']}%"
    )
