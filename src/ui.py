import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.align import Align
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from datetime import datetime

console = Console()

COR_PRIMARIA   = "#22C55E"
COR_SECUNDARIA = "#06B6D4"
COR_ALERTA     = "#F59E0B"
COR_CRITICO    = "#EF4444"
COR_SUTIL      = "#6B7280"

session = PromptSession(
    style=Style.from_dict({"prompt": f"{COR_PRIMARIA} bold"})
)

CENARIOS_DISPONIVEIS = [
    "nominal",
    "incendio_critico",
    "energia_baixa",
    "buffer_cheio",
    "multipla_falha",
]


def show_banner():
    console.clear()

    banner1 = pyfiglet.figlet_format("EnviroSat", font="ansi_shadow")
    banner2 = pyfiglet.figlet_format("Mission Control AI", font="small")

    console.print(Align.center(Text(banner1, style=f"bold {COR_PRIMARIA}")))
    console.print(Align.center(Text(banner2, style=f"bold {COR_SECUNDARIA}")))
    console.print(
        Align.center(
            Text(
                "── 2026.1 · Prompt Engineering and AI · FIAP ──",
                style=f"italic {COR_SUTIL}",
            )
        )
    )
    console.print()

    console.print(
        Panel.fit(
            f"[{COR_PRIMARIA}]Satélite de observação ambiental em LEO — Monitoramento de biomas brasileiros.[/]\n"
            f"Detecção de focos de calor - Desmatamento - Áreas protegidas - NDVI\n\n"
            f"[{COR_SUTIL}]Use [bold]/help[/bold] para ver os comandos  -  [bold]/exit[/bold] para sair[/]\n"
            f"[{COR_SUTIL}]Modelo: gpt-oss:120b via Ollama Cloud[/]",
            title=f"[bold {COR_PRIMARIA}] ENVIROSAT MISSION CONTROL[/]",
            border_style=COR_PRIMARIA,
        )
    )
    console.print()


def show_response(texto: str, titulo: str = " Mission Control AI"):
    hora = datetime.now().strftime("%H:%M:%S")
    console.print(
        Panel(
            texto,
            title=f"[bold {COR_SECUNDARIA}]{titulo}[/]",
            subtitle=f"[{COR_SUTIL}]{hora}[/]",
            border_style=COR_SECUNDARIA,
            padding=(1, 2),
        )
    )
    console.print()


def show_status(texto: str):
    hora = datetime.now().strftime("%H:%M:%S")
    console.print(
        Panel(
            texto,
            title=f"[bold {COR_PRIMARIA}] Telemetria EnviroSat-1[/]",
            subtitle=f"[{COR_SUTIL}]{hora}[/]",
            border_style=COR_PRIMARIA,
            padding=(1, 2),
        )
    )
    console.print()


def show_aviso(mensagem: str):
    console.print(f"[bold {COR_ALERTA}]    {mensagem}[/]")
    console.print()


def show_erro(mensagem: str):
    console.print(f"[bold {COR_CRITICO}]    {mensagem}[/]")
    console.print()


def show_ok(mensagem: str):
    console.print(f"[bold {COR_PRIMARIA}]    {mensagem}[/]")
    console.print()


def cmd_help():
    tabela = Table(
        title="Comandos disponíveis",
        border_style=COR_PRIMARIA,
        header_style=f"bold {COR_PRIMARIA}",
        show_lines=True,
    )
    tabela.add_column("Comando", style=f"bold {COR_SECUNDARIA}", min_width=22)
    tabela.add_column("Descrição", style="white")

    tabela.add_row("/help", "Exibe esta tabela de comandos")
    tabela.add_row("/status", "Leitura atual de telemetria em tempo real")
    tabela.add_row(
        "/cenario <nome>",
        "Simula cenário pré-definido:\n"
        "  nominal | incendio_critico | energia_baixa\n"
        "  buffer_cheio | multipla_falha",
    )
    tabela.add_row("/about", "Informações do projeto e da equipe")
    tabela.add_row("/clear", "Limpa a tela e reexibe o banner")
    tabela.add_row("/exit", "Encerra o Mission Control AI")
    tabela.add_row(
        "[qualquer texto]",
        "Consulta a IA com dados de telemetria atuais.\n"
        'Ex: "Como está a missão?" / "Tem fogo na área?"',
    )

    console.print(tabela)
    console.print()


