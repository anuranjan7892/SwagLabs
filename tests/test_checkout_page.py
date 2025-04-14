import pytest


class TestCheckoutPage:

    def test_add_personal_details(self):
        print("User is able to add his details successfully")

    def test_enter_payment_method(self):
        print("User is able to enter payment method successfully")

    @pytest.mark.smoke
    def test_confirm_order(self):
        print("User is able to confirm the order successfully")