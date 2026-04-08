# Main Orchestrator
import json
from datetime import datetime
from typing import Dict, Any, Optional
import sqlite3
import pandas as pd
import numpy as np

from .data.coingecko import CoinGeckoClient
from .data.defillama import DeFiLlamaClient
from .agents import *
from .memory import MemoryStore
from .llm import LLMClient

class Hunter:
    def __init__(self, 
                 config_path: str = "config.json",
                 db_path: str = "memory.db"):
        self.config = self.load_config(config_path)
        self.db_path = db_path
        
        # Initialize clients
        self.cg_client = CoinGeckoClient()
        self.llama_client = DeFiLlamaClient()
        
        # Initialize memory
        self.memory = MemoryStore(db_path)
        
        # Initialize agents
        self.agents = self.init_agents()
        
        # Initialize LLM client
        self.llm = LLMClient(self.config)
        
        # Store latest data and results
        self.latest_data: Dict[str, Any] = {}
        self.final_allocation: Optional[Dict[str, float]] = None
    
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Return default config if file not found
            return {
                "data_sources": {"coingecko": {"enabled": True}, "defillama": {"enabled": True}},
                "sectors": ["DeFi", "L1", "L2", "Meme", "AI", "Gaming", "Infra", "RWA"],
                "watchlist": {"top_by_market_cap": 100},
                "scoring": {"weights": {}, "min_confidence": 0.6},
                "memory": {"db_path": "memory.db"},
                "run": {"history_days": 30}
            }
    
    def init_agents(self) -> Dict[str, BaseAgent]:
        """Initialize all agents"""
        agents = {}
        
        # Create agents based on config
        for agent_type_str, weight in self.config["scoring"]["weights"].items():
            agent_type = AgentType(agent_type_str)
            
            if agent_type == AgentType.MARKET:
                agents[agent_type] = MarketAnalyst(self.config, self.memory)
            elif agent_type == AgentType.ONCHAIN:
                agents[agent_type] = OnchainAnalyst(self.config, self.memory)
            elif agent_type == AgentType.SENTIMENT:
                agents[agent_type] = SentimentAnalyst(self.config, self.memory)
            elif agent_type == AgentType.RESEARCH:
                agents[agent_type] = ResearchAnalyst(self.config, self.memory)
            elif agent_type == AgentType.TRADER:
                agents[agent_type] = Trader(self.config, self.memory)
            elif agent_type == AgentType.RISK:
                agents[agent_type] = RiskManager(self.config, self.memory)
            elif agent_type == AgentType.PORTFOLIO:
                agents[agent_type] = PortfolioMgr(self.config, self.memory)
        
        return agents
    
    def fetch_data(self) -> Dict[str, Any]:
        """Fetch all necessary data from APIs"""
        data = {}
        
        try:
            # Market data
            if self.config["data_sources"]["coingecko"]["enabled"]:
                coins = self.cg_client.get_coins_markets(per_page=100)
                data["coins"] = coins
                
                # Social stats
                social_stats = {}
                for coin in coins[:50]:  # Limit to top 50 for social
                    try:
                        stats = self.cg_client.get_social_stats(coin["id"])
                        if stats:
                            social_stats[coin["symbol"]] = stats
                    except:
                        pass
                data["social_stats"] = social_stats
            
            # On-chain data
            if self.config["data_sources"]["defillama"]["enabled"]:
                protocols = self.llama_client.get_protocols()
                data["protocols"] = {p["name"]: p for p in protocols}
                
                tvl = self.llama_client.get_tvl()
                data["tvl"] = tvl.get("data", {})
            
        except Exception as e:
            print(f"Error fetching data: {e}")
        
        self.latest_data = data
        return data
    
    def run_agents(self, data: Dict[str, Any]) -> Dict[str, List[AgentSignal]]:
        """Run all agents on fetched data"""
        all_signals = {}
        
        # Clear previous signals
        for agent in self.agents.values():
            agent.reset()
        
        # Run each agent
        for agent_type, agent in self.agents.items():
            try:
                signals = agent.analyze(data, {"all_signals": all_signals})
                all_signals[agent_type] = signals
            except Exception as e:
                print(f"Error running {agent_type.value} agent: {e}")
        
        return all_signals
    
    def run(self) -> Dict[str, Any]:
        """Main execution pipeline"""
        print("Starting DeFi Alpha Hunter run...")
        
        # Step 1: Fetch data
        print("1. Fetching data...")
        data = self.fetch_data()
        
        # Step 2: Run all agents
        print("2. Running analysis agents...")
        all_signals = self.run_agents(data)
        
        # Step 3: Run trader agent
        print("3. Synthesizing signals...")
        if AgentType.TRADER in self.agents:
            trader_signals = self.agents[AgentType.TRADER].analyze(data, {"all_signals": all_signals})
        else:
            trader_signals = []
        
        # Step 4: Run risk manager
        print("4. Assessing risk...")
        if AgentType.RISK in self.agents:
            risk_signals = self.agents[AgentType.RISK].analyze(data, {"all_signals": all_signals})
        else:
            risk_signals = []
        
        # Step 5: Run portfolio manager
        print("5. Generating portfolio allocation...")
        if AgentType.PORTFOLIO in self.agents:
            portfolio_context = {
                "all_signals": all_signals,
                "trade_signals": {s.token: s for s in trader_signals}
            }
            portfolio_signals = self.agents[AgentType.PORTFOLIO].analyze(data, portfolio_context)
            self.final_allocation = portfolio_context.get("portfolio_allocation")
        else:
            portfolio_signals = []
        
        # Step 6: Store signals in memory
        print("6. Updating memory...")
        for agent_signals in all_signals.values():
            for signal in agent_signals:
                self.memory.store_signal(signal)
        
        # Step 7: Update agent weights (monthly)
        # Would implement adaptive scoring here
        
        print("Run completed!")
        
        return self.generate_report()
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate final report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "data_fetched": self.latest_data,
            "signals": {},
            "allocation": self.final_allocation,
            "summary": {
                "total_signals": 0,
                "bullish_signals": 0,
                "bearish_signals": 0
            }
        }
        
        # Collect signals from all agents
        for agent_type, agent in self.agents.items():
            report["signals"][agent_type.value] = [
                s.to_dict() for s in agent.get_signals()
            ]
            for signal in agent.get_signals():
                report["summary"]["total_signals"] += 1
                if signal.signal > 0.5:
                    report["summary"]["bullish_signals"] += 1
                else:
                    report["summary"]["bearish_signals"] += 1
        
        return report
    
    def save_output(self, output_path: str = "output/signals.json"):
        """Save output to JSON file"""
        report = self.generate_report()
        
        import os
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report