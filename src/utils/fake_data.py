from uuid import uuid4

from faker import Faker


class FakeData:
    _categories = (
        "Electronics",
        "Clothing",
        "Home & Kitchen",
        "Personal Care",
        "Sports & Fitness",
        "Books",
        "Toys",
        "Food & Beverages",
        "Pet Supplies",
        "Automotive Accessories",
    )

    def __init__(self, faker: Faker | None = None) -> None:
        self._faker = faker or Faker()

    def generate_name(self) -> str:
        return self._faker.name()

    def generate_unique_category(self) -> str:
        category = self._faker.random_element(self._categories)
        return f"{category}_{uuid4().hex}"

    def generate_email(self) -> str:
        return self._faker.email()

    def generate_password(self) -> str:
        return self._faker.password(
            length=8, special_chars=False, digits=True, upper_case=True, lower_case=True
        )

    def generate_url(self) -> str:
        return self._faker.url()

    def generate_product_title(self) -> str:
        product = self._faker.catch_phrase()
        return f"{product}-{uuid4().hex}"

    def generate_product_price(self) -> int:
        return int(self._faker.random_number(3, False))

    def generate_product_description(self) -> str:
        return self._faker.sentence()

    def generate_product_images(self) -> list[str]:
        return [self._faker.url()]


fake = FakeData()
