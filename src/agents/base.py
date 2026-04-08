# Base Agent Class
import json
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum

class AgentType(Enum):
    MARKET = "market_analyst"
    ONCHAIN = "onchain_analyst"
    SENTIMENT = "sentiment_analyst"
    RESEARCH = "research_analyst"
    TRADER = "trader"
    RISK = "risk_manager"
    PORTFOLIO = "portfolio_mgr"

@dataclass
class AgentSignal:
    agent_type: AgentType
    token: str
    signal: float  # 0-1 confidence
    confidence: float
    reasoning: str
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        return data
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

class BaseAgent(ABC):
    def __init__(self, 
                 agent_type: AgentType, 
                 config: Dict[str, Any],
                 memory: Optional['MemoryStore'] = None):
        self.agent_type = agent_type
        self.config = config
        self.memory = memory
        self.signals: List[AgentSignal] = []
    
    @abstractmethod
    def analyze(self, 
                data: Dict[str, Any], 
                context: Dict[str, Any]) -> List[AgentSignal]:
        """Analyze data and generate signals"""
        pass
    
    def save_signal(self, signal: AgentSignal):
        self.signals.append(signal)
        
        # Store in memory if available
        if self.memory:
            self.memory.store_signal(signal)
    
    def get_signals(self) -> List[AgentSignal]:
        return self.signals
    
    def reset(self):
        self.signals = []
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_type": self.agent_type.value,
            "signals": [s.to_dict() for s in self.signals]
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)