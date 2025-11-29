"""Example: Wallet integration and balance checking"""

from zektra import ZektraGateway
from zektra.payment import WalletManager

# Option 1: Initialize with wallet address and private key
gateway = ZektraGateway(
    wallet_address="0x...",  # Your wallet address
    private_key="0x..."       # Your private key (keep secure!)
)

# Check wallet balance
print("Checking wallet balance...")
eth_balance = gateway.get_wallet_balance()
print(f"ETH Balance: {eth_balance} ETH")

# Check ZEKTRA token balance (if token address configured)
try:
    zektra_balance = gateway.get_wallet_balance(token="ZEKTRA")
    print(f"ZEKTRA Balance: {zektra_balance} ZEKTRA")
except Exception as e:
    print(f"Could not check ZEKTRA balance: {e}")

# Option 2: Use pre-configured wallet manager
wallet = WalletManager(
    wallet_address="0x...",
    private_key="0x..."
)

gateway2 = ZektraGateway(wallet=wallet)

