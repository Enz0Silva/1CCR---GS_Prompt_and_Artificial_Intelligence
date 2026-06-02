"""
src/alertas.py — Thresholds e lógica de decisão do AgroSat.

Toda a lógica de alerta está em código Python puro,
independente da IA. A IA serve para contextualizar e explicar
— não para decidir se é crítico ou não.
"""

# Thresholds de alerta por parâmetro
THRESHOLDS = {
    "ndvi_saude": {
        "critico_baixo": 30,
        "alerta_baixo":  55,
        "normal_min":    70,
    },
    "temperatura": {
        "alerta_alto":  50,
        "critico_alto": 65,
        "alerta_baixo":  5,
        "critico_baixo": -5,
    },
    "armazenamento": {
        "alerta_alto":  85,
        "critico_alto": 95,
    },
    "energia": {
        "critico_baixo": 15,
        "alerta_baixo":  30,
    },
    "downlink": {
        "critico_baixo": 20,
        "alerta_baixo":  45,
    },
}

# Severidades possíveis
SEVERIDADE = {
    "NORMAL":  "✅",
    "ALERTA":  "⚠️",
    "CRITICO": "🚨",
}


def avaliar(dados: dict) -> list[dict]:
    """
    Avalia os dados de telemetria e retorna lista de alertas gerados.
    Cada alerta é um dicionário com: parametro, severidade, valor, mensagem, impacto_terrestre.
    """
    alertas = []

    # --- NDVI / Saúde do sensor ---
    ndvi = dados.get("ndvi_saude", 100)
    th = THRESHOLDS["ndvi_saude"]
    if ndvi < th["critico_baixo"]:
        alertas.append({
            "parametro": "ndvi_saude",
            "severidade": "CRITICO",
            "valor": ndvi,
            "mensagem": f"Sensor NDVI com saúde crítica: {ndvi}%",
            "impacto_terrestre": "Imagens de satélite indisponíveis — produtores rurais perdem acesso a mapas de safra e índices de vegetação para tomada de decisão de irrigação e colheita.",
            "resposta_automatizada": "Modo diagnóstico ativado: calibração forçada do sensor multiespectral iniciada.",
        })
    elif ndvi < th["alerta_baixo"]:
        alertas.append({
            "parametro": "ndvi_saude",
            "severidade": "ALERTA",
            "valor": ndvi,
            "mensagem": f"Sensor NDVI com degradação: {ndvi}%",
            "impacto_terrestre": "Qualidade das imagens NDVI reduzida — análises de safra menos precisas, risco de erro em seguros rurais baseados em índice.",
            "resposta_automatizada": None,
        })

    # --- Temperatura ---
    temp = dados.get("temperatura", 25)
    th = THRESHOLDS["temperatura"]
    if temp > th["critico_alto"]:
        alertas.append({
            "parametro": "temperatura",
            "severidade": "CRITICO",
            "valor": temp,
            "mensagem": f"Temperatura crítica do payload óptico: {temp}°C",
            "impacto_terrestre": "Risco de dano permanente ao sensor — perda total de capacidade de imageamento afetaria monitoramento de milhões de hectares de lavoura.",
            "resposta_automatizada": "Modo proteção térmica ativado: payload óptico em standby, dissipadores de calor ao máximo.",
        })
    elif temp > th["alerta_alto"]:
        alertas.append({
            "parametro": "temperatura",
            "severidade": "ALERTA",
            "valor": temp,
            "mensagem": f"Temperatura elevada do payload: {temp}°C",
            "impacto_terrestre": "Possível redução na resolução das imagens — janelas de imageamento podem precisar ser encurtadas.",
            "resposta_automatizada": None,
        })
    elif temp < th["critico_baixo"]:
        alertas.append({
            "parametro": "temperatura",
            "severidade": "CRITICO",
            "valor": temp,
            "mensagem": f"Temperatura criticamente baixa: {temp}°C",
            "impacto_terrestre": "Risco de dano ao sensor por frio extremo — possível indisponibilidade de imageamento.",
            "resposta_automatizada": "Aquecedores de payload ativados.",
        })

    # --- Armazenamento ---
    arm = dados.get("armazenamento", 50)
    th = THRESHOLDS["armazenamento"]
    if arm > th["critico_alto"]:
        alertas.append({
            "parametro": "armazenamento",
            "severidade": "CRITICO",
            "valor": arm,
            "mensagem": f"Armazenamento a bordo crítico: {arm}% cheio",
            "impacto_terrestre": "Novas imagens não serão gravadas — áreas agrícolas programadas para imageamento hoje perderão a janela de observação.",
            "resposta_automatizada": "Downlink de emergência iniciado: transmissão prioritária das imagens mais recentes para estação terrestre.",
        })
    elif arm > th["alerta_alto"]:
        alertas.append({
            "parametro": "armazenamento",
            "severidade": "ALERTA",
            "valor": arm,
            "mensagem": f"Armazenamento elevado: {arm}% cheio",
            "impacto_terrestre": "Capacidade de imageamento contínuo reduzida nas próximas órbitas.",
            "resposta_automatizada": None,
        })

    # --- Energia ---
    energia = dados.get("energia", 80)
    th = THRESHOLDS["energia"]
    if energia < th["critico_baixo"]:
        alertas.append({
            "parametro": "energia",
            "severidade": "CRITICO",
            "valor": energia,
            "mensagem": f"Energia crítica nos painéis solares: {energia}%",
            "impacto_terrestre": "Risco de desligamento do satélite — todas as operações de sensoriamento agrícola interrompidas.",
            "resposta_automatizada": "Modo economia de energia ativado: sistemas não-essenciais desligados, payload em standby.",
        })
    elif energia < th["alerta_baixo"]:
        alertas.append({
            "parametro": "energia",
            "severidade": "ALERTA",
            "valor": energia,
            "mensagem": f"Energia baixa: {energia}%",
            "impacto_terrestre": "Operações de imageamento podem ser reduzidas na próxima órbita.",
            "resposta_automatizada": None,
        })

    # --- Downlink ---
    downlink = dados.get("downlink", 80)
    th = THRESHOLDS["downlink"]
    if downlink < th["critico_baixo"]:
        alertas.append({
            "parametro": "downlink",
            "severidade": "CRITICO",
            "valor": downlink,
            "mensagem": f"Link de downlink crítico: {downlink}%",
            "impacto_terrestre": "Transmissão de imagens para Terra interrompida — dados de safra não chegam às plataformas agrícolas (FieldView, Strider, etc.).",
            "resposta_automatizada": "Antena secundária ativada, tentativa de reconexão com estação terrestre alternativa.",
        })
    elif downlink < th["alerta_baixo"]:
        alertas.append({
            "parametro": "downlink",
            "severidade": "ALERTA",
            "valor": downlink,
            "mensagem": f"Qualidade do downlink reduzida: {downlink}%",
            "impacto_terrestre": "Velocidade de entrega de imagens para plataformas agrícolas reduzida.",
            "resposta_automatizada": None,
        })

    return alertas


def formatar_alertas(alertas: list[dict]) -> str:
    """Formata a lista de alertas como texto legível para exibição."""
    if not alertas:
        return "✅ Todos os parâmetros dentro dos limites normais."

    linhas = []
    for a in alertas:
        icone = SEVERIDADE.get(a["severidade"], "❓")
        linhas.append(f"{icone} [{a['severidade']}] {a['mensagem']}")
        if a.get("resposta_automatizada"):
            linhas.append(f"   🤖 Resposta automática: {a['resposta_automatizada']}")
    return "\n".join(linhas)


def severidade_maxima(alertas: list[dict]) -> str:
    """Retorna a severidade mais alta entre os alertas ativos."""
    if any(a["severidade"] == "CRITICO" for a in alertas):
        return "CRITICO"
    if any(a["severidade"] == "ALERTA" for a in alertas):
        return "ALERTA"
    return "NORMAL"
