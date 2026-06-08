import random
from datetime import datetime

RANGES_NOMINAIS = {
    "sensor_termico_celsius": (18.0, 42.0),
    "ndvi": (0.35, 1.0),
    "buffer_imagens_pct": (10.0, 70.0),
    "precisao_geo_metros": (5.0, 40.0),
    "energia_pct": (35.0, 100.0),
    "orbita_numero": (1000, 9999),
    "angulo_solar": (5.0, 85.0),
}


def coletar() -> dict:
    chance_anomalia = random.random()

    if chance_anomalia < 0.15:
        sensor_termico = round(random.uniform(55.0, 78.0), 1)
        ndvi = round(random.uniform(0.10, 0.25), 3)
    elif chance_anomalia < 0.30:
        sensor_termico = round(random.uniform(22.0, 38.0), 1)
        ndvi = round(random.uniform(0.40, 0.80), 3)
    else:
        sensor_termico = round(random.uniform(20.0, 40.0), 1)
        ndvi = round(random.uniform(0.45, 0.90), 3)

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sensor_termico_celsius": sensor_termico,
        "ndvi": ndvi,
        "buffer_imagens_pct": round(random.uniform(15.0, 95.0), 1),
        "precisao_geo_metros": round(random.uniform(8.0, 90.0), 1),
        "energia_pct": round(random.uniform(8.0, 98.0), 1),
        "orbita_numero": random.randint(1000, 9999),
        "angulo_solar": round(random.uniform(5.0, 85.0), 1),
    }


def coletar_cenario(nome: str) -> dict:
    cenarios = {
        "nominal": {
            "sensor_termico_celsius": 31.2,
            "ndvi": 0.74,
            "buffer_imagens_pct": 42.0,
            "precisao_geo_metros": 14.5,
            "energia_pct": 81.0,
        },
        "incendio_critico": {
            "sensor_termico_celsius": 68.4,
            "ndvi": 0.17,
            "buffer_imagens_pct": 78.5,
            "precisao_geo_metros": 19.0,
            "energia_pct": 52.0,
        },
        "energia_baixa": {
            "sensor_termico_celsius": 28.5,
            "ndvi": 0.62,
            "buffer_imagens_pct": 33.0,
            "precisao_geo_metros": 16.0,
            "energia_pct": 14.0,
        },
        "buffer_cheio": {
            "sensor_termico_celsius": 35.0,
            "ndvi": 0.58,
            "buffer_imagens_pct": 93.5,
            "precisao_geo_metros": 22.0,
            "energia_pct": 67.0,
        },
        "multipla_falha": {
            "sensor_termico_celsius": 64.1,
            "ndvi": 0.19,
            "buffer_imagens_pct": 91.0,
            "precisao_geo_metros": 78.0,
            "energia_pct": 17.0,
        },
    }

    base = cenarios.get(nome, cenarios["nominal"])
    base["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    base["orbita_numero"] = random.randint(1000, 9999)
    base["angulo_solar"] = round(random.uniform(15.0, 75.0), 1)
    return base


def formatar_para_exibicao(dados: dict) -> str:
    linhas = [
        f"  EnviroSat-1 · Órbita #{dados['orbita_numero']} · {dados['timestamp']}",
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"   Sensor Térmico     : {dados['sensor_termico_celsius']}°C",
        f"   NDVI (vegetação)   : {dados['ndvi']}",
        f"   Buffer de imagens  : {dados['buffer_imagens_pct']}%",
        f"   Precisão Geo       : {dados['precisao_geo_metros']}m",
        f"   Energia disponível : {dados['energia_pct']}%",
        f"   Ângulo solar       : {dados['angulo_solar']}°",
    ]
    return "\n".join(linhas)
