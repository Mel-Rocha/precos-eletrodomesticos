from io import BytesIO

import pandas as pd
from fastapi.responses import JSONResponse
from fastapi_pagination import Page, add_pagination, paginate
from fastapi import APIRouter, UploadFile, File
from tortoise.exceptions import IntegrityError

from apps.wish_list.exceptions import InvalidColumnsException
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
        # File reading
        contents = await file.read()
        file_data = BytesIO(contents)

        # File Processing
        df = pd.read_excel(file_data)

        # Validation columns
        expected_columns = {'WISH_TITLE', 'EXPECTED_PURCHASE_DATE', 'DESIRE_TO_ACQUIRE',
                            'NEED_TO_ACQUIRE'}
        if set(df.columns) != expected_columns:
            raise InvalidColumnsException(status_code=400, detail="Upload Failed")

        # Column treatment
        df['wish_title'] = df['WISH_TITLE'].astype(str).str.strip()
        df = df.drop('WISH_TITLE', axis=1)

        df['expected_purchase_date'] = df['EXPECTED_PURCHASE_DATE'].astype(str).str.strip()
        df = df.drop('EXPECTED_PURCHASE_DATE', axis=1)

        df['desire_to_acquire'] = df['DESIRE_TO_ACQUIRE'].astype(str).str.strip()
        df = df.drop('DESIRE_TO_ACQUIRE', axis=1)

        df['need_to_acquire'] = df['NEED_TO_ACQUIRE'].astype(str).str.strip()
        df = df.drop('NEED_TO_ACQUIRE', axis=1)

        # Format conversion required to create bulk objects
        data_to_insert = df.to_dict(orient='records')

        # Bulk creation
        await WishList.bulk_create([WishList(**row) for row in data_to_insert])

        return JSONResponse(content={"message": "Wish list uploaded successfully"},
                            status_code=201)

    except InvalidColumnsException as e:
        return JSONResponse(content={"message": f'{str(e)}, The spreadsheet must contain these columns PRODUCT_NAME, '
                                                f'SITE_DOMAIN, EXPECTED_PURCHASE_DATE, DESIRE_TO_ACQUIRE, '
                                                f'NEED_TO_ACQUIRE'},
                            status_code=400)
    except IntegrityError as e:
        return JSONResponse(content={"message": f'{str(e)}, the wish_title field cannot have duplicate values'},
                            status_code=400)

    except Exception as e:
        return JSONResponse(content={"message": str(e)},
                            status_code=500)
