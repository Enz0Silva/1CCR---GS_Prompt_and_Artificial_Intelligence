"""Interface CLI estilo Claude Code — usa Rich + prompt-toolkit."""

import pyfiglet
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style

console = Console()
session = PromptSession(style=Style.from_dict({"prompt": "#22C55E bold"}))

COMANDOS = {
    "/help":   "Exibe esta lista de comandos",
    "/status": "Mostra snapshot atual da telemetria",
    "/about":  "Informações sobre o sistema e a trilha",
    "/clear":  "Limpa a tela e exibe o banner",
    "/exit":   "Encerra o sistema",
}


def show_banner():
    """Exibe banner ASCII colorido e card de boas-vindas."""
    linha1 = pyfiglet.figlet_format("AgroSat", font="ansi_shadow")
    linha2 = pyfiglet.figlet_format("Mission Control", font="ansi_shadow")

    console.print(Text(linha1, style="bold #22C55E"))
    console.print(Text(linha2, style="bold #06B6D4"))

    console.print(Panel.fit(
        "🌾 Sistema de monitoramento de satélite agrícola via IA generativa.\n"
        "Trilha AgroSat — FIAP · Global Solution 2026.1\n\n"
        "Use [bold #22C55E]/help[/bold #22C55E] para ver os comandos · "
        "[bold #EF4444]/exit[/bold #EF4444] para sair.\n"
        "Modelo: [bold]gpt-oss:120b[/bold] via Ollama Cloud",
        title="◆ AGROSAT MISSION CONTROL",
        border_style="#22C55E"
    ))


def show_help():
    """Exibe tabela de comandos disponíveis."""
    table = Table(title="Comandos disponíveis", border_style="#22C55E", show_lines=True)
    table.add_column("Comando", style="bold #22C55E")
    table.add_column("Descrição", style="white")
    for cmd, desc in COMANDOS.items():
        table.add_row(cmd, desc)
    console.print(table)


def show_about():
    """Exibe informações sobre o sistema."""
    console.print(Panel(
        "🛰️  [bold]AgroSat Mission Control AI[/bold]\n\n"
        "Simula o monitoramento operacional de um satélite de sensoriamento\n"
        "multiespectral em órbita baixa (similar ao CBERS-4A / Planet Labs).\n\n"
        "📡 [bold]Parâmetros monitorados:[/bold]\n"
        "  • Saúde do sensor NDVI (0–100%)\n"
        "  • Temperatura do payload óptico (°C)\n"
        "  • Capacidade de armazenamento (%)\n"
        "  • Nível de energia dos painéis solares (%)\n"
        "  • Qualidade do link de downlink (%)\n\n"
        "🌾 [bold]Setor de impacto:[/bold] Agronegócio brasileiro\n"
        "   Gestão de safras, irrigação e seguro rural baseado em índice.\n\n"
        "🏢 [bold]Personas atendidas:[/bold]\n"
        "   Engenheiro de operações · Produtor rural · Analista de seguro agrícola",
        title="◆ Sobre o Sistema",
        border_style="#06B6D4"
    ))


def show_response(text: str):
    """Renderiza resposta da IA em painel com timestamp."""
    now = datetime.now().strftime("%H:%M")
    console.print(Panel(
        text,
        title="◆ AgroSat Mission Control",
        subtitle=now,
        border_style="#22C55E"
    ))


def show_error(text: str):
    """Exibe mensagem de erro formatada."""
    console.print(Panel(text, title="⚠ Aviso", border_style="yellow"))


def run_cli(engine):
    """Loop principal da CLI."""
    show_banner()

    if not engine.is_ready():
        console.print(
            "\n  ⚠  Engine status: [yellow]AGUARDANDO IMPLEMENTAÇÃO ✗[/yellow]\n"
        )

    while True:
        try:
            user_input = session.prompt("❯ ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Encerrando sistema...[/dim]")
            break

        if not user_input:
            continue

        if user_input == "/exit":
            console.print("[dim]Missão encerrada. Até a próxima órbita! 🛰️[/dim]")
            break
        elif user_input == "/help":
            show_help()
        elif user_input == "/about":
            show_about()
        elif user_input == "/status":
            show_response(engine.status_snapshot())
        elif user_input == "/clear":
            console.clear()
            show_banner()
        else:
            with console.status("[bold #22C55E]Analisando telemetria...[/bold #22C55E]"):
                resposta = engine.analyze(user_input)
            show_response(resposta)
