# 🌾 Mission Control AI — AgroSat

Sistema de monitoramento operacional de satélite de sensoriamento agrícola com IA generativa, desenvolvido para a Global Solution 2026.1 da FIAP.

---

## Integrantes

- Nome Completo — RM: XXXXXX — Turma: XCCXX
- Nome Completo — RM: XXXXXX — Turma: XCCXX
- Nome Completo — RM: XXXXXX — Turma: XCCXX

---

## O que o projeto faz

O **AgroSat Mission Control AI** simula o monitoramento operacional de um satélite multiespectral em órbita baixa (similar ao CBERS-4A / Planet Labs). O sistema gera dados de telemetria em tempo real, detecta anomalias via lógica Python e usa IA generativa (Ollama Cloud, modelo `gpt-oss:120b`) para analisar o estado da missão em linguagem natural — sempre conectando eventos técnicos em órbita ao impacto no agronegócio brasileiro.

---

## Persona atendida

**Engenheiro de Operações do AgroSat-1** — profissional responsável por monitorar a saúde do satélite, identificar anomalias e acionar protocolos de contingência. Precisa entender rapidamente o estado da missão e comunicar impactos operacionais para clientes terrestres (produtores rurais, seguradoras agrícolas, plataformas como FieldView e Strider).

---

## Tecnologias utilizadas

- Python 3.10+
- Ollama Cloud API (modelo `gpt-oss:120b`)
- `ollama==0.6.2` — cliente Python para Ollama Cloud
- `python-dotenv==1.2.2` — gerenciamento de credenciais via `.env`
- `rich==15.0.0` — interface CLI com painéis, tabelas e formatação
- `prompt-toolkit==3.0.52` — input interativo com histórico
- `pyfiglet==1.0.4` — banner ASCII art

---

## Como executar

```bash
# 1. Clone o repositório
git clone https://github.com/usuario/mission-control-ai.git
cd mission-control-ai

# 2. Crie ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows

# 3. Instale dependências
pip install -r requirements.txt

# 4. Crie o arquivo .env na raiz
cp .env.example .env
# Edite o .env e insira sua chave Ollama Cloud:
# OLLAMA_API_KEY=sua_chave_aqui

# 5. Execute o sistema
python main.py
```

---

## Comandos disponíveis na CLI

| Comando | Descrição |
|---------|-----------|
| `/help` | Lista todos os comandos |
| `/status` | Exibe snapshot atual da telemetria |
| `/about` | Informações sobre o sistema e a trilha |
| `/clear` | Limpa a tela |
| `/exit` | Encerra o sistema |

Qualquer outra entrada é tratada como pergunta ao operador de IA.

---

## Parâmetros monitorados

| Parâmetro | Range Normal | Descrição |
|---|---|---|
| `ndvi_saude` | 70–100% | Saúde do sensor multiespectral |
| `temperatura` | 15–45°C | Temperatura do payload óptico |
| `armazenamento` | 10–80% | Capacidade de armazenamento usada |
| `energia` | 40–100% | Nível dos painéis solares |
| `downlink` | 60–100% | Qualidade do link de transmissão |

---

## Cenários de teste demonstrados

1. **Operação normal** — todos os parâmetros dentro dos ranges
2. **Sensor NDVI degradado** — alerta + análise IA sobre impacto nas imagens de safra
3. **Temperatura crítica** — resposta automatizada: payload em standby
4. **Energia crítica** — modo economia ativado automaticamente
5. **Falha de downlink** — antena secundária ativada, impacto na entrega de dados agrícolas

---

## 💼 Proposta de valor / modelo de negócio

### 1. Qual o problema real terrestre que esta missão resolve?
O agronegócio brasileiro depende de dados de satélite para decisões de irrigação, previsão de safra e validação de seguros rurais baseados em índice. Quando o satélite tem anomalias não detectadas a tempo, imagens chegam com qualidade degradada ou não chegam — produtores tomam decisões com dados incorretos, seguradoras rejeitam sinistros por falta de evidência, e plataformas de gestão agrícola ficam com dados desatualizados. O AgroSat Mission Control AI detecta esses problemas em tempo real e traduz o impacto técnico para as personas certas.

### 2. Quem paga pela solução?
Modelo híbrido: setor privado (operadoras de satélite como Visiona, plataformas como FieldView/Strider, seguradoras rurais como Swiss Re e IRB) contrata o sistema como SaaS de monitoramento operacional. O setor público (EMBRAPA, AEB, INPE) pode contratar como serviço de dados para programas de monitoramento de safra nacional.

### 3. Métrica de impacto
Se o AgroSat-1 operar 100% saudável por 1 ano: aproximadamente **12 milhões de hectares monitorados** continuamente no Cerrado e Matopiba, fornecendo imagens NDVI para ~8.000 produtores rurais, validando índices para ~3.500 apólices de seguro agrícola e alimentando plataformas de gestão que movimentam ~R$ 2 bilhões em decisões de irrigação e insumos.

### 4. Modelo de negócio
**SaaS B2B** com camadas:
- *Dados-como-serviço*: acesso à API de telemetria e imagens processadas via assinatura mensal
- *Monitoramento gerenciado*: contrato anual com SLA de uptime do satélite para operadoras
- *Concessão pública*: parceria com AEB/EMBRAPA para programas governamentais de segurança alimentar

---

## System Prompt

O system prompt completo está em [`prompts/system_prompt.md`](prompts/system_prompt.md). Em resumo, instrui a IA a:
- Atuar como assistente de controle de missão do AgroSat-1
- Sempre conectar análise técnica ao impacto no agronegócio
- Responder com diagnóstico técnico + impacto terrestre + recomendação

---

## Limitações conhecidas

- Os dados de telemetria são simulados aleatoriamente (não refletem uma missão real)
- O histórico de telemetria é perdido ao encerrar o sistema (memória apenas em sessão)
- A API Ollama Cloud pode ter latência variável dependendo da carga do serviço
- Cenários de anomalia ocorrem com 20% de probabilidade por leitura — para testes forçados, edite `data/cenarios.json`

---

## Demonstração

> 📸 *Adicione os prints reais do sistema funcionando na pasta `assets/` e referencie aqui*

![Banner inicial do sistema](assets/screenshot_banner.png)
![Análise IA em cenário de alerta](assets/screenshot_analise.png)

---

## 🎬 Vídeo de demonstração

🔗 [Assistir demonstração no YouTube](https://www.youtube.com/watch?v=SEU_ID_AQUI)

> Configurado como "Não listado" no YouTube.
