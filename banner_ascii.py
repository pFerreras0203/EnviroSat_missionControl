import sys
import pyfiglet
from rich.console import Console
from rich.align import Align
from rich.text import Text
from rich.columns import Columns
from rich.panel import Panel

console = Console()

COR_TITULO  = "#22C55E"
COR_SUBTIT  = "#06B6D4"
COR_RODAPE  = "#6B7280"


def banner_padrao():
    linha1 = pyfiglet.figlet_format("EnviroSat", font="ansi_shadow")
    linha2 = pyfiglet.figlet_format("Mission Control AI", font="small")

    console.print(Align.center(Text(linha1, style=f"bold {COR_TITULO}")))
    console.print(Align.center(Text(linha2, style=f"bold {COR_SUBTIT}")))
    console.print(
        Align.center(
            Text(
                "── 2026.1 - Prompt Engineering and AI - FIAP - EnviroSat  ──",
                style=f"italic {COR_RODAPE}",
            )
        )
    )


def listar_fontes():
    todas = pyfiglet.FigletFont.getFonts()
    console.print(f"\n[bold]Total de fontes disponíveis: {len(todas)}[/]\n")
    colunas = [Text(f, style=COR_SUBTIT) for f in sorted(todas)]
    console.print(Columns(colunas, equal=True, expand=True))


def testar_fonte(fonte: str, texto: str = "EnviroSat"):
    try:
        resultado = pyfiglet.figlet_format(texto, font=fonte)
        console.print(Panel(
            Text(resultado, style=f"bold {COR_TITULO}"),
            title=f"Fonte: {fonte}",
            border_style=COR_SUBTIT,
        ))
    except pyfiglet.FontNotFound:
        console.print(f"[red]Fonte '{fonte}' não encontrada.[/red]")
        console.print("Use [bold]-fonts[/bold] para ver as fontes disponíveis.")


def demo_fontes():
    fontes_demo = [
        "ansi_shadow", "slant", "big", "banner3-D",
        "doom", "speed", "standard", "block",
    ]
    console.print(f"\n[bold {COR_SUBTIT}]Demo de fontes — 'EnviroSat'[/]\n")
    for fonte in fontes_demo:
        try:
            banner = pyfiglet.figlet_format("EnviroSat", font=fonte)
            console.print(Panel(
                Text(banner, style=f"bold {COR_TITULO}"),
                title=f"[bold]{fonte}[/bold]",
                border_style=COR_RODAPE,
            ))
        except pyfiglet.FontNotFound:
            pass


if __name__ == "__main__":
    args = sys.argv[1:]

    if not args:
        banner_padrao()
    elif "-fonts" in args:
        listar_fontes()
    elif "-demo" in args:
        demo_fontes()
    elif "-font" in args:
        idx = args.index("-font")
        fonte = args[idx + 1] if idx + 1 < len(args) else "ansi_shadow"
        texto = "EnviroSat"
        if "-text" in args:
            idx_t = args.index("-text")
            texto = args[idx_t + 1] if idx_t + 1 < len(args) else "EnviroSat"
        testar_fonte(fonte, texto)
    else:
        banner_padrao()
