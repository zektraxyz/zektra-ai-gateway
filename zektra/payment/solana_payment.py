"""Solana payment handler for SPL tokens"""

from typing import Optional
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.system_program import transfer, TransferParams
from solders.transaction import Transaction
from solders.rpc.requests import send_transaction
from solders.rpc.config import RpcSendTransactionConfig
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
import base58

from zektra.models import PaymentResult


class SolanaPaymentHandler:
    """Handle Solana SPL token payments"""

    def __init__(
        self,
        rpc_url: str = "https://api.mainnet-beta.solana.com",
        private_key: Optional[str] = None
    ):
        """
        Initialize Solana payment handler

        Args:
            rpc_url: Solana RPC URL
            private_key: Base58 encoded private key
        """
        self.rpc_url = rpc_url
        self.client = AsyncClient(rpc_url)
        
        if private_key:
            # Decode base58 private key
            key_bytes = base58.b58decode(private_key)
            self.keypair = Keypair.from_bytes(key_bytes)
        else:
            self.keypair = None

    async def pay_sol(
        self,
        amount: float,
        recipient: str,
        sender_keypair: Optional[Keypair] = None
    ) -> PaymentResult:
        """
        Pay with SOL

        Args:
            amount: Amount in SOL
            recipient: Recipient wallet address (base58)
            sender_keypair: Optional sender keypair (uses self.keypair if not provided)

        Returns:
            PaymentResult
        """
        if not sender_keypair and not self.keypair:
            return PaymentResult(
                success=False,
                amount=amount,
                token="SOL",
                error="Private key or keypair required"
            )

        keypair = sender_keypair or self.keypair

        try:
            recipient_pubkey = Pubkey.from_string(recipient)
            
            # Convert SOL to lamports (1 SOL = 1e9 lamports)
            lamports = int(amount * 1e9)

            # Build transfer instruction
            transfer_ix = transfer(
                TransferParams(
                    from_pubkey=keypair.pubkey(),
                    to_pubkey=recipient_pubkey,
                    lamports=lamports
                )
            )

            # Get recent blockhash
            recent_blockhash = (await self.client.get_latest_blockhash()).value.blockhash

            # Build transaction
            transaction = Transaction()
            transaction.add(transfer_ix)
            transaction.recent_blockhash = recent_blockhash
            transaction.sign(keypair)

            # Send transaction
            result = await self.client.send_transaction(
                transaction,
                keypair,
                opts=RpcSendTransactionConfig(skip_preflight=False)
            )

            tx_hash = str(result.value)

            return PaymentResult(
                success=True,
                transaction_hash=tx_hash,
                amount=amount,
                token="SOL"
            )

        except Exception as e:
            return PaymentResult(
                success=False,
                amount=amount,
                token="SOL",
                error=str(e)
            )

    async def pay_spl_token(
        self,
        amount: float,
        token_mint: str,
        recipient: str,
        sender_keypair: Optional[Keypair] = None,
        decimals: int = 9
    ) -> PaymentResult:
        """
        Pay with SPL token (like ZEKTRA from Pump.fun)

        Args:
            amount: Amount in tokens
            token_mint: Token mint address (base58)
            recipient: Recipient wallet address (base58)
            sender_keypair: Optional sender keypair
            decimals: Token decimals (default 9 for most SPL tokens)

        Returns:
            PaymentResult
        """
        if not sender_keypair and not self.keypair:
            return PaymentResult(
                success=False,
                amount=amount,
                token="SPL",
                error="Private key or keypair required"
            )

        keypair = sender_keypair or self.keypair

        try:
            from spl.token.instructions import transfer_checked, TransferCheckedParams
            from spl.token.client import Token
            from spl.token.constants import TOKEN_PROGRAM_ID

            token_mint_pubkey = Pubkey.from_string(token_mint)
            recipient_pubkey = Pubkey.from_string(recipient)

            # Get sender's token account
            token = Token(self.client, token_mint_pubkey, TOKEN_PROGRAM_ID, keypair)
            sender_token_account = await token.get_accounts(keypair.pubkey())
            
            if not sender_token_account.value:
                return PaymentResult(
                    success=False,
                    amount=amount,
                    token="SPL",
                    error="No token account found for sender"
                )

            sender_account_pubkey = sender_token_account.value[0].pubkey

            # Get or create recipient token account
            recipient_token_account = await token.get_accounts(recipient_pubkey)
            if not recipient_token_account.value:
                # Create associated token account if needed
                await token.create_associated_token_account(recipient_pubkey)
                recipient_token_account = await token.get_accounts(recipient_pubkey)

            recipient_account_pubkey = recipient_token_account.value[0].pubkey

            # Convert amount to token units
            amount_units = int(amount * (10 ** decimals))

            # Build transfer instruction
            transfer_ix = transfer_checked(
                TransferCheckedParams(
                    program_id=TOKEN_PROGRAM_ID,
                    source=sender_account_pubkey,
                    mint=token_mint_pubkey,
                    dest=recipient_account_pubkey,
                    owner=keypair.pubkey(),
                    amount=amount_units,
                    decimals=decimals
                )
            )

            # Get recent blockhash
            recent_blockhash = (await self.client.get_latest_blockhash()).value.blockhash

            # Build transaction
            transaction = Transaction()
            transaction.add(transfer_ix)
            transaction.recent_blockhash = recent_blockhash
            transaction.sign(keypair)

            # Send transaction
            result = await self.client.send_transaction(
                transaction,
                keypair,
                opts=RpcSendTransactionConfig(skip_preflight=False)
            )

            tx_hash = str(result.value)

            return PaymentResult(
                success=True,
                transaction_hash=tx_hash,
                amount=amount,
                token="SPL"
            )

        except Exception as e:
            return PaymentResult(
                success=False,
                amount=amount,
                token="SPL",
                error=str(e)
            )

    async def get_balance(
        self,
        wallet_address: str,
        token_mint: Optional[str] = None
    ) -> float:
        """
        Get wallet balance (SOL or SPL token)

        Args:
            wallet_address: Wallet address (base58)
            token_mint: Optional token mint address for SPL token

        Returns:
            Balance in SOL or tokens
        """
        try:
            wallet_pubkey = Pubkey.from_string(wallet_address)

            if token_mint:
                # Get SPL token balance
                from spl.token.client import Token
                from spl.token.constants import TOKEN_PROGRAM_ID

                token_mint_pubkey = Pubkey.from_string(token_mint)
                token = Token(self.client, token_mint_pubkey, TOKEN_PROGRAM_ID, None)

                accounts = await token.get_accounts(wallet_pubkey)
                if accounts.value:
                    account_info = await token.get_account_info(accounts.value[0].pubkey)
                    decimals = account_info.value.decimals
                    return account_info.value.amount / (10 ** decimals)
                return 0.0
            else:
                # Get SOL balance
                balance = await self.client.get_balance(wallet_pubkey)
                return balance.value / 1e9  # Convert lamports to SOL

        except Exception as e:
            return 0.0

    async def close(self):
        """Close RPC connection"""
        await self.client.close()

