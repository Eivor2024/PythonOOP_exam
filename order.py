from abc import ABC, abstractmethod
from datetime import date
from customer import Customer
from order_item import OrderItem
from payment_type import PaymentType


class Order(ABC):
    # Both RegularOrder and VIPOrder use this same list of order IDs.
    _used_ids = []

    def __init__(self, order_id: int, name: str, delivery_address: str,
                 items: list[OrderItem], customer: Customer,
                 payment_type: PaymentType, order_date=None):
        if order_id in Order._used_ids:
            raise ValueError("An order with this ID already exists.")
        if not isinstance(customer, Customer):
            raise TypeError("Order customer must be a Customer object.")
        if not isinstance(payment_type, PaymentType):
            raise TypeError("Payment type must be a PaymentType value.")
        if order_date is not None and not isinstance(order_date, date):
            raise TypeError("Order date must be a date object or None.")

        checked_items = []
        item_ids = []
        for item in items:
            if not isinstance(item, OrderItem):
                raise TypeError("Order items must be OrderItem objects.")
            if item.id in item_ids:
                raise ValueError("An order cannot contain the same item ID twice.")
            checked_items.append(item)
            item_ids.append(item.id)

        self._id = order_id
        self.name = name
        self.delivery_address = delivery_address
        self._items = checked_items
        self.customer = customer
        self.payment_type = payment_type
        if order_date is None:
            self.order_date = date.today()
        else:
            self.order_date = order_date

        self.total_price = 0.0
        # Python calls the implementation belonging to the concrete order type.
        self.calculate_total_price()

        # Update favorites and reserve the ID only after the order is valid.
        for item in self._items:
            self.customer.add_favorite_item(item)
        Order._used_ids.append(order_id)

    @property
    def id(self) -> int:
        return self._id

    @property
    def items(self) -> list[OrderItem]:
        return self._items.copy()

    def _calculate_items_total(self) -> float:
        total = 0.0
        for item in self._items:
            total += item.price
        return total

    @abstractmethod
    def calculate_total_price(self) -> float:
        pass
