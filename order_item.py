class OrderItem:
    # Shared by all OrderItem objects during this program run.
    _used_ids = []

    def __init__(self, item_id: int, name: str, price: float):
        if item_id in OrderItem._used_ids:
            raise ValueError("An item with this ID already exists.")
        if price < 0:
            raise ValueError("Item price cannot be negative.")

        self._id = item_id
        self.name = name
        self.price = price
        OrderItem._used_ids.append(item_id)

    @property
    def id(self) -> int:
        return self._id
