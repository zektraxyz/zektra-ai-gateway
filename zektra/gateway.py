"""Main Zektra Gateway class"""

from typing import Optional, Dict, Any
from zektra.config import ZektraConfig
from zektra.models import AIResponse, PaymentResult, QueryRequest, ServiceInfo
from zektra.services import DeepSeekService, OpenAIService, AnthropicService
from zektra.payment import PaymentHandler, WalletManager


class ZektraGateway:
    """
    Main gateway for connecting AI services with crypto payments
    """

    def __init__(
        self,
        wallet_address: Optional[str] = None,
        private_key: Optional[str] = None,
        wallet: Optional[WalletManager] = None,
        config: Optional[ZektraConfig] = None
    ):
        """
        Initialize Zektra Gateway

        Args:
            wallet_address: Ethereum wallet address
            private_key: Private key for signing transactions
            wallet: Pre-configured WalletManager instance
            config: ZektraConfig instance
        """
        self.config = config or ZektraConfig()

        # Initialize wallet manager
        if wallet:
            self.wallet_manager = wallet
        elif wallet_address or self.config.wallet_address:
            self.wallet_manager = WalletManager(
                wallet_address=wallet_address,
                private_key=private_key,
                config=self.config
            )
        else:
            self.wallet_manager = None

        # Initialize payment handler
        if self.wallet_manager:
            self.payment_handler = PaymentHandler(
                wallet_manager=self.wallet_manager,
                config=self.config
            )
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
            payment_token: Token for payment (ZEKTRA, USDC, ETH)
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

            payment_result = self.payment_handler.pay(
                amount=amount,
                token=payment_token
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
        """Get wallet balance"""
        if not self.wallet_manager:
            raise ValueError("Wallet not configured")

        token_address = None
        if token and token.upper() != "ETH":
            token_address = self.config.zektra_token_address

        return self.wallet_manager.get_balance(token_address=token_address)

