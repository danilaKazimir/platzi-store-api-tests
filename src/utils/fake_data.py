from faker import Faker


class Fake(Faker):
    def generate_name(self) -> str:
        return self.name()

    def generate_email(self) -> str:
        return self.email()

    def generate_password(self) -> str:
        return self.password(
            length=8, special_chars=False, digits=True, upper_case=True, lower_case=True
        )

    def generate_avatar_url(self) -> str:
        return self.url()


fake = Fake()
