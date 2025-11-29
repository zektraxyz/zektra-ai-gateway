"""Payment handler for crypto transactions"""

from typing import Optional
from web3 import Web3
from eth_account import Account
from zektra.models import PaymentResult
from zektra.payment.wallet import WalletManager
from zektra.payment.solana_payment import SolanaPaymentHandler
from zektra.config import ZektraConfig


class PaymentHandler:
    """Handle crypto payments for AI services"""

    # Standard ERC20 Transfer ABI
    ERC20_TRANSFER_ABI = [
        {
            "constant": False,
            "inputs": [
                {"name": "_to", "type": "address"},
                {"name": "_value", "type": "uint256"}
            ],
            "name": "transfer",
            "outputs": [{"name": "", "type": "bool"}],
            "type": "function"
        }
    ]

    def __init__(
        self,
        wallet_manager: Optional[WalletManager] = None,
        config: Optional[ZektraConfig] = None
    ):
        self.config = config or ZektraConfig()
        self.wallet_manager = wallet_manager

        # Initialize based on payment network
        if self.config.payment_network.lower() == "solana":
            self.solana_handler = SolanaPaymentHandler(
                rpc_url=self.config.solana_rpc_url,
                private_key=self.config.solana_private_key
            )
            self.web3 = None
        else:
            # Ethereum
            if not self.wallet_manager:
                if self.config.wallet_address:
                    self.wallet_manager = WalletManager(config=self.config)
                else:
                    raise ValueError("Wallet manager or wallet address required")
            self.web3 = self.wallet_manager.web3
            self.solana_handler = None

    def pay(
        self,
        amount: float,
        token: str = "ZEKTRA",
        recipient: Optional[str] = None,
        token_address: Optional[str] = None
    ) -> PaymentResult:
        """
        Process payment with crypto token

        Args:
            amount: Amount to pay
            token: Token symbol (ZEKTRA, USDC, ETH, SOL)
            recipient: Recipient address (default: payment contract)
            token_address: Token contract/mint address

        Returns:
            PaymentResult with transaction details
        """
        try:
            # Solana payments (async)
            if self.config.payment_network.lower() == "solana":
                import asyncio
                if token.upper() == "SOL":
                    return asyncio.run(self.solana_handler.pay_sol(amount, recipient or ""))
                else:
                    # SPL token (ZEKTRA from Pump.fun)
                    token_mint = token_address or self.config.zektra_token_mint
                    if not token_mint:
                        raise ValueError(f"Token mint address required for {token}")
                    return asyncio.run(
                        self.solana_handler.pay_spl_token(
                            amount=amount,
                            token_mint=token_mint,
                            recipient=recipient or ""
                        )
                    )
            
            # Ethereum payments
            else:
                if token.upper() == "ETH":
                    return self._pay_eth(amount, recipient)
                else:
                    # ERC20 token payment
                    if not token_address:
                        token_address = self.config.zektra_token_address
                        if not token_address:
                            raise ValueError(f"Token address required for {token}")

                    return self._pay_token(amount, token_address, recipient)

        except Exception as e:
            return PaymentResult(
                success=False,
                amount=amount,
                token=token,
                error=str(e)
            )

    def _pay_eth(self, amount: float, recipient: Optional[str] = None) -> PaymentResult:
        """Pay with ETH"""
        if not recipient:
            # Default to a payment contract address (should be configured)
            raise ValueError("Recipient address required for ETH payment")

        recipient = Web3.to_checksum_address(recipient)
        amount_wei = self.web3.to_wei(amount, "ether")

        # Get nonce
        nonce = self.web3.eth.get_transaction_count(
            self.wallet_manager.wallet_address
        )

        # Build transaction
        transaction = {
            "to": recipient,
            "value": amount_wei,
            "gas": 21000,
            "gasPrice": self.web3.eth.gas_price,
            "nonce": nonce,
            "chainId": self.web3.eth.chain_id,
        }

        # Sign and send
        signed_txn = self.wallet_manager.sign_transaction(transaction)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn)

        return PaymentResult(
            success=True,
            transaction_hash=tx_hash.hex(),
            amount=amount,
            token="ETH"
        )

    def _pay_token(
        self,
        amount: float,
        token_address: str,
        recipient: Optional[str] = None
    ) -> PaymentResult:
        """Pay with ERC20 token"""
        if not recipient:
            # Default payment recipient (should be configured)
            raise ValueError("Recipient address required for token payment")

        token_address = Web3.to_checksum_address(token_address)
        recipient = Web3.to_checksum_address(recipient)

        # Get token contract
        contract = self.web3.eth.contract(
            address=token_address,
            abi=self.ERC20_TRANSFER_ABI
        )

        # Get token decimals
        decimals_abi = [{
            "constant": True,
            "inputs": [],
            "name": "decimals",
            "outputs": [{"name": "", "type": "uint8"}],
            "type": "function"
        }]
        decimals_contract = self.web3.eth.contract(
            address=token_address,
            abi=decimals_abi
        )
        decimals = decimals_contract.functions.decimals().call()

        # Convert amount to token units
        amount_units = int(amount * (10 ** decimals))

        # Build transaction
        function_call = contract.functions.transfer(recipient, amount_units)
        transaction = function_call.build_transaction({
            "from": self.wallet_manager.wallet_address,
            "gas": 100000,
            "gasPrice": self.web3.eth.gas_price,
            "nonce": self.web3.eth.get_transaction_count(
                self.wallet_manager.wallet_address
            ),
            "chainId": self.web3.eth.chain_id,
        })

        # Sign and send
        signed_txn = self.wallet_manager.sign_transaction(transaction)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn)

        return PaymentResult(
            success=True,
            transaction_hash=tx_hash.hex(),
            amount=amount,
            token="TOKEN"
        )

    def verify_payment(self, transaction_hash: str) -> bool:
        """Verify a payment transaction"""
        try:
            if self.config.payment_network.lower() == "solana":
                # Verify Solana transaction (async)
                if self.solana_handler:
                    import asyncio
                    from solders.signature import Signature
                    sig = Signature.from_string(transaction_hash)
                    status = asyncio.run(
                        self.solana_handler.client.get_signature_status(sig)
                    )
                    return status.value is not None and status.value[0] is not None
                return False
            else:
                # Verify Ethereum transaction
                receipt = self.web3.eth.get_transaction_receipt(transaction_hash)
                return receipt.status == 1
        except Exception:
            return False

