# DeFi Alpha Hunter v2

Multi-Agent LLM DeFi alpha hunter con memoria persistente e scoring auto-migliorante. 10 agenti analizzano i mercati crypto tramite CoinGecko + DeFiLlama, ma a differenza della prima versione, QUESTA IMPARA dalle proprie previsioni e aggiusta i pesi di scoring nel tempo.

## 🚀 Features

- **10 Specialized Agents**: Ogni agente si concentra su un aspetto specifico (analisi tecnica, on-chain metrics, sentiment, macro, risk management, portfolio allocation)
- **Persistent Memory**: SQLite stores every prediction, its outcome after N days, and accuracy metrics
- **Adaptive Scoring**: I pesi di ogni agente si adattano in base all'accuratezza storica
- **LLM Agnostic**: Supporta OpenAI, Anthropic, Google, OpenRouter
- **Multi-sector Support**: DeFi, L1, L2, Meme, AI, Gaming, Infra, RWA
- **Configurable**: Tutto è definito in config.json

## 📁 Architecture

```
defi-alpha-hunter/
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
├── config.json
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── coingecko.py      # CoinGecko free API data
│   │   └── defillama.py      # DeFiLlama free API data
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base.py           # Base Agent class with persistence
│   │   ├── market_analyst.py # Technical analysis
│   │   ├── onchain_analyst.py # On-chain metrics
│   │   ├── sentiment_analyst.py # Social sentiment
│   │   ├── research_analyst.py # Macro + fundamentals
│   │   ├── trader.py         # Signal synthesis
│   │   ├── risk_manager.py   # Risk assessment
│   │   └── portfolio_mgr.py  # Final allocation
│   ├── memory/
│   │   ├── __init__.py
│   │   ├── store.py          # SQLite-based persistent memory
│   │   ├── scorer.py         # Adaptive scoring
│   │   └── reflect.py        # Self-reflection
│   ├── llm.py                # LLM abstraction layer
│   └── runner.py             # Main orchestrator
└── memory.db                 # SQLite file (auto-created, gitignored)
```

## 📊 How It Works

1. **Data Fetching**: CoinGecko + DeFiLlama APIs (free, no key needed)
2. **Agent Analysis**: 7 analyst agents generate signals with confidence scores
3. **Signal Synthesis**: Trader agent combines all signals into a trade thesis
4. **Risk Assessment**: Risk manager evaluates position sizing and stop-losses
5. **Portfolio Allocation**: Portfolio manager produces final allocation
6. **Memory Update**: Outcomes are stored and weights are adjusted

## 🛠️ Requirements

```txt
requests>=2.31
pydantic>=2.0
openai>=1.0
anthropic>=0.20
google-genai>=0.1
```

## 🎮 Usage

```python
from defi_alpha_hunter.runner import Hunter

hunter = Hunter(config_path="config.json")
result = hunter.run()
print(result.allocation)
```

## 📋 Output

```json
{
  "timestamp": "2026-04-08T09:15:00Z",
  "analysts_votes": {
    "market_analyst": {"BTC": 0.8, "ETH": 0.6},
    "onchain_analyst": {"UNI": 0.7}
  },
  "confidence": 0.75,
  "final_allocation": {
    "BTC": 0.4,
    "ETH": 0.3,
    "UNI": 0.2,
    "USDC": 0.1
  },
  "signals": [...]
}
```

## ⚡ Why This Version?

A differenza della v1, questa versione:
- **Impara dagli errori**: Ogni previsione viene memorizzata e l'accuratezza calcola i pesi
- **Auto-migliorante**: Gli analyst scarsi perdono peso, quelli bravi guadagnano influenza
- **Persistente**: La memoria sopravvive tra le esecuzioni
- **Riflessiva**: Analisi mensile dei pattern di errore

## 📄 License

MIT - Open source e modificabile.