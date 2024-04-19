from fastapi import APIRouter, HTTPException

from scraping.product.extract import ExtractProductPriceStore

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
