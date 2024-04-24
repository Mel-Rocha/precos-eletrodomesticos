from automation.search import AutomationSearchProduct


def test_search_product_on_site():
    automation = AutomationSearchProduct()

    product = "Joico"
    site_domain = "https://www.ikesaki.com.br/"

    redirected_url = automation.search_product(product, site_domain)

    print(redirected_url)


if __name__ == "__main__":
    test_search_product_on_site()
