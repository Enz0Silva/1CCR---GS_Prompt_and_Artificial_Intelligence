"""
src/engine.py — Motor de análise da Mission Control AI (AgroSat).

Este arquivo combina:
  - A função llm() para integração com Ollama Cloud
  - A classe MissionEngine que orquestra telemetria + alertas + IA
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from ollama import Client

from src import telemetria, alertas

load_dotenv()

# Identificação da trilha
TRILHA = "agrosat"

# Cliente Ollama Cloud
client = Client(
    host="https://ollama.com",
    headers={"Authorization": "Bearer " + os.environ.get("OLLAMA_API_KEY", "")}
)

# Verificação da chave na inicialização
_api_key = os.environ.get("OLLAMA_API_KEY", "")
print("API KEY carregada:", "OK ✅" if _api_key else "FALTANDO ❌")


def llm(prompt: str, system: str = None, max_tokens: int = 800, temperature: float = 0.3) -> str:
    """Envia prompt ao gpt-oss:120b via Ollama Cloud e retorna texto."""
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
        return f"⚠️ Erro ao consultar IA: {e}"


def load_system_prompt() -> str:
    """Lê o system prompt do arquivo prompts/system_prompt.md."""
    path = Path("prompts/system_prompt.md")
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "Você é um assistente de controle de missão espacial agrícola."


def _montar_contexto_telemetria(dados: dict, lista_alertas: list[dict]) -> str:
    """Monta o bloco de contexto com dados da telemetria e alertas para injetar no prompt."""
    contexto = "## Leitura de Telemetria Atual\n"
    contexto += telemetria.formatar_leitura(dados)
    contexto += "\n\n## Alertas Detectados\n"
    contexto += alertas.formatar_alertas(lista_alertas)

    # Histórico das últimas 3 leituras (memória de contexto)
    historico = telemetria.obter_historico()
    if len(historico) > 1:
        contexto += "\n\n## Últimas Leituras (histórico)\n"
        for leitura in historico[-3:]:
            contexto += (
                f"[{leitura['timestamp']}] "
                f"NDVI={leitura['ndvi_saude']}% | "
                f"Temp={leitura['temperatura']}°C | "
                f"Energia={leitura['energia']}% | "
                f"Downlink={leitura['downlink']}%\n"
            )

    return contexto


class MissionEngine:
    """Motor de análise do AgroSat Mission Control."""

    def __init__(self):
        self.trilha = TRILHA
        self.system_prompt = load_system_prompt()
        self._pronto = True  # True pois analyze() está implementado

    def is_ready(self) -> bool:
        """Retorna True se o motor está pronto para uso."""
        return self._pronto

    def status_snapshot(self) -> str:
        """Coleta telemetria e retorna snapshot formatado do estado atual da missão."""
        dados = telemetria.coletar()
        lista_alertas = alertas.avaliar(dados)
        sev = alertas.severidade_maxima(lista_alertas)

        icone_status = {"NORMAL": "✅", "ALERTA": "⚠️", "CRITICO": "🚨"}.get(sev, "❓")

        snapshot = f"🛰️  AgroSat-1 — Status Operacional\n"
        snapshot += f"{'─' * 40}\n"
        snapshot += telemetria.formatar_leitura(dados)
        snapshot += f"\n{'─' * 40}\n"
        snapshot += f"Status geral: {icone_status} {sev}\n"
        snapshot += f"\n{alertas.formatar_alertas(lista_alertas)}"

        return snapshot

    def analyze(self, pergunta_usuario: str) -> str:
        """
        Analisa a pergunta do operador com base na telemetria atual + alertas + IA generativa.

        Fluxo:
          1. Coleta dados via telemetria.coletar()
          2. Avalia alertas via alertas.avaliar()
          3. Monta prompt com contexto + pergunta
          4. Chama llm() com system prompt da missão
          5. Retorna resposta contextualizada
        """
        # 1. Coletar telemetria
        dados = telemetria.coletar()

        # 2. Avaliar alertas
        lista_alertas = alertas.avaliar(dados)

        # 3. Montar prompt com contexto injetado dinamicamente
        contexto = _montar_contexto_telemetria(dados, lista_alertas)

        prompt = f"""
{contexto}

## Pergunta do Operador
{pergunta_usuario}

Responda com base nos dados de telemetria acima. Conecte sempre a análise técnica ao impacto no agronegócio brasileiro.
"""

        # 4. Chamar o LLM com system prompt da missão
        resposta = llm(prompt, system=self.system_prompt)

        return resposta
