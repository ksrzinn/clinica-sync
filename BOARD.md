# clinica-sync — Board

> Formato de cada card: **User Story** (o quê/porquê) + **Critérios de Aceite**
> (como você sabe que terminou) + **Contexto técnico** (o que você precisa
> saber/decidir) + **Dependências**. Quando ficar perdido: abre esse arquivo,
> vai na coluna "Doing", esse é o card ativo.

---

## ✅ Done

- **Setup Docker** — `docker-compose.yml` + `Dockerfile` do backend, hot-reload funcionando via bind mount
- **`/agenda/test`** — endpoint validado contra API real
- **Schemas reais confirmados** — `/agenda/lista`, `/tipo-convenio/lista`, `/executor-agenda/lista`, `/paciente/lista`
- **Pydantic básico** — `BaseModel`, `Field(alias=...)`, campo opcional (`| None`) vs obrigatório
- **Pydantic aninhado** — `Contato` dentro de `Paciente`
- **`model_validate()`** a partir de dict
- **`dict`** — criação, `.get()`, iteração
- **``CARD-01``** — Lookup de paciente por id (``dict comprehension``)
---

## 🔨 Doing

### CARD-01: Lookup de paciente por id (dict comprehension)

**Story:** Como desenvolvedor, quero transformar uma lista de `Paciente` num dict indexado por `id`, para que eu consiga buscar o nome de um paciente em tempo O(1) em vez de percorrer a lista inteira.

**Critérios de aceite:**
- [x] Existe uma classe `PacienteListaResponse` com campos `pagina: int`, `total_paginas: int = Field(alias="totalPaginas")`, `lista: list[Paciente]`
- [x] Você consegue instanciar ela via `model_validate()` a partir de um dict com 3 pacientes de teste
- [x] Você escreveu `lookup = {p.id: p.nome for p in resposta.lista}` (sem colar, entendendo cada parte da sintaxe)
- [x] `lookup[<algum_id_de_teste>]` retorna o nome certo
- [x] Você consegue explicar em voz alta (pra si mesmo) por que isso é mais rápido que `for p in lista: if p.id == id: return p.nome`

**Contexto técnico:** isso é o protótipo em miniatura do que o cache SQLite vai fazer de verdade — "dado um id, acho o nome sem bater na API de novo". Não faz parte do sistema final (o dict não persiste), mas o padrão mental é o mesmo.

**Dependências:** nenhuma, você já tem tudo que precisa (models `Paciente`/`Contato` prontos).

---

## 📋 Backlog — Fundamentos Python

### CARD-02: List comprehension geral

**Story:** Como desenvolvedor vindo de PHP/foreach, quero entender a sintaxe `[expressao for item in lista]` isoladamente, antes de combinar com dict, para não confundir os dois conceitos.

**Critérios de aceite:**
- [x] Escreveu 3 exemplos próprios (não copiados): um de transformação (`[x*2 for x in nums]`), um de filtro (`[x for x in nums if x > 10]`), um combinando os dois
- [x] Sabe explicar a equivalência com um `for` tradicional escrevendo as duas versões lado a lado

**Contexto técnico:** isso normalmente vem *antes* do CARD-01 na ordem de aprendizado ideal — se o dict comprehension ainda tá confuso, vale voltar aqui primeiro.

---

### CARD-03: `async`/`await` — conceito

**Story:** Como desenvolvedor que só programou código síncrono (PHP request-response, Laravel), quero entender por que e quando o Python precisa de `async def`/`await`, para não tratar isso como "sintaxe decorativa" no client HTTP.

**Critérios de aceite:**
- [x] Sabe explicar com suas palavras a diferença entre chamar uma função síncrona e dar `await` numa função assíncrona
- [x] Sabe dizer por que `httpx.AsyncClient` precisa de `await client.get(...)` mas `httpx.Client` (versão síncrona) não precisa
- [x] Rodou um exemplo pequeno próprio com `asyncio.run()` chamando uma `async def`

