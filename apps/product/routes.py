from datetime import datetime

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from scraping.product.extract import ExtractProductPriceStore
from apps.wish_list.models import WishList
from apps.product.models import Product
from automation.search import AutomationSearchProduct
from apps.product.utils import extract_info_from_url

load_dotenv()

router = APIRouter()


@router.get("/extract/")
async def extract_product_price_store(url: str):
    return await extract_info_from_url(url)


@router.get("/automation/")
async def automation_product(product: str, site_domain: str = 'https://www.ikesaki.com.br'):
    try:
        automation = AutomationSearchProduct()
        redirected_url = automation.search_product_on_site(product, site_domain)
        return await extract_info_from_url(redirected_url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/create_or_update/")
async def create_or_update():
    wish_lists = await WishList.all().values()
    messages = {}
    status_code = None
    for wish_list in wish_lists:
        try:

            automation = AutomationSearchProduct()
            redirected_url = automation.search_product_on_site(wish_list['wish_title'])
            extractor = ExtractProductPriceStore(redirected_url)
            product_name = extractor.extract_product()
            price = extractor.extract_price()
            store = extractor.extract_store()

            current_date = datetime.now().strftime('%Y-%m-%d')
            if wish_list['product_id'] is None:
                # Create a new Product without specifying an id
                product = await Product.create(
                    name=product_name,
                    store=store,
                    url=redirected_url,
                    price={current_date: price},
                )

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
