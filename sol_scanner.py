import requests
from config import HELIUS_API
from utils import format_alert

async def scan_sol_tokens():
    url = f"https://api.helius.xyz/v0/addresses/solana/new-tokens?api-key={HELIUS_API}"
    res = requests.get(url).json()
    tokens = []
    for item in res.get("tokens", []):
        alert = format_alert("SOL", item["name"], item["symbol"], item["tokenAddress"])
        tokens.append(alert)
    return tokens
