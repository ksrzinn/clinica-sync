from datetime import date, time

from pydantic import BaseModel, ConfigDict, Field


class Procedimento(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    id_tipo_procedimento: int = Field(alias="idTipoProcedimento")
    id_promocao: int | None = Field(default=None, alias="idPromocao")
    id_especialidade: int | None = Field(default=None, alias="idEspecialidade")
    quantidade: int
    nome: str


class AgendaItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    id_pessoa_executor: int = Field(alias="idPessoaExecutor")
    id_paciente: int = Field(alias="idPaciente")
    id_origem_paciente: int | None = Field(default=None, alias="idOrigemPaciente")
    id_tipo_convenio: int = Field(alias="idTipoConvenio")
    id_tipo_consulta: int = Field(alias="idTipoConsulta")
    id_local_agenda: int = Field(alias="idLocalAgenda")
    status: str
    data: date
    hora_inicio: time = Field(alias="horaInicio")
    hora_fim: time = Field(alias="horaFim")
    observacoes: str | None = None
    telefone_celular_paciente: str | None = Field(default=None, alias="telefoneCelularPaciente")
    email_paciente: str | None = Field(default=None, alias="emailPaciente")
    encaminhamento: str | None = None
    url_sala_espera: str | None = Field(default=None, alias="urlSalaEspera")
    id_rotulo: int | None = Field(default=None, alias="idRotulo")
    procedimentos: list[Procedimento] = Field(default_factory=list)


class AgendaListaResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    pagina: int
    total_paginas: int = Field(alias="totalPaginas")
    lista: list[AgendaItem]

class Contato(BaseModel): 
    model_config = ConfigDict(populate_by_name=True)

    telefone_celular: str | None = Field(default=None, alias="telefoneCelular")
    telefone_comercial: str | None = Field(default=None, alias="telefoneComercial")
    telefone_residencial: str | None = Field(default=None, alias="telefoneResidencial")
    email: str | None = Field(default=None, alias="email")

class Paciente(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    nome: str
    cpf_cnpj: str | None = Field(default=None, alias="cpfcnpj")
    data_nascimento: date | None = Field(default=None, alias="dataNascimento")
    sexo: str | None = Field(default=None, alias="sexo")
    contato: Contato | None = None

class PacienteListaResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    pagina: int
    total_paginas: int = Field(alias="totalPaginas")
    lista: list[Paciente]



if __name__ == "__main__":
    dados_pacientes = {
        "pagina": 0,
        "totalPaginas": 1,
        "lista": [
            {"id": 1, "nome": "Ana Silva"},
            {"id": 2, "nome": "Bruno Costa"},
            {"id": 3, "nome": "Carla Souza"},
        ]
    }
    for paciente in dados_pacientes["lista"]:
        print(f"Paciente: {paciente['nome']} (ID: {paciente['id']})")
        lookup = {p['id']: p for p in dados_pacientes["lista"]}


    print(lookup[3])