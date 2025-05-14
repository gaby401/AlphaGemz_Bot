import requests
from config import ETHERSCAN_API
from utils import format_alert
from utils_honeypot import check_eth_contract_safety

async def scan_eth_tokens():
    url = f"https://api.etherscan.io/api?module=account&action=tokentx&address=0x0000000000000000000000000000000000001004&apikey={ETHERSCAN_API}"
    res = requests.get(url).json()
    tokens = []
    seen = set()
    for tx in res['result']:
        contract = tx['contractAddress']
        if contract in seen:
            continue
        seen.add(contract)
        if tx['tokenSymbol'] and tx['tokenName']:
            safety = check_eth_contract_safety(contract)
            alert = format_alert("ETH", tx['tokenName'], tx['tokenSymbol'], contract)
            alert += "\n\nRisk Flags:\n" + "\n".join(safety)
            tokens.append(alert)
    return tokens
