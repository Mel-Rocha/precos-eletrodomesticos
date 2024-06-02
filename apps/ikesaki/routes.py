import logging

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from starlette.responses import StreamingResponse

from apps.ikesaki.extract import IkesakiExtract
from apps.ikesaki.db_manager import DatabaseManager
from apps.ikesaki.excel_generator import ExcelGenerator
from apps.ikesaki.automation import IkesakiAutomation

logging.basicConfig(level=logging.INFO)

router = APIRouter()


@router.get("/crawler/ikesaki/")
async def ikesaki():
    try:
        collect_urls = IkesakiAutomation()
        collected_urls, metrics, automation_failure_analysis = collect_urls.ikesaki_url_all()

        if collected_urls:
            extraction = IkesakiExtract(collected_urls)
            data, extract_failure_analysis, not_price = extraction.extract()

            logging.info(f"Métricas de desempenho ao obter URLs: {metrics}")
            logging.info(f"Falha ao obter URL, dos seguintes anúncios: {automation_failure_analysis}")
            logging.info(f"Falha na extração: {extract_failure_analysis}")
            logging.info(f"Quantidade de Anúncios sem Preço: {len(not_price)}  URLs Correspondentes: {not_price}")

            if data:
                new_records_count = await DatabaseManager.save_data_and_get_new_record_count(data)

                if new_records_count > 0:
                    return JSONResponse(status_code=201, content={
                        "message": "Dados cadastrados com sucesso",
                        "Quantidade de novos registros": new_records_count,
                    })
                else:
                    return JSONResponse(status_code=200, content={
                        "message": "Nenhum novo dado foi cadastrado",
                        "Quantidade de novos registros": new_records_count,
                    })
    except Exception as e:
        logging.error(f"Erro: {str(e)}")
        raise HTTPException(status_code=500, detail="Ocorreu um erro, falha no processo.")


@router.get("/consolidated/ikesaki/excel/", response_class=StreamingResponse)
async def ikesaki_excel():
    try:
        data = await DatabaseManager.get_all_data()
        if not data:
            return JSONResponse(status_code=400, content={
                "message": "O banco não possui nenhum registro, portanto não é possível gerar o excel. Execute a "
                           "automação préviamente."
            })

        excel_generator = ExcelGenerator()
        response = excel_generator.generate(data)
        return response
    except Exception as e:
        logging.error(f"Erro: {str(e)}")
        raise HTTPException(status_code=500, detail="Ocorreu um erro, falha no processo.")
