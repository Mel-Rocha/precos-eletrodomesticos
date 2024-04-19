from fastapi import APIRouter, HTTPException

from scraping.ikesaki.extract import ExtractProductPrice

router = APIRouter()


@router.get("/extract/")
async def extract_product_price(url: str):
    try:
        extractor = ExtractProductPrice(url)
        product = extractor.extract_product()
        price = extractor.extract_price()
        return {"product": product, "price": price}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
