# DeFiLlama API Client
import requests
from typing import Dict, Any, Optional

class DeFiLlamaClient:
    def __init__(self, base_url: str = "https://api.llama.fi", timeout: int = 30):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
    
    def _request(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint}"
        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def get_tvl(self, chain: Optional[str] = None) -> Dict[str, Any]:
        """Get TVL data for all chains or specific chain"""
        endpoint = "chains" if chain is None else f"chain/{chain}"
        return self._request(endpoint)
    
    def get_protocols(self) -> Dict[str, Any]:
        """Get list of all protocols"""
        return self._request("protocols")
    
    def get_protocol(self, name: str) -> Dict[str, Any]:
        """Get data for a specific protocol"""
        return self._request(f"protocol/{name}")
    
    def get_protocol_history(self, name: str) -> Dict[str, Any]:
        """Get historical data for a protocol"""
        return self._request(f"protocol/{name}/history")
    
    def get_liquidity_wallets(self, address: str) -> Dict[str, Any]:
        """Get liquidity wallet data"""
        return self._request(f"wallets/{address}")
    
    def close(self):
        self.session.close()