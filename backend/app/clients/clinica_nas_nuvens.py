import asyncio

import httpx
from aiolimiter import AsyncLimiter

from app.config import settings
from app.models import AgendaItem, AgendaListaResponse, ExecutorAgenda, ExecutorAgendaListaResponse, PacienteListaResponse, TipoConvenio, TipoConvenioListaResponse


class ClinicaNasNuvensClient:
    """
    Client pra API pública do Clínica nas Nuvens.

    Limite documentado: 120 req/token/minuto -> respeita 115/min como margem
    de segurança (evita bater exatamente no teto em condição de corrida).
    """

    def __init__(self) -> None:
        self._limiter = AsyncLimiter(115, 60)
        self._client = httpx.AsyncClient(
            base_url=settings.cnn_base_url,
            auth=(settings.cnn_client_id, settings.cnn_client_secret),
            headers={"clinicaNasNuvens-cid": settings.cnn_clinic_token},
            timeout=30.0,
        )

    async def _get(self, path: str, params: dict) -> dict:
        async with self._limiter:
            resp = await self._client.get(path, params=params)
            resp.raise_for_status()
            return resp.json()

    async def listar_agenda_pagina(
        self, data_inicial: str, data_final: str, pagina: int = 0
    ) -> AgendaListaResponse:
        data = await self._get(
            "/agenda/lista",
            params={
                "dataInicial": data_inicial,
                "dataFinal": data_final,
                "pagina": pagina,
            },
        )
        return AgendaListaResponse.model_validate(data)

    async def listar_agenda_completa(
        self, data_inicial: str, data_final: str
    ) -> list[AgendaItem]:
        """Percorre todas as páginas e devolve a lista completa de agendamentos."""
        primeira = await self.listar_agenda_pagina(data_inicial, data_final, pagina=0)
        itens = list(primeira.lista)

        for pagina in range(1, primeira.total_paginas):
            resp = await self.listar_agenda_pagina(data_inicial, data_final, pagina=pagina)
            itens.extend(resp.lista)

        return itens

    async def listar_tipo_convenio(self) -> TipoConvenioListaResponse:
        data = await self._get("/tipo-convenio/lista", params={"pagina": 0})
        return TipoConvenioListaResponse.model_validate(data)

    async def listar_executor_agenda(self) -> ExecutorAgendaListaResponse:
        data = await self._get("/executor-agenda/lista", params={"pagina": 0})
        return ExecutorAgendaListaResponse.model_validate(data)

    async def iter_clientes(self):
        pagina = 0
        primeira_data = await self._get("/paciente/lista", params={"pagina": pagina})
        primeira = PacienteListaResponse.model_validate(primeira_data)
        yield primeira.lista

        for pagina in range(1, primeira.total_paginas):
            data = await self._get("/paciente/lista", params={"pagina": pagina})
            resp = PacienteListaResponse.model_validate(data)
            yield resp.lista

    async def aclose(self) -> None:
        await self._client.aclose()