**Contexto técnico:** você vai precisar disso pra escrever o client de verdade (`ClinicaNasNuvensClient`), que já existe como referência mas foi construído por mim — a ideia é você reescrever peças dele entendendo, não só usar.

**Dependências:** nenhuma, mas ajuda ter feito CARD-01/02 antes (aquece a leitura de sintaxe nova).

---

### CARD-04: Context managers (`with` / `async with`)

**Story:** Como desenvolvedor, quero entender por que `with Session(engine) as session:` e `async with self._limiter:` garantem que recursos são liberados sozinhos, para usar esse padrão corretamente em vez de decorar a sintaxe.

**Critérios de aceite:**
- [x] Sabe explicar o que aconteceria se você abrisse uma conexão de banco sem `with` (esquecer de fechar)
- [x] Escreveu um exemplo próprio de `with open(...) as f:` lendo um arquivo texto simples

**Dependências:** nenhuma.

---

### CARD-05: Generators (`yield`)

**Story:** Como desenvolvedor, quero entender por que `iter_clientes()` usa `yield` em vez de retornar uma lista gigante, para não tentar "otimizar" isso incorretamente depois.

**Critérios de aceite:**
- [x] Escreveu uma função geradora simples própria (ex: gerar números pares até N, um por vez)
- [x] Sabe explicar a diferença de memória entre `return lista_com_2000_paginas` e `yield pagina` uma por vez

**Dependências:** ajuda ter feito CARD-03 (async) antes, já que o gerador real é `async def ... yield`.

---

## 📋 Backlog — Client da API

### CARD-06: `PacienteListaResponse` (produção)

**Story:** Como desenvolvedor, quero ter o wrapper de paginação do paciente pronto e testado, para reutilizar no client de verdade.

**Critérios de aceite:**
- [x] Já feito dentro do CARD-01, só formalizar/revisar

**Dependências:** CARD-01.

---

### CARD-07: Models de Agenda, Convênio e Executor (do zero, sem colar)

**Story:** Como desenvolvedor, quero reescrever `AgendaItem`, `Procedimento`, `TipoConvenio` e `ExecutorAgenda` sozinho olhando só o JSON real (sem colar o que já foi construído), para fixar o padrão de alias/opcional por repetição deliberada.

**Critérios de aceite:**
- [x] `TipoConvenio` criado e testado com o dict real do `/tipo-convenio/lista` (esse é o mais simples, sem aninhamento — bom pra começar)
- [x] `ExecutorAgenda` criado e testado — **atenção especial**: precisa lembrar que `idpessoa` é a chave de join com a agenda, não `id`
- [x] `Procedimento` e `AgendaItem` criados e testados com o dict real do `/agenda/lista`

**Contexto técnico:** você já viu esse schema passar na tela várias vezes nessa conversa — o exercício aqui é reescrever de memória/leitura do JSON, não copiar o que já existe no projeto.

**Dependências:** CARD-01 a 02 (dict/list comprehension não são estritamente necessários aqui, mas ajuda ter fluência).

---

### CARD-08: `httpx` síncrono básico (antes de complicar com async)

**Story:** Como desenvolvedor, quero fazer um `GET` simples com `httpx.get()` (sem client assíncrono, sem classe), para isolar "como a lib funciona" de "como asyncio funciona".

**Critérios de aceite:**
- [x] Fez um `httpx.get(url, params={...}, auth=(...), headers={...})` batendo em `/tipo-convenio/lista` de verdade
- [x] Sabe explicar a diferença entre `response.json()` e `response.text`
- [x] Tratou o caso de erro (`response.raise_for_status()`) e viu o que acontece se a URL/credencial estiver errada

**Dependências:** CARD-03 (não é estritamente necessário pra esse card específico, já que é síncrono, mas contextualiza o próximo passo).

---

### CARD-09: Client assíncrono completo (juntando tudo)

**Story:** Como desenvolvedor, quero escrever a classe `ClinicaNasNuvensClient` do zero (auth, headers, rate limiter, paginação, os 4 métodos de listagem), para consolidar async/await + context manager + generator num artefato real e reutilizável.

