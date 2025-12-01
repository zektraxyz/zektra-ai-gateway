"""Command-line interface for Zektra AI Gateway"""

import sys
import argparse
from typing import Optional
from zektra import ZektraGateway
from zektra.config import ZektraConfig


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Zektra AI Gateway - Connect AI services with crypto payments"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Query command
    query_parser = subparsers.add_parser("query", help="Query AI service")
    query_parser.add_argument("service", choices=["deepseek", "openai", "anthropic"])
    query_parser.add_argument("prompt", help="Prompt to send")
    query_parser.add_argument("--model", help="Model to use")
    query_parser.add_argument("--payment", default="ZEKTRA", help="Payment token")
    query_parser.add_argument("--amount", type=float, help="Payment amount")
    query_parser.add_argument("--no-payment", action="store_true", help="Skip payment")

    # Services command
    services_parser = subparsers.add_parser("services", help="List available services")
    services_parser.add_argument("list", nargs="?", const=True, help="List services")

    # Wallet command
    wallet_parser = subparsers.add_parser("wallet", help="Wallet operations")
    wallet_subparsers = wallet_parser.add_subparsers(dest="wallet_command")
    
    balance_parser = wallet_subparsers.add_parser("balance", help="Check balance")
    balance_parser.add_argument("--token", help="Token address or symbol")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        # Initialize gateway
        config = ZektraConfig()
        gateway = ZektraGateway(config=config)

        if args.command == "query":
            response = gateway.query(
                prompt=args.prompt,
                service=args.service,
                model=args.model,
                payment_token=args.payment,
                payment_amount=args.amount,
                require_payment=not args.no_payment
            )
            print("\n" + "="*60)
            print("AI Response:")
            print("="*60)
            print(response.text)
            print("\n" + "="*60)
            print(f"Model: {response.model}")
            if response.usage:
                print(f"Usage: {response.usage}")

        elif args.command == "services":
            services = gateway.get_available_services()
            print("\nAvailable AI Services:")
            print("="*60)
            for name, info in services.items():
                status = "✓ Available" if info.available else "✗ Not configured"
                print(f"\n{name.upper()}: {status}")
                print(f"  Models: {', '.join(info.models)}")
                print(f"  Default: {info.default_model}")
                if info.description:
                    print(f"  Description: {info.description}")

        elif args.command == "wallet":
            if args.wallet_command == "balance":
                balance = gateway.get_wallet_balance(token=args.token)
                token_name = args.token or "SOL"
                print(f"\nBalance: {balance} {token_name}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

