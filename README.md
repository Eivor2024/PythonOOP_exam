# Customer Order Management System

A Python OOP exam project that manages customers, regular orders, VIP orders,
favorite items, and customer gifts. Each class is stored in a separate file,
and `main.py` demonstrates how the objects work together.

## Requirements and running the project

- Python 3.9 or later.
- No external packages are required. The project uses Python's standard library.

Keep all ten Python files in the same folder. Open a terminal in that folder
and run:

```bash
python main.py
```

In PyCharm:

1. Open the folder containing the Python files as a project.
2. Select a Python interpreter for the project.
3. Open `main.py`.
4. Right-click inside the editor and select **Run 'main'**.

## Project files

| File | Purpose |
| --- | --- |
| [main.py](main.py) | Creates example customers, items, orders, and a gift. |
| [customer.py](customer.py) | Stores customer details and manages favorite items and gifts. |
| [customer_type.py](customer_type.py) | Defines the `REGULAR` and `VIP` customer types using `Enum`. |
| [order_item.py](order_item.py) | Stores an item's unique ID, name, and price. |
| [order.py](order.py) | Abstract base class containing the shared order attributes and behavior. |
| [regular_order.py](regular_order.py) | Implements the total-price calculation without a discount. |
| [vip_order.py](vip_order.py) | Checks VIP eligibility and calculates the discounted total. |
| [payment_type.py](payment_type.py) | Defines `CREDIT_CARD`, `CASH`, `CHECK`, and `OTHER` payment types. |
| [gift.py](gift.py) | Abstract class declaring the `open_gift()` method. |
| [gift_box.py](gift_box.py) | Implements a gift that prints the required congratulations message. |

## Orders and price calculation

Every order stores its ID, name, delivery address, item list, customer,
total price, payment type, and date. If a date is not supplied, it uses
the current date.

`RegularOrder` and `VIPOrder` inherit their constructor from `Order`.
The constructor calls `calculate_total_price()`, and Python selects the
implementation belonging to the order's class.

- A **regular order** sums the prices of its items without applying a discount,
  even if its customer is VIP.
- A **VIP order** first checks that its customer has `CustomerType.VIP`.
  A regular customer attempting to create a VIP order causes a `ValueError`.
  Eligible customers receive the discount stored in their `discount` field.

Discounts are percentages: `discount=20` means 20%. A discount of `None`
is treated as 0%. When creating a customer, a supplied discount must be
a number between 0 and 100.

For Bob's VIP order in `main.py`:

```text
Laptop:                  1000.00
Keyboard:                 200.00
Items total:             1200.00
VIP discount (20%):        240.00
Final order total:        960.00
```

The formula is:

```python
total_price = items_total * (1 - discount / 100)
```

Calling `calculate_total_price()` again recalculates the amount and updates
the order's stored `total_price`. For example, this can be used after changing
an item's price.

## Unique IDs

Each of `Customer`, `OrderItem`, and `Order` maintains a class-level
`_used_ids` list. Creating another object of the same kind with an existing
ID raises a `ValueError`.

- Regular and VIP orders share the same order-ID list.
- Customers, items, and orders have separate ID lists. A customer and an
  order can therefore have the same numeric ID.
- Existing customer and item objects can be reused in multiple orders.
- The same item ID cannot appear twice within one order.
- Two distinct items may have the same name if their IDs are different.

IDs are exposed through read-only `id` properties. IDs are reserved after
successful construction, so a failed construction does not consume an ID.
The lists exist in memory for the current program run and reset when a
new Python process starts. The project does not save data to a database or file.

## Favorite items

Each customer starts with an empty favorite-items list. After an order is
successfully created, all its items are automatically added to that customer's
favorites.

Favorites are compared by their **exact names**, using ordinary loops.
For example, items named `Mouse` with IDs `102` and `104` count as the same
favorite. The first stored item is retained. Both items can still appear
in an order, where both prices contribute to the total.

Customers can also update favorites manually. In the demonstration:

```python
alice.add_favorite_item(keyboard)
alice.remove_favorite_item(laptop)
```

Adding an existing favorite or removing an absent favorite leaves the list
unchanged. Removal also compares names, so an item with a different ID but
the same name can be used to remove a favorite.

The `favorite_items` and order `items` properties return copies of their
lists. The item objects inside those copies are still the same objects.

## Customer gifts

A customer initially has `customer_gift = None`, meaning no gift is assigned.
`take_gift(gift)` accepts any object with a callable `open_gift()` method.
This is duck typing: the object does not have to inherit from `Gift`.

`GiftBox` is the provided example. It inherits from the abstract `Gift` class,
and its `open_gift()` method prints exactly:

```text
Congratulations! you got a new gift! Enjoy!
```

The demonstration gives Alice a gift, opens it, and clears her gift afterward:

```python
alice.take_gift(GiftBox())

if alice.customer_gift is not None:
    alice.customer_gift.open_gift()
    alice.customer_gift = None

print(f"Alice's gift after opening: {alice.customer_gift}")
```

Its output is:

```text
Congratulations! you got a new gift! Enjoy!
Alice's gift after opening: None
```

The assignment to `None` is performed explicitly in `main.py`.
Calling the gift's `open_gift()` method alone only prints the message.

## What the demonstration covers

Running `main.py` demonstrates:

1. Creating items and regular/VIP customers.
2. Creating a regular order totaling **1100.00**.
3. Creating a VIP order totaling **960.00**, after a 20% discount on 1200.00.
4. Creating another regular order totaling **120.00**.
5. Adding order items to favorites automatically, without duplicate names.
6. Adding and removing favorites manually.
7. Receiving, opening, and clearing a gift.
8. Rejecting a VIP order placed by a regular customer.
9. Rejecting an order ID already used by another order type.

The final `Rejected:` messages are intentional examples handled with
`try`/`except`; they show that the checks work. Dates in the output depend
on the day the program runs.

## OOP concepts used

- **Classes and objects:** customers, items, orders, and gifts.
- **Constructors:** initialize attributes and calculate order totals.
- **Encapsulation:** internal fields, read-only ID properties, and list copies.
- **Class attributes:** shared lists used to enforce unique IDs.
- **Inheritance:** `RegularOrder` and `VIPOrder` inherit from `Order`;
  `GiftBox` inherits from `Gift`.
- **Abstract classes:** `ABC` and `@abstractmethod` define required methods.
- **Polymorphism:** each order type implements its own price calculation.
- **Composition:** orders hold customer and item objects; customers hold a gift.
- **Enums:** named customer and payment choices.
- **Duck typing:** accepting gift objects through their `open_gift()` method.
- **Exceptions:** reporting invalid inputs and duplicate IDs.

Calculations and favorite-item checks use ordinary loops to keep the
implementation suitable for an introductory Python OOP course.
