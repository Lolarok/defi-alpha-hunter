# On-Chain Analyst Agent
from .base import BaseAgent, AgentSignal, AgentType

class OnchainAnalyst(BaseAgent):
    def __init__(self, 
                 config: Dict[str, Any],
                 memory: Optional['MemoryStore'] = None):
        super().__init__(AgentType.ONCHAIN, config, memory)
    
    def analyze(self, 
                data: Dict[str, Any], 
                context: Dict[str, Any]) -> List[AgentSignal]:
        """Analyze on-chain metrics and generate signals"""
        signals = []
        
        # Get TVL data
        tvl_data = data.get("tvl", {})
        
        for protocol, metrics in tvl_data.items():
            try:
                # Check for unusual TVL changes
                tvl_change = metrics.get("tvl_change_24h", 0)
                
                if tvl_change > 10.0:  # Significant inflow
                    signal = AgentSignal(
                        agent_type=self.agent_type,
                        token=protocol,
                        signal=1.0,
                        confidence=0.8,
                        reasoning=f"TVL increased by {tvl_change:.2f}% in 24h",
                        timestamp=datetime.now()
                    )
                    self.save_signal(signal)
                    signals.append(signal)
                elif tvl_change < -10.0:  # Significant outflow
                    signal = AgentSignal(
                        agent_type=self.agent_type,
                        token=protocol,
                        signal=0.0,
                        confidence=0.8,
                        reasoning=f"TVL decreased by {abs(tvl_change):.2f}% in 24h",
                        timestamp=datetime.now()
                    )
                    self.save_signal(signal)
                    signals.append(signal)
                    
            except Exception:
                continue
        
        return signals