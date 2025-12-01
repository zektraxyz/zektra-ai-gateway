"""
Zektra AI Gateway - Connect AI services with crypto payments
Version: 0.1.0-beta
"""

__version__ = "0.1.0"
__author__ = "Zektra Team"

from zektra.gateway import ZektraGateway
from zektra.config import ZektraConfig
from zektra.models import AIResponse, PaymentResult

__all__ = [
    "ZektraGateway",
    "ZektraConfig",
    "AIResponse",
    "PaymentResult",
]

