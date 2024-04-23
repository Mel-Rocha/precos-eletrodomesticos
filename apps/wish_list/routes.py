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
    """
    Objective:
        retrieve all WishList objects and present them in page format


    Parameters:
        Optional:
        page (int) : The page number to be displayed.
        size (int) : The number of items to be displayed per page.


    returns:
        dict: A dictionary that contains the following keys:
        - 'items': A list of dictionaries, where each dictionary represents a WishList object.
        - 'total': The total number of WishList objects.
        - 'page': The current page number.
        - 'size': The number of items displayed per page.
        - 'pages': The total number of pages.
    """

    wish_list_all = await WishList.all().values()
    return paginate(wish_list_all)

add_pagination(router)


@router.post("/upload")
async def upload_wish_list(file: UploadFile = File(...)):
    """
    Objective:
        This endpoint is responsible for uploading a spreadsheet containing a list of wishes.


    Parameters:
        Mandatory:
        file (UploadFile): The spreadsheet containing the list of wishes.


    Returns:
        JSONResponse: A JSON response that contains the following variables:
        - 'content': A dictionary that contains the key 'message'. Is a string that indicates the result of the upload.
        - 'status_code': An HTTP status code indicating the upload result.

        The 'status_code' is an HTTP status code that indicates the result of the operation. It could be one of the
        following:
        - 201: The upload was successful.
        - 400: An error occurred during the upload.
        - 500: An internal server error occurred.
    """
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

        # Check for duplicate wish_titles in the spreadsheet
        seen_wish_titles = set()
        unique_rows = []
        for _, row in df.iterrows():
            wish_title = row['wish_title']
            if wish_title not in seen_wish_titles:
                seen_wish_titles.add(wish_title)
                unique_rows.append(row.to_dict())

        # Bulk creation
        await WishList.bulk_create([WishList(**row) for row in unique_rows])

        return JSONResponse(content={"message": "Wish list uploaded successfully"},
                            status_code=201)

    except InvalidColumnsException as e:
        return JSONResponse(content={"message": f'{str(e)}, The spreadsheet must contain these columns WISH_TITLE, '
                                                f'EXPECTED_PURCHASE_DATE, DESIRE_TO_ACQUIRE, '
                                                f'NEED_TO_ACQUIRE'},
                            status_code=400)
    except IntegrityError as e:
        return JSONResponse(content={"message": f'{str(e)}, the wish_title field cannot have duplicate values'},
                            status_code=400)

    except Exception as e:
        return JSONResponse(content={"message": str(e)},
                            status_code=500)
