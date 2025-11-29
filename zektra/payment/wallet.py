"""Wallet management for crypto payments"""

from typing import Optional
from web3 import Web3
from eth_account import Account
from zektra.config import ZektraConfig


class WalletManager:
    """Manage Web3 wallet operations"""

    def __init__(
        self,
        wallet_address: Optional[str] = None,
        private_key: Optional[str] = None,
        rpc_url: Optional[str] = None,
        config: Optional[ZektraConfig] = None
    ):
        self.config = config or ZektraConfig()
        
        self.wallet_address = wallet_address or self.config.wallet_address
        self.private_key = private_key or self.config.private_key
        self.rpc_url = rpc_url or self.config.rpc_url

        if not self.wallet_address:
            raise ValueError("Wallet address is required")

        # Initialize Web3 connection
        self.web3 = Web3(Web3.HTTPProvider(self.rpc_url))

        if not self.web3.is_connected():
            raise ConnectionError(f"Failed to connect to RPC: {self.rpc_url}")

        # Validate wallet address
        if not self.web3.is_address(self.wallet_address):
            raise ValueError(f"Invalid wallet address: {self.wallet_address}")

        # If private key provided, validate it matches address
        if self.private_key:
            account = Account.from_key(self.private_key)
            if account.address.lower() != self.wallet_address.lower():
                raise ValueError("Private key does not match wallet address")

    def get_balance(self, token_address: Optional[str] = None) -> float:
        """Get wallet balance (ETH or ERC20 token)"""
        if token_address:
            return self._get_token_balance(token_address)
        else:
            balance_wei = self.web3.eth.get_balance(self.wallet_address)
            return self.web3.from_wei(balance_wei, "ether")

    def _get_token_balance(self, token_address: str) -> float:
        """Get ERC20 token balance"""
        # ERC20 balanceOf ABI
        abi = [
            {
                "constant": True,
                "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "balance", "type": "uint256"}],
                "type": "function"
            },
            {
                "constant": True,
                "inputs": [],
                "name": "decimals",
                "outputs": [{"name": "", "type": "uint8"}],
                "type": "function"
            }
        ]

        contract = self.web3.eth.contract(
            address=Web3.to_checksum_address(token_address),
            abi=abi
        )

        balance = contract.functions.balanceOf(
            Web3.to_checksum_address(self.wallet_address)
        ).call()

        decimals = contract.functions.decimals().call()
        return balance / (10 ** decimals)

    def sign_transaction(self, transaction: dict) -> dict:
        """Sign a transaction"""
        if not self.private_key:
            raise ValueError("Private key required for signing transactions")

        account = Account.from_key(self.private_key)
        signed_txn = account.sign_transaction(transaction)
        return signed_txn.rawTransaction

