import requests

def validate_dexscreener_link(chain, contract):
    url = f"https://api.dexscreener.com/latest/dex/pairs/{chain}/{contract}"
    try:
        response = requests.get(url)
        return response.status_code == 200 and "pairs" in response.json()
    except:
        return False

def format_alert(chain, name, symbol, contract):
    chain_slug = 'ethereum' if chain == 'ETH' else 'solana'
    if validate_dexscreener_link(chain_slug, contract):
        link = f"https://dexscreener.com/{chain_slug}/{contract}"
    else:
        link = f"Dexscreener: Not available yet\nGeckoTerminal: https://www.geckoterminal.com/{chain_slug}/pools/{contract}"

    return f"""
New {chain} Token Detected!
Name: {name}
Symbol: {symbol}
CA: {contract}

{link}
"""
