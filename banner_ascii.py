"""
banner_ascii.py — Gerador de banner ASCII para Mission Control AI
Uso:
  python banner_ascii.py              # Banner padrão
  python banner_ascii.py -fonts       # Lista fontes disponíveis
  python banner_ascii.py -font slant -text "Meu Texto"
  python banner_ascii.py -demo        # Demonstra 8 fontes
"""

import sys
import pyfiglet
from rich.console import Console
from rich.align import Align
from rich.text import Text

console = Console()


def print_banner():
    """Exibe o banner padrão do projeto."""
    linha1 = pyfiglet.figlet_format("Global Solution", font="ansi_shadow")
    linha2 = pyfiglet.figlet_format("Mission Control AI", font="ansi_shadow")

    console.print(Align.center(Text(linha1, style="bold #A855F7")))
    console.print(Align.center(Text(linha2, style="bold #06B6D4")))
    console.print(Align.center(
        Text("── 2026.1 · Prompt Engineering and AI · FIAP ──",
             style="italic #8484A0")
    ))
    console.print(Align.center(
        Text("🌾 Trilha AgroSat — Sensoriamento Agrícola", style="bold #22C55E")
    ))


def list_fonts():
    """Lista todas as fontes disponíveis no PyFiglet."""
    fonts = pyfiglet.FigletFont.getFonts()
    console.print(f"[bold]Fontes disponíveis ({len(fonts)} total):[/bold]")
    for i, font in enumerate(sorted(fonts)):
        console.print(f"  {font}", end="  " if (i + 1) % 4 != 0 else "\n")


def demo_fonts():
    """Demonstra 8 fontes diferentes."""
    fontes = ["ansi_shadow", "slant", "big", "banner3", "doom", "epic", "star_wars", "chunky"]
    for font in fontes:
        try:
            banner = pyfiglet.figlet_format("AgroSat", font=font)
            console.print(f"[dim]Fonte: {font}[/dim]")
            console.print(Text(banner, style="bold #06B6D4"))
            console.rule()
        except Exception:
            console.print(f"[red]Fonte '{font}' indisponível[/red]")


if __name__ == "__main__":
    args = sys.argv[1:]

    if "-fonts" in args:
        list_fonts()
    elif "-demo" in args:
        demo_fonts()
    elif "-font" in args:
        idx = args.index("-font")
        font = args[idx + 1] if idx + 1 < len(args) else "ansi_shadow"
        text_idx = args.index("-text") if "-text" in args else -1
        text = args[text_idx + 1] if text_idx >= 0 and text_idx + 1 < len(args) else "Mission Control AI"
        try:
            banner = pyfiglet.figlet_format(text, font=font)
            console.print(Text(banner, style="bold #06B6D4"))
        except Exception as e:
            console.print(f"[red]Erro: {e}[/red]")
    else:
        print_banner()
