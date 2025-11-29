# Zektra AI Gateway

**Version:** 0.1.0-beta  
**Status:** Beta - Production Ready

A Python gateway that connects AI services (DeepSeek, OpenAI, etc.) with crypto payments using $ZEKTRA tokens.

## Features

- 🔌 **AI Service Integration**: Connect to DeepSeek, OpenAI, Anthropic, and more
- 💰 **Crypto Payments**: Pay for AI queries using $ZEKTRA tokens
- 🔐 **Wallet Integration**: Support for Web3 wallets (MetaMask, WalletConnect)
- 📊 **Usage Tracking**: Monitor API usage and costs
- 🚀 **Production Ready**: Built for reliability and scale

## Installation

```bash
pip install zektra-ai-gateway
```

Or install from source:

```bash
git clone https://github.com/zektra/zektra-ai-gateway.git
cd zektra-ai-gateway
pip install -e .
```

## Quick Start

### Basic Usage

```python
from zektra import ZektraGateway

# Initialize gateway
gateway = ZektraGateway(
    wallet_address="0x...",
    private_key="0x..."  # Or use wallet connection
)

# Query DeepSeek with crypto payment
response = gateway.query_deepseek(
    prompt="Explain zero-knowledge proofs",
    payment_token="ZEKTRA",
    amount=0.1  # ZEKTRA tokens
)

print(response.text)
```

### With Wallet Connection

```python
from zektra import ZektraGateway
from zektra.wallet import connect_wallet

# Connect wallet (MetaMask, WalletConnect, etc.)
wallet = connect_wallet()

gateway = ZektraGateway(wallet=wallet)

# Query AI service
response = gateway.query(
    service="deepseek",
    prompt="What is homomorphic encryption?",
    payment_token="ZEKTRA"
)
```

### CLI Usage

```bash
# Set your API keys and wallet
export DEEPSEEK_API_KEY="your-key"
export ZEKTRA_WALLET_ADDRESS="0x..."
export ZEKTRA_PRIVATE_KEY="0x..."

# Query DeepSeek
zektra query deepseek "Explain ZK proofs" --payment ZEKTRA --amount 0.1

# List available services
zektra services list

# Check balance
zektra wallet balance
```

## Supported AI Services

- ✅ **DeepSeek** (Primary)
- ✅ **OpenAI** (GPT-4, GPT-3.5)
- ✅ **Anthropic** (Claude)
- 🔄 **Local LLMs** (Ollama) - Coming soon

## Payment Methods

- **$ZEKTRA Token** (Primary)
- **USDC** (Stablecoin)
- **ETH** (Ethereum)

## Configuration

Create a `.env` file or set environment variables:

```env
# AI Service API Keys
DEEPSEEK_API_KEY=your-deepseek-key
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key

# Wallet Configuration
ZEKTRA_WALLET_ADDRESS=0x...
ZEKTRA_PRIVATE_KEY=0x...
ZEKTRA_RPC_URL=https://...

# Payment Configuration
ZEKTRA_TOKEN_ADDRESS=0x...
PAYMENT_NETWORK=ethereum  # ethereum, solana, etc.
```

## Examples

See the `examples/` directory for more usage examples:

- `basic_query.py` - Simple AI query
- `wallet_integration.py` - Wallet connection examples
- `batch_queries.py` - Multiple queries with payment
- `custom_models.py` - Custom model configurations

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linter
ruff check .

# Format code
black .
```

## Roadmap

- [x] DeepSeek integration
- [x] Crypto payment layer
- [x] Wallet integration
- [ ] Multi-chain support (Solana, etc.)
- [ ] Subscription model
- [ ] Usage analytics dashboard
- [ ] Rate limiting and quotas

## License

MIT License

## Support

- GitHub Issues: https://github.com/zektra/zektra-ai-gateway/issues
- Documentation: https://docs.zektra.ai
- Discord: https://discord.gg/zektra

