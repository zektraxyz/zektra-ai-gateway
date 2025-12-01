"""Basic example: Query DeepSeek with Solana payment"""

from zektra import ZektraGateway

# Initialize gateway
# Make sure to set DEEPSEEK_API_KEY, SOLANA_PRIVATE_KEY, SOLANA_WALLET_ADDRESS in .env
gateway = ZektraGateway()

# Query DeepSeek with ZEKTRA payment
print("Querying DeepSeek...")
response = gateway.query_deepseek(
    prompt="Explain zero-knowledge proofs in simple terms",
    payment_token="ZEKTRA",
    amount=0.1
)

print("\n" + "="*60)
print("Response:")
print("="*60)
print(response.text)
print("\n" + "="*60)
print(f"Model: {response.model}")
print(f"Usage: {response.usage}")

