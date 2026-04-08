# Adaptive Scoring System
import sqlite3
from datetime import datetime
from typing import Dict, Any, Optional

class AdaptiveScorer:
    def __init__(self, memory: 'MemoryStore', learning_rate: float = 0.3, decay_factor: float = 0.7):
        self.memory = memory
        self.learning_rate = learning_rate
        self.decay_factor = decay_factor
    
    def calculate_new_weight(self, agent_type: str, current_weight: float, accuracy: float) -> float:
        """Calculate new weight based on accuracy"""
        # If accuracy is high, increase weight
        if accuracy > 0.6:
            adjustment = (accuracy - 0.5) * self.learning_rate
            new_weight = current_weight * (1 + adjustment)
        # If accuracy is low, decrease weight
        elif accuracy < 0.4:
            adjustment = (0.5 - accuracy) * self.learning_rate
            new_weight = current_weight * (1 - adjustment)
        else:
            new_weight = current_weight
        
        # Apply decay factor to prevent weights from growing too large
        new_weight = new_weight * self.decay_factor
        
        return max(0.1, min(new_weight, 2.0))  # Clamp between 0.1 and 2.0
    
    def update_weights(self, config: Dict[str, Any]):
        """Update all agent weights based on recent performance"""
        weights = {}
        
        for agent_type in config["scoring"]["weights"].keys():
            accuracy_data = self.memory.calculate_accuracy(agent_type)
            if accuracy_data:
                current_weight = config["scoring"]["weights"][agent_type]
                new_weight = self.calculate_new_weight(
                    agent_type, 
                    current_weight, 
                    accuracy_data["accuracy"]
                )
                weights[agent_type] = new_weight
        
        return weights