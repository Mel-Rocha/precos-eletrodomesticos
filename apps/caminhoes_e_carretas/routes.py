from io import BytesIO
from typing import List

import pandas as pd
from dotenv import load_dotenv
from fastapi import APIRouter, Query
from fastapi_pagination import Page, add_pagination, paginate
from starlette.responses import StreamingResponse

from apps.caminhoes_e_carretas.models import CaminhoesECarretas
from apps.caminhoes_e_carretas.schema import CaminhoesECarretasSchema
from scraping.caminhoes_e_carretas.backhoe import BackhoeExtract

load_dotenv()

router = APIRouter()


@router.get("/")
async def get_caminhoes_e_carretas_all() -> Page[CaminhoesECarretasSchema]:
    caminhoes_e_carretas_all = await CaminhoesECarretas.all().values()
    return paginate(caminhoes_e_carretas_all)


add_pagination(router)


@router.get("/extract/backhoe_all/")
async def extract_backhoe_all(urls: List[str] = Query(...)):
    e = BackhoeExtract(urls)
    result = e.extract()
    return {"result": result}


@router.get("/backhoe/excel/")
async def extract_urls(urls: List[str] = Query(...)):
    e = BackhoeExtract(urls)
    data = e.extract()

    df = pd.DataFrame(data)

    df.rename(columns={
        'fabricator': 'Fabricante',
        'model': 'Modelo',
        'year': 'Ano',
        'price': 'Preço',
        'worked_hours': 'Horas',
        'url': 'URL',
        'crawling_date': 'Data da Busca'
    }, inplace=True)

    df['Cód. Somos'] = ''

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

    output.seek(0)

    return StreamingResponse(output, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                             headers={
                                 'Content-Disposition': 'attachment; filename="dataframe.xlsx"'
                             })