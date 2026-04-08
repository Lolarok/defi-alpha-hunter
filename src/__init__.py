# DeFi Alpha Hunter v2 - Package initialization
__version__ = "2.0.0"

from .data.coingecko import CoinGeckoClient
from .data.defillama import DeFiLlamaClient
from .agents import *
from .memory import *
from .llm import LLMClient
from .runner import Hunter

__all__ = [
    "CoinGeckoClient",
    "DeFiLlamaClient",
    "BaseAgent", "MarketAnalyst", "OnchainAnalyst", 
    "SentimentAnalyst", "ResearchAnalyst", "Trader", 
    "RiskManager", "PortfolioMgr",
    "MemoryStore", "AdaptiveScorer", "SelfReflector",
    "LLMClient",
    "Hunter"
]