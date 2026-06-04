# 🚀 Mission Control AI — AgroSat

## Integrantes

- Eric Hernandes Penhalbell — RM: 570237 — Turma: 1CCR
- Enzo Ricardo Silva — RM: 571333 — Turma: 1CCR
- João Guilherme Figueiredo — RM: 572697 — Turma: 1CCR

## O que o projeto faz

O AgroSat Mission Control AI simula o monitoramento operacional de um satélite multiespectral em órbita baixa (similar ao CBERS-4A / Planet Labs), gerando dados de telemetria em tempo real e detectando anomalias via lógica Python. A IA generativa (Ollama Cloud, modelo `gpt-oss:120b`) analisa o estado da missão em linguagem natural, sempre conectando eventos técnicos em órbita ao impacto direto no agronegócio brasileiro — gestão de safras, irrigação e seguro rural baseado em índice.

## Persona atendida

**Engenheiro de Operações do AgroSat-1** — profissional responsável por monitorar a saúde do satélite e acionar protocolos de contingência. Precisa entender rapidamente o estado da missão e comunicar impactos operacionais para clientes terrestres como produtores rurais, seguradoras agrícolas e plataformas como FieldView e Strider.

## Tecnologias utilizadas

- Python 3.10+
- Ollama Cloud API (modelo `gpt-oss:120b`)
- Bibliotecas: `ollama`, `python-dotenv`, `rich`, `prompt-toolkit`, `pyfiglet`

## Como executar

1. Clone o repositório
2. Crie ambiente virtual: `python -m venv .venv` e `source .venv/bin/activate` (Linux/macOS) ou `.venv\Scripts\activate` (Windows)
3. Instale dependências: `pip install -r requirements.txt`
4. Crie arquivo `.env` na raiz com:
   `OLLAMA_API_KEY=sua_chave_aqui`
5. Execute pelo **PowerShell ou CMD externos** (não pelo terminal integrado do PyCharm):
   ```bash
   python main.py
   ```

> ⚠️ **Importante:** o `prompt-toolkit` requer um console Windows real. Sempre execute pelo PowerShell ou CMD externos — o terminal integrado do PyCharm não é suportado.

## Arquitetura técnica

O projeto é organizado em camadas bem definidas, cada uma com responsabilidade única:

```
mission-control-ai/
├── main.py                  # Ponto de entrada — instancia engine e inicia CLI
├── banner_ascii.py          # Gerador de banner ASCII com PyFiglet
├── requirements.txt         # Dependências fixadas
├── .env.example             # Template de credenciais
├── src/
│   ├── telemetria.py        # Geração e histórico de dados simulados
│   ├── alertas.py           # Thresholds e lógica de decisão em Python puro
│   ├── engine.py            # Motor de análise: orquestra telemetria + alertas + IA
│   └── ui.py                # Interface CLI com Rich + prompt-toolkit
├── prompts/
│   └── system_prompt.md     # System prompt da IA com contexto da missão
└── data/
    └── cenarios.json        # Cenários pré-definidos para testes
```

### `src/telemetria.py` — Geração de dados simulados

Simula leituras dos 5 parâmetros do AgroSat-1 a cada chamada, com variações aleatórias e 20% de chance de introduzir uma anomalia em algum parâmetro. Mantém histórico das últimas 20 leituras em memória, que é passado para a IA como contexto temporal — permitindo que o modelo perceba tendências (ex: temperatura subindo progressivamente ao longo das órbitas).

| Parâmetro | Range Normal | O que representa |
|---|---|---|
| `ndvi_saude` | 70–100% | Saúde do sensor multiespectral — determina qualidade das imagens NDVI |
| `temperatura` | 15–45°C | Temperatura do payload óptico — afeta resolução e vida útil do sensor |
| `armazenamento` | 10–80% | Capacidade de armazenamento usada — se cheio, novas imagens não são gravadas |
| `energia` | 40–100% | Nível dos painéis solares — insuficiente paralisa todas as operações |
| `downlink` | 60–100% | Qualidade da transmissão para Terra — determina se os dados chegam às plataformas |

### `src/alertas.py` — Lógica de decisão em Python puro

Toda a lógica de detecção de anomalias está implementada em código Python, sem depender da IA para decidir se um parâmetro é crítico ou não. Cada parâmetro tem thresholds de dois níveis (ALERTA e CRITICO), e situações críticas disparam **respostas automatizadas** imediatas:

| Situação crítica | Resposta automatizada |
|---|---|
| Energia < 15% | Modo economia: sistemas não-essenciais desligados, payload em standby |
| Temperatura > 65°C | Proteção térmica: payload em standby, dissipadores ao máximo |
| Armazenamento > 95% | Downlink de emergência: transmissão prioritária para estação terrestre |
| Downlink < 20% | Antena secundária ativada, reconexão com estação alternativa |
| NDVI < 30% | Modo diagnóstico: calibração forçada do sensor iniciada |

### `src/engine.py` — Motor de análise

O `MissionEngine` é o ponto de orquestração do sistema. Para cada pergunta do operador, ele:

