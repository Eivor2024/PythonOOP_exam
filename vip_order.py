from customer_type import CustomerType
from order import Order


class VIPOrder(Order):
    def calculate_total_price(self) -> float:
        if self.customer.customer_type != CustomerType.VIP:
            raise ValueError("A VIP order requires a VIP customer.")

        total = self._calculate_items_total()
        discount = self.customer.discount
        if discount is None:
            discount = 0

        self.total_price = total * (1 - discount / 100)
        return self.total_price
