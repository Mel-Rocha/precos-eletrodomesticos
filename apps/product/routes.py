from datetime import datetime

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from apps.wish_list.models import WishList
from apps.product.models import Product
from automation.product.search import AutomationSearchProduct
from apps.product.utils import extract_info_from_url

load_dotenv()

router = APIRouter()


@router.get("/extract/")
async def extract_product_price_store(url: str):
    """
    Objective:
        This endpoint is responsible for extracting product information from a URL.


    Parameters:
        Mandatory:
        url (str): The URL of the product page.

    Returns:
        If the operation is successful, the dictionary contains the keys 'product', 'price' and 'store'.

        If an error occurs while extract product information, the return is a JSONResponse with the key
        detail and the status_code.

        The 'status_code' is an HTTP status code that indicates the result of the operation. It could be one of the
        following:
        - 200: The search and removal of product information was successful.
        - 400: An error occurred while searching or removing product information.
    """

    return await extract_info_from_url(url)


@router.get("/automation/")
async def automation_product(specific_product: str, site_domain: str = 'https://www.ikesaki.com.br'):
    """
    Objective:
        This endpoint is responsible for automating the process of extracting product information from a website.


    Parameters:
        Mandatory:
        specific_product (str): The name of the product to be searched.

        Optional:
        site_domain (str): The domain of the site where the product will be searched.


    Returns:
        If the operation is successful, the dictionary contains the keys 'product', 'price' and 'store'.

        If an error occurs while searching or removing product information, the return is a JSONResponse with the key
        detail and the status_code.

        The 'status_code' is an HTTP status code that indicates the result of the operation. It could be one of the
        following:
        - 200: The search and removal of product information was successful.
        - 500: An error occurred while searching or removing product information.

    """

    try:
        automation = AutomationSearchProduct()
        redirected_url = automation.search_product(specific_product, site_domain)
        return await extract_info_from_url(redirected_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/create/")
async def create_product(generic_product: str, site_domain: str = 'https://www.ikesaki.com.br'):
    try:
        automation = AutomationSearchProduct()
        redirected_urls = automation.search_product_all(generic_product, site_domain)
        products = []
        for url in redirected_urls:
            products.append(await extract_info_from_url(url))
        return products
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)


@router.get("/create_or_update/")
async def create_or_update():
    """
    Objective:
        This endpoint is responsible for creating or updating products based on the information in the WishList table.


    Returns:
        JSONResponse: A JSONResponse object that contains a 'content' dictionary and a 'status_code'.

        The 'content' dictionary contains the key 'message', which can have one of the following values:
        - "Product created": A new product has been created successfully.
        - "Product updated": An existing product has been updated successfully.
        - An error message, an error will occur while creating or updating the product. The 'status_code'

        is an HTTP status code that indicates the result of the operation. It could be one of the following:
        - 201: A new product has been created successfully.
        - 200: An existing product has been successfully updated.
        - 500: An error occurred while creating or updating the product.
    """

    # Returns variables
    messages = {}
    status_code = None

    # Retrieve and processing WishList
    wish_lists = await WishList.all().values()
    for wish_list in wish_lists:
        try:
            # Extract product information
            automation = AutomationSearchProduct()
            redirected_url = automation.search_product(wish_list['wish_title'])
            product_info = await extract_info_from_url(redirected_url)
            product_name = product_info['product']
            price = product_info['price']
            store = product_info['store']

            # Create product
            current_date = datetime.now().strftime('%Y-%m-%d')
            if wish_list['product_id'] is None:
                product = await Product.create(
                    name=product_name,
                    store=store,
                    url=redirected_url,
                    price={current_date: price},
                )

                # Relates the newly created product to the corresponding wish_list
                wish_list['product_id'] = product.id
                await WishList.filter(id=wish_list['id']).update(product_id=product.id)

                messages[str(product.name)] = "Product created"
                status_code = 201
            else:
                # Try to get or create a Product with the specified id
                product, created = await Product.get_or_create(
                    id=wish_list['product_id'],
                    defaults={
                        "name": product_name,
                        "store": store,
                        "url": redirected_url,
                        "price": {current_date: price},
                    }
                )

                # If the product already exists, update it
                if not created:
                    product.name = product_name
                    product.store = store
                    product.url = redirected_url
                    if not isinstance(product.price, dict):
                        product.price = {}
                    product.price[current_date] = price
                    await product.save()
                    messages[str(product.name)] = "Product updated"
                    status_code = 200

        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=500)

    return JSONResponse(content=messages, status_code=status_code)