1. Chama `telemetria.coletar()` para obter leitura atualizada
2. Chama `alertas.avaliar()` para detectar anomalias em Python
3. Monta um prompt dinâmico injetando os dados reais + alertas + histórico das últimas 3 leituras
4. Chama `llm()` com o system prompt da missão via Ollama Cloud
5. Retorna a resposta contextualizada ao operador

A função `llm()` é o único ponto de contato com o modelo — toda chamada à IA passa por ela, facilitando manutenção e testes.

### `prompts/system_prompt.md` — System Prompt

O system prompt define a identidade, escopo e formato de resposta da IA. Instrui o modelo a sempre responder em três blocos: **diagnóstico técnico** → **impacto terrestre** → **recomendação operacional**. A regra fundamental do prompt é: nenhum evento técnico pode ser analisado sem traduzir o impacto para o agronegócio brasileiro.

## Demonstração

O Status normal da Missão

Alerta Crítico com Analise da IA

## System Prompt

O system prompt completo está em [`prompts/system_prompt.md`](prompts/system_prompt.md). Instrui a IA a atuar como assistente de controle de missão do AgroSat-1, sempre conectando a análise técnica ao impacto no agronegócio brasileiro, respondendo com diagnóstico técnico + impacto terrestre + recomendação operacional.

## Cenários de teste demonstrados

1. Operação normal — todos os parâmetros dentro do range
2. Sensor NDVI degradado — alerta + análise IA sobre impacto nas imagens de safra
3. Temperatura crítica — resposta automatizada (payload em standby) + análise IA
4. Energia crítica — modo economia ativado automaticamente
5. Falha de downlink — antena secundária ativada, impacto na entrega de dados agrícolas

## Limitações conhecidas

- Os dados de telemetria são simulados aleatoriamente e não refletem uma missão real
- O histórico de telemetria é perdido ao encerrar o sistema (memória apenas em sessão)
- A API Ollama Cloud pode ter latência variável dependendo da carga do serviço
- Não há persistência de logs entre sessões
- O sistema requer execução via PowerShell ou CMD externos no Windows (não compatível com terminal integrado do PyCharm)

## Proposta de valor / modelo de negócio

**1. Qual o problema real terrestre que esta missão resolve?**

O Brasil é o maior exportador agrícola do mundo, com mais de 70 milhões de hectares cultivados e um setor que representa ~25% do PIB nacional. Toda essa produção depende crescentemente de dados de satélite para decisões críticas: quando irrigar, quando colher, como validar sinistros de seguro rural baseado em índice de vegetação (NDVI). O problema é que a cadeia de valor desses dados começa no satélite — e falhas não detectadas a tempo chegam silenciosamente às plataformas agrícolas na forma de imagens degradadas, gaps de cobertura e dados atrasados. Um produtor que toma uma decisão de irrigação com base em imagens NDVI corrompidas pode perder parte da safra. Uma seguradora que valida uma apólice com dados de downlink interrompido pode pagar sinistros indevidos ou negar sinistros legítimos. O AgroSat Mission Control AI resolve exatamente esse gap: detecta anomalias em tempo real, aciona respostas automatizadas e traduz cada evento técnico em órbita para o impacto concreto que ele gera na Terra — para que o operador tome a decisão certa antes que o problema chegue ao produtor.

**2. Quem paga pela solução?**

Modelo híbrido com duas frentes de receita:

- **Setor privado (principal):** Operadoras de satélite como Visiona e Akaer contratam como SaaS de monitoramento operacional com SLA de uptime. Plataformas agrícolas como FieldView, Strider e Aegro pagam pelo acesso à API de telemetria processada para alimentar seus próprios sistemas de alerta. Seguradoras rurais como Swiss Re, IRB e Mapfre usam os dados de disponibilidade do satélite para validar a confiabilidade dos índices que fundamentam suas apólices.

- **Setor público (complementar):** EMBRAPA e AEB podem contratar via concessão pública para programas nacionais de monitoramento de safra e segurança alimentar, com dados abertos para pesquisa.

**3. Métrica de impacto:**

Se o AgroSat-1 operar com 99% de disponibilidade por 1 ano (vs. 85% sem monitoramento inteligente): aproximadamente **12 milhões de hectares monitorados continuamente** no Cerrado e Matopiba, fornecendo imagens NDVI semanais para ~8.000 produtores rurais, validando índices para ~3.500 apólices de seguro agrícola e reduzindo perdas por decisão com dado ruim em estimados **R$ 180 milhões** na cadeia do agronegócio.

**4. Modelo de negócio:**

**SaaS B2B** com três camadas:
- *Monitoramento como serviço:* assinatura mensal para operadoras de satélite com dashboard de saúde operacional e alertas em tempo real
- *Dados como serviço (DaaS):* acesso à API de telemetria processada e histórico de disponibilidade para plataformas agrícolas e seguradoras
- *Concessão pública:* parceria com AEB/EMBRAPA para programas governamentais de segurança alimentar e mapeamento de safra nacional

## Vídeo de demonstração
https://youtu.be/xl58VBKGWUc