**Critérios de aceite:**
- [x] Classe com `__init__` configurando `httpx.AsyncClient` com `auth` e `headers`
- [x] Método privado `_get()` usando `async with self._limiter:`
- [x] `listar_tipo_convenio()` e `listar_executor_agenda()` (1 página, síncronos em espírito)
- [x] `listar_agenda_completa()` com paginação em loop
- [x] `iter_clientes()` como gerador assíncrono (streaming de página em página)
- [x] Testado batendo na API real pros 4 endpoints

**Dependências:** CARD-03, 04, 05, 07, 08 — esse é o card que consolida tudo dos fundamentos.

---

## 📋 Backlog — Cache local (SQLModel)

### CARD-10: Conceito SQLModel (comparação com Eloquent)

**Story:** Como desenvolvedor Laravel/Eloquent, quero entender a analogia "classe SQLModel = Model Eloquent, `table=True` = existe migration", para não estranhar a sintaxe.

**Critérios de aceite:**
- [ ] Escreveu uma tabela de teste simples (`Produto` com `id`, `nome`, `preco`) e criou o banco local
- [ ] Sabe apontar a diferença entre o `Paciente` (Pydantic puro, do client HTTP) e o `Paciente` de tabela (SQLModel, do banco) — **atenção:** são conceitos diferentes com nomes parecidos, pode confundir

**Dependências:** nenhuma técnica, mas fica mais fácil depois do CARD-09 (você já vai estar íntimo de `BaseModel`).

---

### CARD-11: Engine, sessão e upsert (`merge`)

**Story:** Como desenvolvedor, quero entender por que se usa `session.merge()` em vez de `session.add()` no sync, para não duplicar registros toda vez que o sync rodar de novo.

**Critérios de aceite:**
- [ ] Rodou o mesmo `merge()` duas vezes seguidas com o mesmo `id` e confirmou que não duplicou (SELECT manual no banco)
- [ ] Sabe explicar o que `add()` faria de diferente (erro de PK duplicada, ou duplicata, dependendo do caso)

**Dependências:** CARD-10.

---

### CARD-12: Sync de convênio (primeiro sync real, 1 página)

**Story:** Como desenvolvedor, quero sincronizar a tabela de convênios com a API real, para ter o primeiro fluxo "API → Pydantic → SQLModel → banco" funcionando de ponta a ponta, no caso mais simples possível (sem paginação).

**Critérios de aceite:**
- [ ] Endpoint `POST /sync/convenios` retorna quantidade sincronizada
- [ ] Rodando 2x seguidas, tabela continua com 49 registros (não duplica)

**Dependências:** CARD-09 (client), CARD-11 (merge).

---

### CARD-13: Sync de executor (mesmo padrão do CARD-12)

**Story:** Igual ao CARD-12, mas pra tabela de executores — reforça o padrão sem novidade conceitual.

**Critérios de aceite:**
- [ ] Endpoint `POST /sync/executores` funcionando
- [ ] Conferiu no banco que `idpessoa` bate com o valor usado na agenda (não confundir com `id`)

**Dependências:** CARD-12.

---

### CARD-14: Sync de paciente (streaming + background)

**Story:** Como desenvolvedor, quero sincronizar as ~2200 páginas de paciente sem travar a aplicação, usando o gerador do CARD-09 e rodando em background, para a base ficar completa localmente sem impactar a experiência de quem for usar o sistema.

**Critérios de aceite:**
- [ ] `POST /sync/pacientes` retorna imediatamente (não espera 20min)
- [ ] `GET /sync/pacientes/status` mostra progresso crescendo
- [ ] Ao final, tabela tem ~110 mil registros (ou o total real da clínica)

**Dependências:** CARD-09, 11, 13.

---

## 📋 Backlog — FastAPI (backend web)

### CARD-15: Rotas GET/POST (comparação com rotas Laravel)

**Story:** Como desenvolvedor Laravel, quero mapear mentalmente `@app.get("/rota")` para `Route::get('/rota', ...)`, para não reaprender o conceito de roteamento do zero.

**Critérios de aceite:**
- [ ] Criou uma rota nova de teste com path param (`/teste/{id}`) e outra com query param

