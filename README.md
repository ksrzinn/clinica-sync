# clinica-sync

Automação de exportação de agenda (Clínica nas Nuvens → xlsx), rodando 100% em Docker.

## 1. Instalar o Docker (só uma vez)

**Windows / Mac:** instale o **Docker Desktop**: https://www.docker.com/products/docker-desktop/
Depois de instalar, abre o Docker Desktop e deixa rodando em background (ícone na bandeja/menu bar).

**Linux:** instale o Docker Engine:
```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
# depois disso, faz logout/login pra não precisar de sudo
```

Confirma que instalou certo:
```bash
docker --version
docker compose version
```

## 2. Configurar credenciais

Edita o arquivo `.env` (já criado a partir do `.env.example`) com as credenciais da API
(Configurações -> Minha Empresa -> Integrações -> API Clínica nas Nuvens, dentro do sistema).

## 3. Subir o projeto

Na raiz do projeto (onde está o `docker-compose.yml`):
```bash
docker compose up --build
```

Primeira vez demora um pouco (baixa a imagem Python e instala as deps). Depois disso é rápido.

Confirma que subiu certo abrindo no navegador:
```
http://localhost:8000/health
```
Deve responder `{"status":"ok"}`.

## 4. Desenvolvimento

- Qualquer arquivo em `backend/app/` é montado direto no container (bind mount) — você edita local
  no seu editor normalmente, o `uvicorn --reload` detecta e reinicia sozinho. **Não precisa de Python
  instalado na sua máquina, nem rebuildar a imagem** pra mudanças de código.
- Só precisa `docker compose up --build` de novo se mexer no `requirements.txt` ou no `Dockerfile`.
- Pra parar: `Ctrl+C` ou `docker compose down` (em outro terminal).
- Pra ver logs sem travar o terminal: `docker compose logs -f backend`.

## Estrutura

```
clinica-sync/
├── docker-compose.yml
├── .env                  # credenciais (fora do git)
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       └── main.py       # FastAPI app
```

## Próximos passos (ainda não implementado)

- [ ] Client HTTP pra API Clínica nas Nuvens (auth Basic + header `clinicaNasNuvens-cid`)
- [ ] Rate limiter (120 req/min) + cache local (SQLite) de pacientes/convênios
- [ ] Endpoint `POST /export` com filtros de data/convênio/médico
- [ ] Geração do xlsx
- [ ] Frontend Vue 3 consumindo a API
