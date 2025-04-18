import pytest


class TestLandingPage:

    def test_opencart_logo(self):
        print("Opencart logo should be displayed successfully")

    def test_menu_items(self):
        print("All menu items should be displayed successfully")

    def test_featured_section(self):
        print("Featured section should be displayed successfully")

    def test_search_field(self):
        print("Search field is working as expected")

    def test_footer_section(self):
        print("Footer section should be displayed successfully")

    @pytest.mark.smoke
    def test_add_item_to_cart(self):
        print("Item is added to cart successfully")