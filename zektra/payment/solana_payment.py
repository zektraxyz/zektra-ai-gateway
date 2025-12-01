"""Example: Using Zektra AI Gateway with Solana payments (Pump.fun token)"""

import asyncio
from zektra import ZektraGateway

async def main():
    # Initialize gateway with Solana configuration
    # Make sure to set SOLANA_PRIVATE_KEY, SOLANA_WALLET_ADDRESS, and TOKEN_MINT in .env
    gateway = ZektraGateway()

    # Query DeepSeek with ZEKTRA token payment (Solana SPL)
    print("Querying DeepSeek with ZEKTRA token payment...")
    
    response = gateway.query_deepseek(
        prompt="Explain zero-knowledge proofs",
        payment_token="ZEKTRA",  # Will use Solana SPL token
        amount=0.1  # ZEKTRA tokens
    )

    print("\n" + "="*60)
    print("Response:")
    print("="*60)
    print(response.text)
    print("\n" + "="*60)
    print(f"Model: {response.model}")
    print(f"Transaction: {response.metadata.get('transaction_hash') if response.metadata else 'N/A'}")

if __name__ == "__main__":
    asyncio.run(main())





