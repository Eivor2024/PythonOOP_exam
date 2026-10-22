from customer import Customer
from customer_type import CustomerType
from gift_box import GiftBox
from order_item import OrderItem
from payment_type import PaymentType
from regular_order import RegularOrder
from vip_order import VIPOrder


def print_order(order) -> None:
    print(f"Order {order.id}: {order.name}")
    print(f"Customer: {order.customer.first_name} {order.customer.last_name}")
    print(f"Delivery address: {order.delivery_address}")
    print(f"Payment: {order.payment_type.value}")
    print(f"Date: {order.order_date}")
    for item in order.items:
        print(f"  {item.name}: {item.price:.2f}")
    print(f"Total price: {order.total_price:.2f}")
    print()


def print_favorites(customer) -> None:
    print(f"{customer.first_name}'s favorite items:")
    for item in customer.favorite_items:
        print(f"  {item.name} (ID: {item.id})")
    print()


def main() -> None:
    # 1. Create items. These two Mouse objects have different unique IDs.
    laptop = OrderItem(101, "Laptop", 1000)
    mouse = OrderItem(102, "Mouse", 100)
    keyboard = OrderItem(103, "Keyboard", 200)
    another_mouse = OrderItem(104, "Mouse", 120)

    # 2. Create a regular customer and a VIP customer with a 20% discount.
    alice = Customer(1, "Alice", "Cohen", "alice@example.com",
                     "10 Main St", CustomerType.REGULAR)
    bob = Customer(2, "Bob", "Levi", "bob@example.com",
                   "20 Main St", CustomerType.VIP, discount=20)

    # 3. Creating each order calculates its total and updates favorites.
    regular_order = RegularOrder(
        1001, "Alice's first order", alice.delivery_address,
        [laptop, mouse], alice, PaymentType.CASH
    )
    vip_order = VIPOrder(
        1002, "Bob's VIP order - (VIP discount 20%)", bob.delivery_address,
        [laptop, keyboard], bob, PaymentType.CREDIT_CARD
    )
    print("CREATED ORDERS")
    print_order(regular_order)  # 1100.00: no discount.
    print_order(vip_order)      # 960.00: 1200 minus 20%.

    # 4. Another order contains a Mouse with a different ID.
    # Alice's favorites still contain only one item named Mouse.
    second_order = RegularOrder(
        1003, "Alice's second order", alice.delivery_address,
        [another_mouse], alice, PaymentType.CHECK
    )
    print("SECOND ORDER AND AUTOMATIC FAVORITES")
    print_order(second_order)
    print_favorites(alice)
    print_favorites(bob)

    # 5. Alice manually adds Keyboard and removes Laptop from her favorites.
    print("MANUAL FAVORITE UPDATES")
    alice.add_favorite_item(keyboard)
    alice.remove_favorite_item(laptop)
    print_favorites(alice)

    # 6. Give Alice a gift, then open the gift if she has one. If opened - gift is cleared.
    print("CUSTOMER GIFT")
    alice.take_gift(GiftBox())
    if alice.customer_gift is not None:
        alice.customer_gift.open_gift()
        print("Gift used")
        alice.customer_gift = None
    print(f"Alice's gift after opening: {alice.customer_gift}")

    # 7. A regular customer cannot create a VIP order.
    print("\nINVALID VIP ORDER")
    try:
        VIPOrder(1004, "Invalid VIP order", alice.delivery_address,
                 [keyboard], alice, PaymentType.OTHER)
    except ValueError as error:
        print(f"Rejected: {error}")

    # 8. Order IDs must be unique across both order types.
    print("\nDUPLICATE ORDER ID")
    try:
        VIPOrder(1001, "Duplicate order", bob.delivery_address,
                 [keyboard], bob, PaymentType.CREDIT_CARD)
    except ValueError as error:
        print(f"Rejected: {error}")


if __name__ == "__main__":
    main()