def cmd_about():
    console.print(
        Panel.fit(
            f"[bold {COR_PRIMARIA}]  EnviroSat Mission Control AI[/]\n\n"
            "[white]Sistema de monitoramento operacional de satélite de observação\n"
            "ambiental com análise em linguagem natural via IA generativa.\n\n"
            "Detecta focos de calor, desmatamento e anomalias operacionais,\n"
            "conectando cada alerta técnico ao impacto terrestre correspondente.[/]\n\n"
            f"[{COR_SUTIL}]── Equipe ──[/]\n"
            f"[white]Pedro Ferreras  - RM: 568713 - Turma: 1CCPI\n"
            f"Pedro Santos    - RM: 571017 - Turma: 1CCPI[/]\n\n"
            f"[{COR_SUTIL}]Disciplina: Prompt Engineering and Artificial Intelligence\n"
            f"FIAP - Ciência da Computação - Global Solution 2026.1\n"
            f"Modelo: gpt-oss:120b via Ollama Cloud - Trilha: EnviroSat [/]",
            title=f"[bold {COR_SECUNDARIA}] Sobre o Projeto[/]",
            border_style=COR_SECUNDARIA,
        )
    )
    console.print()


def cmd_cenario(engine, args: list):
    if not args:
        show_aviso(
            "Informe o nome do cenário. Disponíveis: "
            + " | ".join(CENARIOS_DISPONIVEIS)
        )
        return

    nome = args[0].lower().replace("-", "_")
    if nome not in CENARIOS_DISPONIVEIS:
        show_erro(
            f"Cenário '{nome}' não encontrado. Disponíveis: "
            + " | ".join(CENARIOS_DISPONIVEIS)
        )
        return

    show_ok(f"Simulando cenário: [bold]{nome}[/]")

    with console.status(
        f"[{COR_PRIMARIA}]Analisando cenário {nome}...[/]", spinner="dots"
    ):
        resposta = engine.analyze_cenario(
            f"Analise o estado atual da missão neste cenário: {nome}",
            nome_cenario=nome,
        )

    show_response(resposta, titulo=f" Análise — Cenário: {nome}")


def run_cli(engine):
    show_banner()

    if not engine.is_ready():
        show_aviso(
            "Engine status: AGUARDANDO IMPLEMENTAÇÃO ✗\n"
            "  Complete os métodos em src/engine.py para ativar a IA."
        )

    while True:
        try:
            entrada = session.prompt("❯ ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print(
                f"\n[{COR_SUTIL}]Encerrando Mission Control AI... Até a próxima órbita. [/]\n"
            )
            break

        if not entrada:
            continue

        partes = entrada.split()
        comando = partes[0].lower()
        args = partes[1:]

        if comando == "/exit":
            console.print(
                f"\n[{COR_SUTIL}]Encerrando Mission Control AI... Até a próxima órbita. [/]\n"
            )
            break

        if comando == "/help":
            cmd_help()
            continue

        if comando == "/clear":
            show_banner()
            continue

        if comando == "/about":
            cmd_about()
            continue

        if comando == "/status":
            with console.status(
                f"[{COR_PRIMARIA}]Coletando telemetria...[/]", spinner="dots"
            ):
                snapshot = engine.status_snapshot()
            show_status(snapshot)
            continue

        if comando == "/cenario":
            cmd_cenario(engine, args)
            continue

        with console.status(
            f"[{COR_PRIMARIA}]Analisando com gpt-oss:120b...[/]", spinner="dots"
        ):
            resposta = engine.analyze(entrada)

        show_response(resposta)
