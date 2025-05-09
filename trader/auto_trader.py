# trader/auto_trader.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scanner')))
import requests
from scanner.meme_coin_scanner import scan_token

def fetch_pump_tokens():
    try:
        response = requests.get("https://pump.fun/api/token/list", timeout=10)
        token_list = response.json()
        tokens = []

        for token in token_list:
            token_data = {
                "symbol": token.get("name", "$UNKNOWN"),
                "liquidity": token.get("liquidity", 0) / 1_000_000_000,  # convert lamports to SOL
                "creator_hold_percent": token.get("creator_holding_percent", 100),
                "mintable": token.get("mint_authority", None) is not None,
                "freeze_authority": token.get("freeze_authority", None)
            }
            tokens.append(token_data)

        return tokens

    except Exception as e:
        print(f"❌ Failed to fetch tokens: {e}")
        return []

def run_autonomous_trader():
    print("🧠 Scanning for new meme coins from Pump.fun...")
    tokens = fetch_pump_tokens()

    for token in tokens[:10]:  # limit for now to avoid overload
        print(f"\n--- Checking {token['symbol']} ---")
        if not scan_token(token):
            continue

        print(f"📈 Executing trade for 0.2 SOL of {token['symbol']}")
        # Here you'd replace with a real call like: jupiter_client.execute_trade(...)