# Trader Agent
from .base import BaseAgent, AgentSignal, AgentType

class Trader(BaseAgent):
    def __init__(self, 
                 config: Dict[str, Any],
                 memory: Optional['MemoryStore'] = None):
        super().__init__(AgentType.TRADER, config, memory)
    
    def analyze(self, 
                data: Dict[str, Any], 
                context: Dict[str, Any]) -> List[AgentSignal]:
        """Synthesize all signals into trade signals"""
        signals = []
        
        # Get all signals from other agents
        all_signals = context.get("all_signals", {})
        
        # Simple voting mechanism
        token_scores = {}
        
        for agent_signals in all_signals.values():
            for signal in agent_signals:
                token = signal.token
                score = token_scores.get(token, 0)
                token_scores[token] = score + signal.signal * signal.confidence
        
        # Generate trade signals based on score
        for token, score in token_scores.items():
            if score > 2.0:  # Strong buy
                signal = AgentSignal(
                    agent_type=self.agent_type,
                    token=token,
                    signal=1.0,
                    confidence=min(0.9, score / 5.0),
                    reasoning=f"Consensus buy signal from multiple agents (score: {score:.2f})",
                    timestamp=datetime.now()
                )
                self.save_signal(signal)
                signals.append(signal)
            elif score < -2.0:  # Strong sell
                signal = AgentSignal(
                    agent_type=self.agent_type,
                    token=token,
                    signal=0.0,
                    confidence=min(0.9, abs(score) / 5.0),
                    reasoning=f"Consensus sell signal from multiple agents (score: {score:.2f})",
                    timestamp=datetime.now()
                )
                self.save_signal(signal)
                signals.append(signal)
        
        return signals