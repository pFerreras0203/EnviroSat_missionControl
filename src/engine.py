import os
from ollama import Client
from dotenv import load_dotenv
from pathlib import Path

from src.telemetria import coletar, coletar_cenario, formatar_para_exibicao
from src.alertas import avaliar, nivel_geral, acoes_automaticas, resumo_alertas

load_dotenv()

TRILHA = "envirosat"

_api_key = os.environ.get("OLLAMA_API_KEY", "")
print(f"[EnviroSat] API KEY Ollama: {'OK ✓' if _api_key else 'FALTANDO ✗ — configure .env'}")

client = Client(
    host="https://ollama.com",
    headers={"Authorization": f"Bearer {_api_key}"},
)


def llm(prompt: str, system: str = None, max_tokens: int = 900, temperature: float = 0.3) -> str:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    try:
        resposta = client.chat(
            model="gpt-oss:120b",
            messages=messages,
            options={"num_predict": max_tokens, "temperature": temperature},
            stream=False,
        )
        return resposta["message"]["content"].strip()
    except Exception as e:
        return (
            f"  Erro ao consultar a IA: {e}\n\n"
            "Verifique:\n"
            "  • Se OLLAMA_API_KEY está correta no arquivo .env\n"
            "  • Se há conexão com a internet\n"
            "  • Se o serviço Ollama Cloud está disponível"
        )


def _load_system_prompt() -> str:
    caminho = Path("prompts/system_prompt.md")
    if caminho.exists():
        return caminho.read_text(encoding="utf-8")
    return (
        "Você é o Mission Control AI do satélite EnviroSat-1, "
        "um satélite de observação ambiental em órbita baixa. "
        "Analise os dados de telemetria e forneça diagnóstico técnico "
        "e impacto terrestre para cada situação."
    )


class MissionEngine:
    def __init__(self):
        self.trilha = TRILHA
        self.system_prompt = _load_system_prompt()
        self._historico: list = []
        self._max_historico = 3
        self._ciclo_atual = 0

    def is_ready(self) -> bool:
        return True

    def status_snapshot(self) -> str:
        dados = coletar()
        alertas = avaliar(dados)
        nivel = nivel_geral(alertas)
        acoes = acoes_automaticas(alertas)

        saida = [formatar_para_exibicao(dados), ""]

        emoji_nivel = {"NOMINAL": "✅", "AVISO": "🟡", "CRÍTICO": "🔴"}
        saida.append(f"Status geral da missão: {emoji_nivel.get(nivel, '❓')} {nivel}")

        if alertas:
            saida.append("\n  Alertas ativos:")
            for alerta in alertas:
                saida.append(f"   {alerta['mensagem']}")
        else:
            saida.append(" Todos os parâmetros dentro dos limites nominais.")

        if acoes:
            saida.append("\n Ações automáticas disparadas:")
            for acao in acoes:
                saida.append(f"   → {acao['acao']} (gatilho: {acao['parametro']})")

        return "\n".join(saida)

    def analyze(self, pergunta_usuario: str, cenario: str = None) -> str:
        self._ciclo_atual += 1

        if cenario:
            dados = coletar_cenario(cenario)
        else:
            dados = coletar()

        alertas = avaliar(dados)
        nivel = nivel_geral(alertas)
        acoes = acoes_automaticas(alertas)
        resumo = resumo_alertas(alertas)

        entrada_historico = {
            "ciclo": self._ciclo_atual,
            "timestamp": dados["timestamp"],
            "nivel": nivel,
            "sensor_termico": dados["sensor_termico_celsius"],
            "ndvi": dados["ndvi"],
            "energia": dados["energia_pct"],
            "buffer": dados["buffer_imagens_pct"],
            "alertas": [a["mensagem"][:80] for a in alertas],
        }
        self._historico.append(entrada_historico)
        if len(self._historico) > self._max_historico:
            self._historico.pop(0)

        historico_bloco = ""
        ciclos_anteriores = self._historico[:-1]
        if ciclos_anteriores:
            linhas_hist = ["\n[HISTÓRICO DOS ÚLTIMOS CICLOS — para análise de tendência]"]
            for c in ciclos_anteriores:
                linhas_hist.append(
                    f"  Ciclo {c['ciclo']} ({c['timestamp']}): "
                    f"nível={c['nivel']}, "
                    f"térmico={c['sensor_termico']}°C, "
                    f"NDVI={c['ndvi']}, "
                    f"energia={c['energia']}%, "
                    f"buffer={c['buffer']}%"
                )
                if c["alertas"]:
                    for alerta_hist in c["alertas"]:
                        linhas_hist.append(f"    → {alerta_hist}")
            historico_bloco = "\n".join(linhas_hist)

        acoes_bloco = ""
        if acoes:
            linhas_acoes = ["\n[AÇÕES AUTOMÁTICAS JÁ DISPARADAS PELO SISTEMA]"]
            for a in acoes:
                linhas_acoes.append(f"  ✓ {a['acao']} (gatilho: {a['parametro']})")
            acoes_bloco = "\n".join(linhas_acoes)

        prompt = f"""[LEITURA DE TELEMETRIA — Ciclo #{self._ciclo_atual} · {dados['timestamp']}]
Sensor Térmico       : {dados['sensor_termico_celsius']}°C
NDVI (vegetação)     : {dados['ndvi']}
Buffer de imagens    : {dados['buffer_imagens_pct']}%
Precisão geoloc.     : {dados['precisao_geo_metros']}m
Energia disponível   : {dados['energia_pct']}%
Órbita #             : {dados['orbita_numero']}
Ângulo solar         : {dados['angulo_solar']}°
Nível geral          : {nivel}

[ALERTAS ATIVOS — CALCULADOS POR LÓGICA PYTHON]
{resumo}
{acoes_bloco}
{historico_bloco}

[PERGUNTA DO OPERADOR]
{pergunta_usuario}
"""

        return llm(prompt, system=self.system_prompt)

    def analyze_cenario(self, pergunta: str, nome_cenario: str) -> str:
        return self.analyze(pergunta, cenario=nome_cenario)
