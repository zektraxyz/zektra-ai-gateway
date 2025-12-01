"""Payment handler for Solana transactions"""

from typing import Optional
import asyncio
from zektra.models import PaymentResult
from zektra.payment.solana_payment import SolanaPaymentHandler
from zektra.config import ZektraConfig


class PaymentHandler:
    """Handle Solana payments for AI services"""

    def __init__(
        self,
        config: Optional[ZektraConfig] = None
    ):
        self.config = config or ZektraConfig()
        
        # Initialize Solana payment handler
        self.solana_handler = SolanaPaymentHandler(
            rpc_url=self.config.solana_rpc_url,
            private_key=self.config.solana_private_key
        )

    def pay(
        self,
        amount: float,
        token: str = "ZEKTRA",
        recipient: Optional[str] = None,
        token_mint: Optional[str] = None
    ) -> PaymentResult:
        """
        Process payment with Solana token

        Args:
            amount: Amount to pay
            token: Token symbol (ZEKTRA, SOL, or other SPL token)
            recipient: Recipient wallet address (base58)
            token_mint: Token mint address (defaults to config token_mint)

        Returns:
            PaymentResult with transaction details
        """
        try:
            if token.upper() == "SOL":
                # Pay with SOL
                if not recipient:
                    raise ValueError("Recipient address required for SOL payment")
                return asyncio.run(
                    self.solana_handler.pay_sol(amount, recipient)
                )
            else:
                # Pay with SPL token (ZEKTRA or other)
                if not recipient:
                    raise ValueError("Recipient address required for token payment")
                
                mint_address = token_mint or self.config.token_mint
                if not mint_address:
                    raise ValueError(f"Token mint address required for {token}")
                
                return asyncio.run(
                    self.solana_handler.pay_spl_token(
                        amount=amount,
                        token_mint=mint_address,
                        recipient=recipient
                    )
                )

        except Exception as e:
            return PaymentResult(
                success=False,
                amount=amount,
                token=token,
                error=str(e)
            )

    def verify_payment(self, transaction_hash: str) -> bool:
        """Verify a Solana payment transaction"""
        try:
            import asyncio
            from solders.signature import Signature
            
            sig = Signature.from_string(transaction_hash)
            status = asyncio.run(
                self.solana_handler.client.get_signature_status(sig)
            )
            return status.value is not None and status.value[0] is not None
        except Exception:
            return False
