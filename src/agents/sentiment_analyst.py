# Sentiment Analyst Agent
from .base import BaseAgent, AgentSignal, AgentType

class SentimentAnalyst(BaseAgent):
    def __init__(self, 
                 config: Dict[str, Any],
                 memory: Optional['MemoryStore'] = None):
        super().__init__(AgentType.SENTIMENT, config, memory)
    
    def analyze(self, 
                data: Dict[str, Any], 
                context: Dict[str, Any]) -> List[AgentSignal]:
        """Analyze social sentiment and generate signals"""
        signals = []
        
        # Get social stats
        social_stats = data.get("social_stats", {})
        
        for token, stats in social_stats.items():
            try:
                # Check social engagement
                twitter_followers = stats.get("twitter_followers", 0)
                twitter_sentiment = stats.get("twitter_sentiment", 0)  # -1 to 1
                reddit_activity = stats.get("reddit_activity", 0)
                
                # Positive sentiment with high engagement
                if twitter_sentiment > 0.5 and twitter_followers > 10000:
                    signal = AgentSignal(
                        agent_type=self.agent_type,
                        token=token,
                        signal=1.0,
                        confidence=min(0.9, 0.5 + twitter_sentiment),
                        reasoning=f"Positive social sentiment: {twitter_sentiment:.2f} with {twitter_followers:,} followers",
                        timestamp=datetime.now()
                    )
                    self.save_signal(signal)
                    signals.append(signal)
                elif twitter_sentiment < -0.5:  # Negative sentiment
                    signal = AgentSignal(
                        agent_type=self.agent_type,
                        token=token,
                        signal=0.0,
                        confidence=min(0.9, 0.5 + abs(twitter_sentiment)),
                        reasoning=f"Negative social sentiment: {twitter_sentiment:.2f}",
                        timestamp=datetime.now()
                    )
                    self.save_signal(signal)
                    signals.append(signal)
                    
            except Exception:
                continue
        
        return signals