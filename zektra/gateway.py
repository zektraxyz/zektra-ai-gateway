"""Main Zektra Gateway class"""

from typing import Optional, Dict, Any
from zektra.config import ZektraConfig
from zektra.models import AIResponse, PaymentResult, QueryRequest, ServiceInfo
from zektra.services import DeepSeekService, OpenAIService, AnthropicService
from zektra.payment import PaymentHandler


class ZektraGateway:
    """
    Main gateway for connecting AI services with Solana crypto payments
    """

    def __init__(
        self,
        solana_private_key: Optional[str] = None,
        config: Optional[ZektraConfig] = None
    ):
        """
        Initialize Zektra Gateway

        Args:
            solana_private_key: Solana private key (base58 encoded)
            config: ZektraConfig instance
        """
        self.config = config or ZektraConfig()
        
        # Override private key if provided
        if solana_private_key:
            self.config.solana_private_key = solana_private_key

        # Initialize payment handler (Solana only)
        if self.config.solana_private_key:
            self.payment_handler = PaymentHandler(config=self.config)
        else:
            self.payment_handler = None

        # Initialize AI services
        self.services: Dict[str, Any] = {}

        if self.config.deepseek_api_key:
            self.services["deepseek"] = DeepSeekService(
                api_key=self.config.deepseek_api_key,
                api_url=self.config.deepseek_api_url
            )

        if self.config.openai_api_key:
            self.services["openai"] = OpenAIService(
                api_key=self.config.openai_api_key,
                api_url=self.config.openai_api_url
            )

        if self.config.anthropic_api_key:
            self.services["anthropic"] = AnthropicService(
                api_key=self.config.anthropic_api_key,
                api_url=self.config.anthropic_api_url
            )

    def query(
        self,
        prompt: str,
        service: str = "deepseek",
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        payment_token: str = "ZEKTRA",
        payment_amount: Optional[float] = None,
        require_payment: bool = True,
        **kwargs
    ) -> AIResponse:
        """
        Query AI service with optional crypto payment

        Args:
            prompt: User prompt
            service: AI service name (deepseek, openai, anthropic)
            model: Specific model to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            payment_token: Token for payment (ZEKTRA, SOL, or other SPL token)
            payment_amount: Payment amount (defaults to config)
            require_payment: Whether payment is required
            **kwargs: Additional service-specific parameters

        Returns:
            AIResponse with generated text
        """
        # Get service
        if service not in self.services:
            raise ValueError(
                f"Service '{service}' not available. "
                f"Available services: {list(self.services.keys())}"
            )

        ai_service = self.services[service]

        # Process payment if required
        if require_payment and self.payment_handler:
            amount = payment_amount or self.config.default_payment_amount

            # Get recipient address (should be configured)
            recipient = self.config.solana_wallet_address
            if not recipient:
                raise ValueError("Recipient wallet address required for payment")

            payment_result = self.payment_handler.pay(
                amount=amount,
                token=payment_token,
                recipient=recipient,
                token_mint=self.config.token_mint if payment_token.upper() != "SOL" else None
            )

            if not payment_result.success:
                raise Exception(
                    f"Payment failed: {payment_result.error}"
                )

        # Query AI service
        response = ai_service.query(
            prompt=prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )

        return response

    def query_deepseek(
        self,
        prompt: str,
        model: Optional[str] = None,
        payment_token: str = "ZEKTRA",
        amount: Optional[float] = None,
        **kwargs
    ) -> AIResponse:
        """Convenience method for DeepSeek queries"""
        return self.query(
            prompt=prompt,
            service="deepseek",
            model=model,
            payment_token=payment_token,
            payment_amount=amount,
            **kwargs
        )

    def query_openai(
        self,
        prompt: str,
        model: Optional[str] = None,
        payment_token: str = "ZEKTRA",
        amount: Optional[float] = None,
        **kwargs
    ) -> AIResponse:
        """Convenience method for OpenAI queries"""
        return self.query(
            prompt=prompt,
            service="openai",
            model=model,
            payment_token=payment_token,
            payment_amount=amount,
            **kwargs
        )

    def get_available_services(self) -> Dict[str, ServiceInfo]:
        """Get list of available AI services"""
        return {
            name: service.get_service_info()
            for name, service in self.services.items()
        }

    def get_wallet_balance(self, token: Optional[str] = None) -> float:
        """Get Solana wallet balance (SOL or SPL token)"""
        if not self.payment_handler:
            raise ValueError("Payment handler not configured. Set SOLANA_PRIVATE_KEY in config.")

        import asyncio
        wallet_address = self.config.solana_wallet_address
        if not wallet_address:
            # Derive wallet address from private key if available
            if self.config.solana_private_key:
                from solders.keypair import Keypair
                import base58
                key_bytes = base58.b58decode(self.config.solana_private_key)
                keypair = Keypair.from_bytes(key_bytes)
                wallet_address = str(keypair.pubkey())
            else:
                raise ValueError("Wallet address or private key required")

        token_mint = None
        if token and token.upper() != "SOL":
            token_mint = self.config.token_mint

        return asyncio.run(
            self.payment_handler.solana_handler.get_balance(
                wallet_address=wallet_address,
                token_mint=token_mint
            )
        )

