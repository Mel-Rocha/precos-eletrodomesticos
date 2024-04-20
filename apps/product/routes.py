import os

from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv

from scraping.product.extract import ExtractProductPriceStore
from automation.search import AutomationSearchProduct

load_dotenv()

router = APIRouter()


@router.get("/extract/")
async def extract_product_price_store(url: str):
    try:
        extractor = ExtractProductPriceStore(url)
        product = extractor.extract_product()
        price = extractor.extract_price()
        store = extractor.extract_store()
        return {"product": product, "price": price, "store": store}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/automation/product/")
async def automation_product(site_domain: str, product: str):
    try:
        automation = AutomationSearchProduct()
        redirected_url = automation.search_product_on_site(site_domain, product)

        # Call the extract functions directly with the redirected url
        extractor = ExtractProductPriceStore(redirected_url)
        product = extractor.extract_product()
        price = extractor.extract_price()
        store = extractor.extract_store()

        # Return the extracted product information
        return {"product": product, "price": price, "store": store}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
