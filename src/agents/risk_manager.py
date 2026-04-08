# Risk Manager Agent
from .base import BaseAgent, AgentSignal, AgentType

class RiskManager(BaseAgent):
    def __init__(self, 
                 config: Dict[str, Any],
                 memory: Optional['MemoryStore'] = None):
        super().__init__(AgentType.RISK, config, memory)
    
    def analyze(self, 
                data: Dict[str, Any], 
                context: Dict[str, Any]) -> List[AgentSignal]:
        """Assess risk and generate risk management signals"""
        signals = []
        
        # Check overall market conditions
        fear_greed_index = data.get("fear_greed_index", 50)
        volatility_index = data.get("volatility_index", 20)
        
        # High greed = potential correction
        if fear_greed_index > 75:
            signal = AgentSignal(
                agent_type=self.agent_type,
                token="MARKET",
                signal=0.0,
                confidence=0.7,
                reasoning=f"High greed index: {fear_greed_index}",
                timestamp=datetime.now()
            )
            self.save_signal(signal)
            signals.append(signal)
        
        # High volatility = risk off
        if volatility_index > 30:
            signal = AgentSignal(
                agent_type=self.agent_type,
                token="MARKET",
                signal=0.0,
                confidence=0.6,
                reasoning=f"High volatility: {volatility_index}",
                timestamp=datetime.now()
            )
            self.save_signal(signal)
            signals.append(signal)
        
        return signals