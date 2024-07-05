class DummyEmailService:
    @staticmethod
    def send_registration_email(email: str):
        print(f"Registration successful for email: {email}")