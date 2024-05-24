import logging

from dotenv import load_dotenv
from fastapi import APIRouter
from starlette.responses import StreamingResponse

from apps.caminhoes_e_carretas.extract import BackhoeExtract
from apps.caminhoes_e_carretas.db_manager import save_to_database
from apps.caminhoes_e_carretas.automation import CaminhoesECarretasAutomation

logging.basicConfig(level=logging.INFO)

load_dotenv()

router = APIRouter()


@router.get("/crawler/backhoe/", response_class=StreamingResponse)
async def backhoe():
    collect_urls = CaminhoesECarretasAutomation()
    collected_urls, metrics, automation_failure_analysis = collect_urls.backhoe_url_all()

    extraction = BackhoeExtract(collected_urls)
    data, extract_failure_analysis, not_price = extraction.extract()

    logging.info(f"Métricas de desempenho ao obter URLs: {metrics}")
    logging.info(f"Falha ao obter URL, dos seguintes anúncios: {automation_failure_analysis}")
    logging.info(f"Falha na extração: {extract_failure_analysis}")
    logging.info(f"Quantidade de Anúncios sem Preço: {len(not_price)}  URLs Correspondentes: {not_price}")

    await save_to_database(data)

    return {"message": "Data saved to database successfully"}
