from customer_type import CustomerType
from order_item import OrderItem


class Customer:
    _used_ids = []

    def __init__(self, customer_id: int, first_name: str, last_name: str,
                 email: str, delivery_address: str,
                 customer_type: CustomerType, discount=None):
        if customer_id in Customer._used_ids:
            raise ValueError("A customer with this ID already exists.")
        if not isinstance(customer_type, CustomerType):
            raise TypeError("Customer type must be a CustomerType value.")
        if discount is not None:
            if not isinstance(discount, (int, float)) or isinstance(discount, bool):
                raise TypeError("Discount must be a number or None.")
            if not 0 <= discount <= 100:
                raise ValueError("Discount must be between 0 and 100 percent.")

        self._id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.delivery_address = delivery_address
        self.customer_type = customer_type
        self.discount = discount
        self._favorite_items = []
        self.customer_gift = None
        Customer._used_ids.append(customer_id)

    @property
    def id(self) -> int:
        return self._id

    @property
    def favorite_items(self) -> list[OrderItem]:
        # Return a copy so updates go through the methods below.
        return self._favorite_items.copy()

    def add_favorite_item(self, item: OrderItem) -> None:
        if not isinstance(item, OrderItem):
            raise TypeError("A favorite item must be an OrderItem object.")

        for favorite in self._favorite_items:
            if favorite.name == item.name:
                return

        self._favorite_items.append(item)

    def remove_favorite_item(self, item: OrderItem) -> None:
        if not isinstance(item, OrderItem):
            raise TypeError("A favorite item must be an OrderItem object.")

        for favorite in self._favorite_items:
            if favorite.name == item.name:
                self._favorite_items.remove(favorite)
                return

    def take_gift(self, gift) -> None:
        # Duck typing: accept any object with a callable open_gift method.
        if not callable(getattr(gift, "open_gift", None)):
            raise TypeError("A gift must have an open_gift() method.")

        self.customer_gift = gift
