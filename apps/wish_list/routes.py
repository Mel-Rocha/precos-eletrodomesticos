from io import BytesIO

import pandas as pd
from fastapi.responses import JSONResponse
from fastapi_pagination import Page, add_pagination, paginate
from fastapi import APIRouter, UploadFile, File

from apps.wish_list.models import WishList
from apps.wish_list.schema import WishListSchema

router = APIRouter()


@router.get("/")
async def get_wish_list_all() -> Page[WishListSchema]:
    wish_list_all = await WishList.all().values()
    return paginate(wish_list_all)

add_pagination(router)


@router.post("/upload")
async def upload_wish_list(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        file_data = BytesIO(contents)

        df = pd.read_excel(file_data)

        df['product_name'] = df['PRODUCT_NAME'].astype(str).str.strip()
        df = df.drop('PRODUCT_NAME', axis=1)

        df['site_domain'] = df['SITE_DOMAIN'].astype(str).str.strip()
        df = df.drop('SITE_DOMAIN', axis=1)

        df['expected_purchase_date'] = df['EXPECTED_PURCHASE_DATE'].astype(str).str.strip()
        df = df.drop('EXPECTED_PURCHASE_DATE', axis=1)

        df['desire_to_acquire'] = df['DESIRE_TO_ACQUIRE'].astype(str).str.strip()
        df = df.drop('DESIRE_TO_ACQUIRE', axis=1)

        df['need_to_acquire'] = df['NEED_TO_ACQUIRE'].astype(str).str.strip()
        df = df.drop('NEED_TO_ACQUIRE', axis=1)

        data_to_insert = df.to_dict(orient='records')

        await WishList.bulk_create([WishList(**row) for row in data_to_insert])

        return JSONResponse(content={"message": "Wish list uploaded successfully"},
                            status_code=201)

    except Exception as e:
        return JSONResponse(content={"message": str(e)},
                            status_code=500)
