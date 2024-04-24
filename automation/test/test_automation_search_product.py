from unittest.mock import MagicMock, PropertyMock

from automation.product.search import AutomationSearchProduct


class AutomationSearchProductTest:
    @staticmethod
    def test_search_product_all():
        # Create a mock for the driver
        driver_mock = MagicMock()

        # Set up the mock to return a specific element for find_element
        element_mock = MagicMock()
        type(element_mock).aria_disabled = PropertyMock(return_value='false')
        driver_mock.find_element.return_value = element_mock

        # Create an instance of the class with the mock driver
        automation = AutomationSearchProduct()
        automation.driver = driver_mock

        # Run the method with a generic product and a site domain
        generic_product = "Shampoo"
        site_domain = "https://www.ikesaki.com.br/"
        urls = automation.search_product_all(generic_product, site_domain)

        # Verify that find_element was called on the driver
        driver_mock.find_element.assert_called()

        # Print the returned urls
        print(urls)


if __name__ == "__main__":
    AutomationSearchProductTest.test_search_product_all()

