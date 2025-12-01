"""Configuration management for Zektra AI Gateway"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class ZektraConfig(BaseSettings):
    """Configuration for Zektra AI Gateway (Solana only)"""

    # AI Service API Keys
    deepseek_api_key: Optional[str] = Field(default=None, env="DEEPSEEK_API_KEY")
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")

    # Solana Configuration
    solana_rpc_url: str = Field(
        default="https://api.mainnet-beta.solana.com",
        env="SOLANA_RPC_URL"
    )
    solana_private_key: Optional[str] = Field(
        default=None,
        env="SOLANA_PRIVATE_KEY"
    )
    solana_wallet_address: Optional[str] = Field(
        default=None,
        env="SOLANA_WALLET_ADDRESS"
    )
    
    # Token Configuration
    token_mint: Optional[str] = Field(
        default="7p3jMiwW5sapCq7eXysuhGAXdDhr6sERytjUzH5fpump",
        env="TOKEN_MINT"  # Solana SPL token mint address (ZEKTRA from Pump.fun)
    )
    
    # Default payment amount (in tokens)
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

