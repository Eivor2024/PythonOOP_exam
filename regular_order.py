from order import Order


class RegularOrder(Order):
    def calculate_total_price(self) -> float:
        self.total_price = self._calculate_items_total()
        return self.total_price
