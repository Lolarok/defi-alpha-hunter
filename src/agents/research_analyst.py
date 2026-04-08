# Research Analyst Agent
from .base import BaseAgent, AgentSignal, AgentType

class ResearchAnalyst(BaseAgent):
    def __init__(self, 
                 config: Dict[str, Any],
                 memory: Optional['MemoryStore'] = None):
        super().__init__(AgentType.RESEARCH, config, memory)
    
    def analyze(self, 
                data: Dict[str, Any], 
                context: Dict[str, Any]) -> List[AgentSignal]:
        """Analyze fundamentals and macro trends"""
        signals = []
        
        # Get protocol data
        protocols = data.get("protocols", {})
        
        for protocol, info in protocols.items():
            try:
                # Check fundamentals
                if info.get("audit", False):
                    signal = AgentSignal(
                        agent_type=self.agent_type,
                        token=protocol,
                        signal=1.0,
                        confidence=0.8,
                        reasoning="Protocol has been audited",
                        timestamp=datetime.now()
                    )
                    self.save_signal(signal)
                    signals.append(signal)
                
                # Check for recent news
                if info.get("news", []):
                    signal = AgentSignal(
                        agent_type=self.agent_type,
                        token=protocol,
                        signal=1.0,
                        confidence=0.7,
                        reasoning="Positive recent news",
                        timestamp=datetime.now()
                    )
                    self.save_signal(signal)
                    signals.append(signal)
                    
            except Exception:
                continue
        
        return signals