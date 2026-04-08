# Portfolio Manager Agent
from .base import BaseAgent, AgentSignal, AgentType

class PortfolioMgr(BaseAgent):
    def __init__(self, 
                 config: Dict[str, Any],
                 memory: Optional['MemoryStore'] = None):
        super().__init__(AgentType.PORTFOLIO, config, memory)
    
    def analyze(self, 
                data: Dict[str, Any], 
                context: Dict[str, Any]) -> List[AgentSignal]:
        """Generate final portfolio allocation"""
        signals = []
        
        # Get trade signals
        trade_signals = context.get("trade_signals", {})
        
        # Simple portfolio construction
        allocation = {}
        total_score = 0
        
        for signal in trade_signals.values():
            if signal.signal > 0.5:  # Bullish
                allocation[signal.token] = allocation.get(signal.token, 0) + signal.confidence
                total_score += signal.confidence
        
        # Normalize
        if total_score > 0:
            for token in allocation:
                allocation[token] = allocation[token] / total_score
        
        # Generate signal
        signal = AgentSignal(
            agent_type=self.agent_type,
            token="PORTFOLIO",
            signal=1.0 if total_score > 0 else 0.0,
            confidence=min(0.9, total_score / 5.0),
            reasoning=f"Portfolio allocation generated for {len(allocation)} tokens",
            timestamp=datetime.now()
        )
        self.save_signal(signal)
        signals.append(signal)
        
        # Store allocation in context for output
        context["portfolio_allocation"] = allocation
        
        return signals