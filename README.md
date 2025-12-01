# Zektra AI Gateway

**Version:** 0.1.0-beta  
**Status:** Beta - Production Ready

A Python gateway that connects AI services (DeepSeek, OpenAI, etc.) with Solana crypto payments using $ZEKTRA tokens from [Pump.fun](https://pump.fun/coin/7p3jMiwW5sapCq7eXysuhGAXdDhr6sERytjUzH5fpump).

## Features

- 🔌 **AI Service Integration**: Connect to DeepSeek, OpenAI, Anthropic, and more
- 💰 **Solana Payments**: Pay for AI queries using $ZEKTRA tokens or SOL
- 🔐 **Solana Wallet Support**: Native Solana wallet integration
- 📊 **Usage Tracking**: Monitor API usage and costs
- 🚀 **Production Ready**: Built for reliability and scale

## Installation

```bash
pip install zektra-ai-gateway
```

Or install from source:

```bash
git clone https://github.com/zektraxyz/zektra-ai-gateway.git
cd zektra-ai-gateway
pip install -e .
```

## Quick Start

### Basic Usage

```python
from zektra import ZektraGateway

# Initialize gateway (uses SOLANA_PRIVATE_KEY from .env or config)
gateway = ZektraGateway()

# Query DeepSeek with ZEKTRA token payment
response = gateway.query_deepseek(
    prompt="Explain zero-knowledge proofs",
    payment_token="ZEKTRA",
    amount=0.1  # ZEKTRA tokens
)

print(response.text)
```

### With Custom Configuration

```python
from zektra import ZektraGateway, ZektraConfig

# Create custom config
config = ZektraConfig(
    solana_private_key="your-base58-private-key",
    solana_wallet_address="recipient-wallet-address",
    token_mint="7p3jMiwW5sapCq7eXysuhGAXdDhr6sERytjUzH5fpump"  # ZEKTRA token
)

gateway = ZektraGateway(config=config)

# Query AI service
response = gateway.query(
    service="deepseek",
    prompt="What is homomorphic encryption?",
    payment_token="ZEKTRA"
)
```

### CLI Usage

```bash
# Set your API keys and Solana wallet
export DEEPSEEK_API_KEY="your-key"
export SOLANA_PRIVATE_KEY="your-base58-private-key"
export SOLANA_WALLET_ADDRESS="recipient-address"
export TOKEN_MINT="7p3jMiwW5sapCq7eXysuhGAXdDhr6sERytjUzH5fpump"

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

- **$ZEKTRA Token** (Primary) - Solana SPL token from [Pump.fun](https://pump.fun/coin/7p3jMiwW5sapCq7eXysuhGAXdDhr6sERytjUzH5fpump)
- **SOL** (Solana native)
- **Other SPL Tokens** - Any Solana SPL token by providing mint address

## Configuration

Create a `.env` file or set environment variables:

```env
# AI Service API Keys
DEEPSEEK_API_KEY=your-deepseek-key
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key

# Solana Configuration
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
SOLANA_PRIVATE_KEY=your-base58-private-key
SOLANA_WALLET_ADDRESS=recipient-wallet-address  # Where payments are sent

# Token Configuration
TOKEN_MINT=7p3jMiwW5sapCq7eXysuhGAXdDhr6sERytjUzH5fpump  # ZEKTRA token from Pump.fun
DEFAULT_PAYMENT_AMOUNT=0.1
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
- [x] Solana payment layer
- [x] Solana wallet integration
- [x] SPL token support
- [ ] Subscription model
- [ ] Usage analytics dashboard
- [ ] Rate limiting and quotas

## License

MIT License

## Support

- GitHub Issues: https://github.com/zektraxyz/zektra-ai-gateway/issues
