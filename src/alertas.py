THRESHOLDS = {
    "sensor_termico_celsius": {
        "aviso":   45.0,
        "critico": 60.0,
    },
    "ndvi": {
        "aviso":   0.30,
        "critico": 0.20,
    },
    "buffer_imagens_pct": {
        "aviso":   75.0,
        "critico": 90.0,
    },
    "precisao_geo_metros": {
        "aviso":   50.0,
        "critico": 75.0,
    },
    "energia_pct": {
        "aviso":   30.0,
        "critico": 20.0,
    },
}


def avaliar(dados: dict) -> list:
    alertas = []

    temp = dados.get("sensor_termico_celsius", 0.0)
    if temp >= THRESHOLDS["sensor_termico_celsius"]["critico"]:
        alertas.append({
            "parametro": "sensor_termico",
            "valor": temp,
            "nivel": "CRÍTICO",
            "mensagem": f" FOCO DE CALOR DETECTADO: {temp}°C — Temperatura acima de 60°C indica possível incêndio ativo.",
            "acao_automatica": "downlink_prioritario_solicitado",
            "impacto_terrestre": "Brigadistas do PREVFOGO dependem desta imagem para mobilização. Atraso no downlink pode custar horas de resposta ao fogo.",
        })
    elif temp >= THRESHOLDS["sensor_termico_celsius"]["aviso"]:
        alertas.append({
            "parametro": "sensor_termico",
            "valor": temp,
            "nivel": "AVISO",
            "mensagem": f" Temperatura elevada: {temp}°C — Monitoramento intensificado.",
            "acao_automatica": None,
            "impacto_terrestre": "Área sob vigilância. Possível início de evento de calor.",
        })

    ndvi = dados.get("ndvi", 1.0)
    if ndvi <= THRESHOLDS["ndvi"]["critico"]:
        alertas.append({
            "parametro": "ndvi",
            "valor": ndvi,
            "nivel": "CRÍTICO",
            "mensagem": f" VEGETAÇÃO CRITICAMENTE DEGRADADA: NDVI={ndvi} — Degradação severa detectada, consistente com queimada ativa.",
            "acao_automatica": "alerta_desmatamento_gerado",
            "impacto_terrestre": "IBAMA e ICMBio devem ser notificados. Dados válidos para abertura de auto de infração ambiental.",
        })
    elif ndvi <= THRESHOLDS["ndvi"]["aviso"]:
        alertas.append({
            "parametro": "ndvi",
            "valor": ndvi,
            "nivel": "AVISO",
            "mensagem": f" NDVI baixo: {ndvi} — Vegetação sob estresse na área imageada.",
            "acao_automatica": None,
            "impacto_terrestre": "Área requer acompanhamento nas próximas 24–48h.",
        })

    buffer = dados.get("buffer_imagens_pct", 0.0)
    if buffer >= THRESHOLDS["buffer_imagens_pct"]["critico"]:
        alertas.append({
            "parametro": "buffer_imagens",
            "valor": buffer,
            "nivel": "CRÍTICO",
            "mensagem": f" BUFFER CRÍTICO: {buffer}% — Risco real de perda de imagens antes do próximo downlink.",
            "acao_automatica": "downlink_prioritario_solicitado",
            "impacto_terrestre": "Imagens de focos de calor podem ser sobrescritas e perdidas permanentemente. Alertas a brigadistas podem não ser disparados.",
        })
    elif buffer >= THRESHOLDS["buffer_imagens_pct"]["aviso"]:
        alertas.append({
            "parametro": "buffer_imagens",
            "valor": buffer,
            "nivel": "AVISO",
            "mensagem": f" Buffer elevado: {buffer}% — Agende próximo downlink.",
            "acao_automatica": None,
            "impacto_terrestre": "Atraso no downlink pode comprometer entrega de dados ao INPE.",
        })

    geo = dados.get("precisao_geo_metros", 0.0)
    if geo >= THRESHOLDS["precisao_geo_metros"]["critico"]:
        alertas.append({
            "parametro": "precisao_geo",
            "valor": geo,
            "nivel": "CRÍTICO",
            "mensagem": f" GEOLOCALIZAÇÃO DEGRADADA: {geo}m — Coordenadas fora da margem de confiança para laudos ambientais.",
            "acao_automatica": "recalibracao_atitude_iniciada",
            "impacto_terrestre": "Dados desta passagem NÃO estão qualificados para uso em processos de fiscalização do IBAMA. Marcar como não confiáveis.",
        })
    elif geo >= THRESHOLDS["precisao_geo_metros"]["aviso"]:
        alertas.append({
            "parametro": "precisao_geo",
            "valor": geo,
            "nivel": "AVISO",
            "mensagem": f" Precisão reduzida: {geo}m — Verificar sistema de atitude.",
            "acao_automatica": None,
            "impacto_terrestre": "Coordenadas com margem de erro elevada. Confirmar antes de laudo.",
        })

    energia = dados.get("energia_pct", 100.0)
    if energia <= THRESHOLDS["energia_pct"]["critico"]:
        alertas.append({
            "parametro": "energia",
            "valor": energia,
            "nivel": "CRÍTICO",
            "mensagem": f" ENERGIA CRÍTICA: {energia}% — Modo de economia ativado. Sensor óptico suspenso temporariamente.",
            "acao_automatica": "modo_economia_ativado",
            "impacto_terrestre": "Imageamento suspenso até recarga dos painéis. Janelas de monitoramento de focos de calor comprometidas por 1–2 órbitas.",
        })
    elif energia <= THRESHOLDS["energia_pct"]["aviso"]:
        alertas.append({
            "parametro": "energia",
            "valor": energia,
            "nivel": "AVISO",
            "mensagem": f" Energia baixa: {energia}% — Reduzir operações não essenciais.",
            "acao_automatica": None,
            "impacto_terrestre": "Operação degradada pode reduzir frequência de imageamento.",
        })

    return alertas


def nivel_geral(alertas: list) -> str:
    if any(a["nivel"] == "CRÍTICO" for a in alertas):
        return "CRÍTICO"
    if any(a["nivel"] == "AVISO" for a in alertas):
        return "AVISO"
    return "NOMINAL"


def acoes_automaticas(alertas: list) -> list:
    return [
        {"acao": a["acao_automatica"], "parametro": a["parametro"]}
        for a in alertas
        if a.get("acao_automatica")
    ]


def resumo_alertas(alertas: list) -> str:
    if not alertas:
        return " Nenhum alerta ativo — todos os parâmetros dentro dos limites nominais."

    linhas = []
    for a in alertas:
        linhas.append(f"[{a['nivel']}] {a['mensagem']}")
        if a.get("acao_automatica"):
            linhas.append(f"  → Ação automática disparada: {a['acao_automatica']}")
        if a.get("impacto_terrestre"):
            linhas.append(f"  → Impacto terrestre: {a['impacto_terrestre']}")
    return "\n".join(linhas)
