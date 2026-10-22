from enum import Enum


class PaymentType(Enum):
    CREDIT_CARD = "CREDIT CARD"
    CASH = "CASH"
    CHECK = "CHECK"
    OTHER = "OTHER"
