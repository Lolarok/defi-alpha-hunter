# CoinGecko API Client
import requests
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

class CoinGeckoClient:
    def __init__(self, base_url: str = "https://api.coingecko.com/api/v3", timeout: int = 30):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
    
    def _request(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint}"
        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def get_market_data(self, vs_currency: str = "usd") -> Dict[str, Any]:
        """Fetch global market data"""
        return self._request("global")
    
    def get_coins_markets(self, 
                         vs_currency: str = "usd",
                         per_page: int = 100,
                         page: int = 1) -> Dict[str, Any]:
        """Get top coins by market cap"""
        params = {
            "vs_currency": vs_currency,
            "per_page": per_page,
            "page": page,
            "order": "market_cap_desc"
        }
        return self._request("coins/markets", params)
    
    def get_coin_by_id(self, 
                      id: str, 
                      vs_currency: str = "usd",
                      localization: bool = False) -> Dict[str, Any]:
        """Get coin data by ID"""
        params = {"vs_currency": vs_currency, "localization": "false"}
        return self._request(f"coins/{id}", params)
    
    def get_coin_history(self, 
                        id: str, 
                        date: str, 
                        vs_currency: str = "usd") -> Dict[str, Any]:
        """Get historical data for a coin"""
        return self._request(f"coins/{id}/history", {"vs_currency": vs_currency, "date": date})
    
    def get_coin_market_chart(self, 
                            id: str, 
                            vs_currency: str = "usd",
                            days: int = 30) -> Dict[str, Any]:
        """Get market chart for a coin"""
        return self._request(f"coins/{id}/market_chart", 
                           {"vs_currency": vs_currency, "days": days})
    
    def get_social_stats(self, id: str) -> Optional[Dict[str, Any]]:
        """Get social media stats for a coin"""
        try:
            return self._request(f"coins/{id}/social_stats")
        except:
            return None
    
    def close(self):
        self.session.close()