**Dependências:** nenhuma (você já viu isso funcionando, esse card é só formalizar o entendimento).

---

### CARD-16: `BackgroundTasks` (por que o sync de paciente não pode ser síncrono)

**Story:** Como desenvolvedor, quero entender o padrão "retorna rápido, processa depois", para aplicar em qualquer operação longa do sistema, não só no sync de paciente.

**Critérios de aceite:**
- [ ] Sabe explicar o que aconteceria (timeout no navegador) se `/sync/pacientes` fosse síncrono

**Dependências:** CARD-14 (você já viu isso implementado, esse card é reforço conceitual).

---

### CARD-17: Endpoint de export (o objetivo final do projeto)

**Story:** Como usuária final (namorada do Arthur), quero informar data início/fim (e opcionalmente convênio/médico), para receber uma planilha com agendamentos já com nome de paciente/convênio/médico preenchidos, sem precisar fazer isso manualmente.

**Critérios de aceite:**
- [ ] `POST /export` aceita `data_inicial`, `data_final`, `convenio_id` (opcional), `executor_id` (opcional)
- [ ] Busca agenda na API (tempo real) + resolve nomes via cache local (sem chamada de API por paciente)
- [ ] Retorna um job id, roda em background (reaproveita padrão do CARD-16)
- [ ] `GET /export/{id}/status` e `GET /export/{id}/download` funcionando

**Dependências:** CARD-09, 14, 16.

---

### CARD-18: Geração de xlsx

**Story:** Como usuária final, quero abrir a planilha gerada no Excel e já ver as colunas com nome legível (não ids), para não precisar de nenhum tratamento manual depois.

**Critérios de aceite:**
- [ ] Planilha com colunas: data, hora, paciente, telefone, convênio, médico, procedimento, status
- [ ] Testado abrindo no Excel/LibreOffice de verdade

**Dependências:** CARD-17.

---

## 📋 Backlog — Frontend (Vue 3)

### CARD-19: Tela de filtros

**Story:** Como usuária final, quero selecionar data/convênio/médico numa tela simples, para gerar a exportação sem usar terminal ou Postman.

**Critérios de aceite:**
- [ ] Dropdowns de convênio/médico populados a partir de um endpoint que lê o cache local
- [ ] Botão "gerar" chama `/export`

**Dependências:** CARD-17.

---

### CARD-20: Polling de status + download

**Story:** Como usuária final, quero ver uma barra de progresso enquanto a planilha é gerada, para saber que o sistema não travou.

**Critérios de aceite:**
- [ ] Polling a cada ~2s em `/export/{id}/status`
- [ ] Botão de download aparece quando `status == "concluido"`

**Dependências:** CARD-19.

---

## 📋 Backlog — Deploy

### CARD-21: Dockerfile de produção

**Story:** Como desenvolvedor, quero uma imagem sem hot-reload/dependências de dev, para rodar no VPS com menos superfície de erro.

**Dependências:** todo o backend funcional.

### CARD-22: Deploy no VPS (Contabo, ao lado do Fleetis)

**Story:** Como desenvolvedor, quero subir o sistema em produção acessível pra namorada usar de qualquer lugar, não só localhost.

**Dependências:** CARD-21.

### CARD-23: Cron do sync noturno de paciente

**Story:** Como sistema, quero rodar o sync de paciente automaticamente 1x/dia de madrugada, para a base nunca ficar desatualizada sem intervenção manual.

**Dependências:** CARD-22.

---

## Notas técnicas já descobertas (não esquecer)

- `idPessoaExecutor` (agenda) faz join com `idpessoa` do `/executor-agenda/lista` — **não** é o campo `id` desse endpoint.
- `/paciente/lista` tem 2212 páginas → sync completo leva ~18-20min com rate limit de 120/min.
- `/tipo-convenio/lista` e `/executor-agenda/lista` têm 1 página só → sync trivial.
- `/agenda/lista` já retorna telefone, e-mail e nome do procedimento — só falta resolver paciente/convênio/médico por id.
