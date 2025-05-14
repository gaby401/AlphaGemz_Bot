import requests
from config import ETHERSCAN_API

def check_eth_contract_safety(contract_address):
    risk_flags = []

    # 1. Check if contract is renounced
    url = f"https://api.etherscan.io/api?module=contract&action=getsourcecode&address={contract_address}&apikey={ETHERSCAN_API}"
    response = requests.get(url).json()
    result = response.get("result", [{}])[0]

    if result.get("ContractName"):
        source_code = result.get("SourceCode", "")
        if "Ownable" in source_code and "renounceOwnership" in source_code:
            risk_flags.append("✅ Contract Renounce Function Detected")
        else:
            risk_flags.append("❌ No Renounce Function Detected")
    else:
        risk_flags.append("❌ No Verified Source Code")

    # 2. Check for possible blacklist or honeypot keywords
    blacklist_keywords = ["addBlacklist", "setBlacklist", "isBlacklisted", "blacklist"]
    if any(keyword in result.get("SourceCode", "") for keyword in blacklist_keywords):
        risk_flags.append("⚠️ Blacklist Function Detected")

    return risk_flags
