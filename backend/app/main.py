from fastapi import FastAPI

from app.clients.clinica_nas_nuvens import ClinicaNasNuvensClient

app = FastAPI(title="Clinica Sync", version="0.1.0")


@app.get("/health")
def health() -> dict:
    """Endpoint simples pra confirmar que o container e o hot-reload estão funcionando."""
    return {"status": "ok"}


@app.get("/agenda/test")
async def agenda_test(data_inicial: str, data_final: str) -> dict:
    """
    Endpoint temporário só pra validar client + models contra a API real.
    Ex: /agenda/test?data_inicial=2026-06-30&data_final=2026-06-30
    """
    client = ClinicaNasNuvensClient()
    try:
        itens = await client.listar_agenda_completa(data_inicial, data_final)
    finally:
        await client.aclose()

    return {
        "total_agendamentos": len(itens),
        "convenios_distintos": sorted({i.id_tipo_convenio for i in itens}),
        "medicos_distintos": sorted({i.id_pessoa_executor for i in itens}),
        "primeiro": itens[0].model_dump(mode="json") if itens else None,
    }
