from abc import ABC, abstractmethod


class Animal(ABC):
    def __init__(self, legs: int):
        # UML uses # for a protected field; Python uses an underscore convention.
        self._legs = legs

    def walk(self) -> None:
        print(f"This animal walks on {self._legs} legs.")

    @abstractmethod
    def eat(self) -> None:
        pass


# Python represents this interface with an abstract class.
class Pet(ABC):
    @abstractmethod
    def getName(self) -> str:
        pass

    @abstractmethod
    def setName(self, name: str) -> None:
        pass

    @abstractmethod
    def play(self) -> None:
        pass


class Spider(Animal):
    def __init__(self):
        super().__init__(8)

    def eat(self) -> None:
        print("The spider eats insects.")


class Cat(Animal, Pet):
    # The default value supports both Cat() and Cat("Mittens").
    def __init__(self, name: str = ""):
        super().__init__(4)
        self._name = name

    def getName(self) -> str:
        return self._name

    def setName(self, name: str) -> None:
        self._name = name

    def play(self) -> None:
        print(f"{self._name} plays with a ball.")

    def eat(self) -> None:
        print(f"{self._name} eats cat food.")


class Fish(Animal, Pet):
    def __init__(self):
        super().__init__(0)
        self._name = ""

    def getName(self) -> str:
        return self._name

    def setName(self, name: str) -> None:
        self._name = name

    def play(self) -> None:
        print(f"{self._name} swims around playfully.")

    def walk(self) -> None:
        print("Fish cannot walk; they swim instead.")

    def eat(self) -> None:
        print(f"{self._name} eats fish food.")


def main() -> None:
    spider = Spider()
    cat = Cat("Mittens")
    fish = Fish()
    fish.setName("Nemo")

    print("SPIDER")
    spider.walk()
    spider.eat()

    print("\nCAT")
    print("Name:", cat.getName())
    cat.walk()
    cat.eat()
    cat.play()

    print("\nFISH")
    print("Name:", fish.getName())
    fish.walk()
    fish.eat()
    fish.play()

    print("\nCAT CREATED WITHOUT A NAME")
    another_cat = Cat()
    another_cat.setName("Luna")
    print("Name after setName():", another_cat.getName())

    # Polymorphism: each object runs its own eat() implementation.
    print("\nALL ANIMALS EATING")
    animals = [spider, cat, fish]
    for animal in animals:
        animal.eat()


if __name__ == "__main__":
    main()
