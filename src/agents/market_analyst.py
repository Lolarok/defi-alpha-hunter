# Market Analyst Agent
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List
from .base import BaseAgent, AgentSignal, AgentType

class MarketAnalyst(BaseAgent):
    def __init__(self, 
                 config: Dict[str, Any],
                 memory: Optional['MemoryStore'] = None):
        super().__init__(AgentType.MARKET, config, memory)
    
    def analyze(self, 
                data: Dict[str, Any], 
                context: Dict[str, Any]) -> List[AgentSignal]:
        """Analyze market trends and generate signals"""
        signals = []
        
        # Get top coins by market cap
        coins = data.get("coins", [])[:20]  # Top 20 only
        
        for coin in coins:
            try:
                # Calculate technical indicators
                trends = coin.get("price_change_percentage_24h", 0)
                trends_7d = coin.get("price_change_percentage_7d", 0)
                
                # Simple momentum strategy
                if trends > 5.0:
                    signal = AgentSignal(
                        agent_type=self.agent_type,
                        token=coin["symbol"],
                        signal=1.0,
                        confidence=0.7 + (trends / 100.0),
                        reasoning=f"Strong 24h momentum: {trends:.2f}%",
                        timestamp=datetime.now()
                    )
                    self.save_signal(signal)
                    signals.append(signal)
                elif trends_7d > 10.0:
                    signal = AgentSignal(
                        agent_type=self.agent_type,
                        token=coin["symbol"],
                        signal=1.0,
                        confidence=0.6,
                        reasoning=f"Strong 7d momentum: {trends_7d:.2f}%",
                        timestamp=datetime.now()
                    )
                    self.save_signal(signal)
                    signals.append(signal)
                elif trends < -5.0:
                    signal = AgentSignal(
                        agent_type=self.agent_type,
                        token=coin["symbol"],
                        signal=0.0,
                        confidence=0.7 + (abs(trends) / 100.0),
                        reasoning=f"Strong negative momentum: {trends:.2f}%",
                        timestamp=datetime.now()
                    )
                    self.save_signal(signal)
                    signals.append(signal)
                    
            except Exception as e:
                continue
        
        return signals