# trader/jupiter_client.py

import requests
import base64
import json
import os
from solders.keypair import Keypair
from solana.rpc.api import Client
from solana.transaction import Transaction
from solders.transaction import VersionedTransaction
from solders.signature import Signature
from solders.pubkey import Pubkey

QUICKNODE_RPC = os.getenv("QUICKNODE_RPC")
PRIVATE_KEY_JSON = os.getenv("PRIVATE_KEY_JSON")

wallet_keypair = Keypair.from_bytes(bytearray(json.loads(PRIVATE_KEY_JSON)))
solana_client = Client(QUICKNODE_RPC)

def get_best_quote(input_mint, output_mint, amount):
    url = "https://lite-api.jup.ag/v1/quote"
    params = {
        "inputMint": input_mint,
        "outputMint": output_mint,
        "amount": str(int(amount * 1_000_000_000)),  # SOL to lamports
        "slippage": 1,
    }
    response = requests.get(url, params=params)
    return response.json()

def get_swap_transaction(input_mint, output_mint, amount, user_pubkey):
    quote = get_best_quote(input_mint, output_mint, amount)
    route = quote['data'][0]

    tx_request = {
        "route": route,
        "userPublicKey": str(user_pubkey),
        "wrapUnwrapSOL": True,
        "feeAccount": None,
        "asLegacyTransaction": False
    }

    response = requests.post("https://lite-api.jup.ag/v1/swap", json=tx_request)
    tx_b64 = response.json()["swapTransaction"]
    return base64.b64decode(tx_b64)

def execute_trade(input_mint, output_mint, amount):
    print(f"🟡 Preparing swap: {amount} SOL for {output_mint}")
    swap_tx = get_swap_transaction(input_mint, output_mint, amount, wallet_keypair.pubkey())
    tx = VersionedTransaction.deserialize(swap_tx)
    tx.sign([wallet_keypair])

    print("📤 Sending transaction...")
    result = solana_client.send_raw_transaction(tx.serialize())
    print(f"✅ Swap submitted! Tx Signature: {result['result']}")
    return result['result']