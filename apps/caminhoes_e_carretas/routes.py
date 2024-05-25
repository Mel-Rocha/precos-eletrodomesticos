import logging

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from starlette.responses import StreamingResponse

from apps.caminhoes_e_carretas.extract import BackhoeExtract
from apps.caminhoes_e_carretas.db_manager import DatabaseManager
from apps.caminhoes_e_carretas.automation import CaminhoesECarretasAutomation

logging.basicConfig(level=logging.INFO)

router = APIRouter()


@router.get("/crawler/backhoe/", response_class=StreamingResponse)
async def backhoe():
    try:
        collect_urls = CaminhoesECarretasAutomation()
        collected_urls, metrics, automation_failure_analysis = collect_urls.backhoe_url_all()

        extraction = BackhoeExtract(collected_urls)
        data, extract_failure_analysis, not_price = extraction.extract()

        logging.info(f"Métricas de desempenho ao obter URLs: {metrics}")
        logging.info(f"Falha ao obter URL, dos seguintes anúncios: {automation_failure_analysis}")
        logging.info(f"Falha na extração: {extract_failure_analysis}")
        logging.info(f"Quantidade de Anúncios sem Preço: {len(not_price)}  URLs Correspondentes: {not_price}")

        new_records_count = await DatabaseManager.save_data_and_get_new_record_count(data)
        records_with_null_model_code = await DatabaseManager.count_records_with_null_model_code()

        if new_records_count > 0:
            return JSONResponse(status_code=201, content={
                "message": "Data saved to database successfully",
                "new_records_count": new_records_count,
                "records_with_null_model_code": records_with_null_model_code
            })
        else:
            return JSONResponse(status_code=200, content={
                "message": "Data saved to database successfully",
                "new_records_count": new_records_count,
                "records_with_null_model_code": records_with_null_model_code
            })
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")
