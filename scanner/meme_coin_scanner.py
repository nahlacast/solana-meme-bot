# meme_coin_scanner.py

def is_rugpull(token_data):
    """
    Very basic rugpull detection logic
    """
    liquidity = token_data.get("liquidity", 0)
    creator_hold = token_data.get("creator_hold_percent", 100)
    mintable = token_data.get("mintable", True)
    freeze_authority = token_data.get("freeze_authority", True)

    if liquidity < 5:
        return True
    if creator_hold > 50:
        return True
    if mintable:
        return True
    if freeze_authority:
        return True

    return False

def scan_token(token_data):
    """
    Example logic to process a single token
    """
    print(f"Scanning {token_data['symbol']}...")

    if is_rugpull(token_data):
        print(f"🚫 Skipping {token_data['symbol']} — rugpull risk detected.")
        return False

    print(f"✅ {token_data['symbol']} passed rugpull check.")
    return True

# Example: Simulated token data
example_token = {
    "symbol": "$WAGMI",
    "liquidity": 1.5,
    "creator_hold_percent": 80,
    "mintable": True,
    "freeze_authority": True
}

# Simulate scanning
scan_token(example_token)

