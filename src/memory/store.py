# SQLite-based Persistent Memory
import sqlite3
from datetime import datetime
from typing import Dict, Any, Optional, List
import json
from . import AgentSignal

class MemoryStore:
    def __init__(self, db_path: str = "memory.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Predictions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_type TEXT,
                    token TEXT,
                    signal REAL,
                    confidence REAL,
                    reasoning TEXT,
                    timestamp TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Outcomes table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS outcomes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prediction_id INTEGER,
                    actual_return REAL,
                    days_elapsed INTEGER,
                    was_correct INTEGER,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (prediction_id) REFERENCES predictions (id)
                )
            ''')
            
            # Accuracy history
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS accuracy_history (
                    agent_type TEXT,
                    total_predictions INTEGER,
                    correct_predictions INTEGER,
                    accuracy REAL,
                    weight REAL,
                    recorded_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
    
    def store_signal(self, signal: AgentSignal):
        """Store a prediction signal"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO predictions (agent_type, token, signal, confidence, reasoning, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                signal.agent_type.value,
                signal.token,
                signal.signal,
                signal.confidence,
                signal.reasoning,
                signal.timestamp.isoformat()
            ))
            conn.commit()
    
    def store_outcome(self, prediction_id: int, actual_return: float, days_elapsed: int, was_correct: bool):
        """Store the outcome of a prediction"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO outcomes (prediction_id, actual_return, days_elapsed, was_correct)
                VALUES (?, ?, ?, ?)
            ''', (prediction_id, actual_return, days_elapsed, was_correct))
            conn.commit()
    
    def get_prediction_history(self, agent_type: str, days: int = 30) -> List[Dict[str, Any]]:
        """Get prediction history for an agent"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)
            
            cursor.execute('''
                SELECT * FROM predictions 
                WHERE agent_type = ? AND timestamp > ?
            ''', (agent_type, datetime.fromtimestamp(cutoff).isoformat()))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def calculate_accuracy(self, agent_type: str, days: int = 30) -> Optional[Dict[str, Any]]:
        """Calculate accuracy for an agent"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get correct predictions
            cursor.execute('''
                SELECT COUNT(*) as correct 
                FROM predictions p
                JOIN outcomes o ON p.id = o.prediction_id
                WHERE p.agent_type = ? 
                AND p.timestamp > ?
                AND o.was_correct = 1
            ''', (agent_type, datetime.now().isoformat()))
            
            correct_row = cursor.fetchone()
            correct = correct_row[0] if correct_row else 0
            
            # Get total predictions
            cursor.execute('''
                SELECT COUNT(*) as total
                FROM predictions 
                WHERE agent_type = ? AND timestamp > ?
            ''', (agent_type, datetime.now().isoformat()))
            
            total_row = cursor.fetchone()
            total = total_row[0] if total_row else 0
            
            if total == 0:
                return None
            
            accuracy = correct / total
            
            return {
                "agent_type": agent_type,
                "total_predictions": total,
                "correct_predictions": correct,
                "accuracy": accuracy
            }
    
    def update_agent_weight(self, agent_type: str, weight: float):
        """Update the weight for an agent"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO accuracy_history (agent_type, total_predictions, correct_predictions, accuracy, weight)
                VALUES (?, ?, ?, ?, ?)
            ''', (agent_type, 0, 0, 0, weight))
            conn.commit()
    
    def get_latest_weights(self) -> Dict[str, float]:
        """Get the latest weights for all agents"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT agent_type, weight 
                FROM accuracy_history 
                WHERE recorded_at = (
                    SELECT MAX(recorded_at) FROM accuracy_history
                )
            ''')
            
            rows = cursor.fetchall()
            return {row["agent_type"]: row["weight"] for row in rows}