"""Configuration management for Zektra AI Gateway"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class ZektraConfig(BaseSettings):
    """Configuration for Zektra AI Gateway"""

    # AI Service API Keys
    deepseek_api_key: Optional[str] = Field(default=None, env="DEEPSEEK_API_KEY")
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")

    # Wallet Configuration
    wallet_address: Optional[str] = Field(default=None, env="ZEKTRA_WALLET_ADDRESS")
    private_key: Optional[str] = Field(default=None, env="ZEKTRA_PRIVATE_KEY")
    rpc_url: str = Field(
        default="https://eth.llamarpc.com",
        env="ZEKTRA_RPC_URL"
    )

    # Payment Configuration
    zektra_token_address: Optional[str] = Field(
        default=None,
        env="ZEKTRA_TOKEN_ADDRESS"
    )
    payment_network: str = Field(default="solana", env="PAYMENT_NETWORK")  # solana or ethereum
    
    # Solana Configuration
    solana_rpc_url: str = Field(
        default="https://api.mainnet-beta.solana.com",
        env="SOLANA_RPC_URL"
    )
    solana_private_key: Optional[str] = Field(
        default=None,
        env="SOLANA_PRIVATE_KEY"
    )
    zektra_token_mint: Optional[str] = Field(
        default=None,
        env="ZEKTRA_TOKEN_MINT"  # Solana SPL token mint address
    )
    
    # Default payment amount (in ZEKTRA tokens)
    default_payment_amount: float = Field(default=0.1, env="DEFAULT_PAYMENT_AMOUNT")

    # API Endpoints
    deepseek_api_url: str = Field(
        default="https://api.deepseek.com/v1/chat/completions",
        env="DEEPSEEK_API_URL"
    )
    openai_api_url: str = Field(
        default="https://api.openai.com/v1/chat/completions",
        env="OPENAI_API_URL"
    )
    anthropic_api_url: str = Field(
        default="https://api.anthropic.com/v1/messages",
        env="ANTHROPIC_API_URL"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


def get_config() -> ZektraConfig:
    """Get Zektra configuration from environment"""
    return ZektraConfig()

