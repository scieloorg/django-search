# Django Search (Elasticsearch + Solr)

Busca em Django 5.1 (Python 3.12) com suporte a **Elasticsearch** e **Solr** via uma camada simples.
Selecione o backend por variável de ambiente `SEARCH_ENGINE` (`elasticsearch` ou `solr`).

## Requisitos
- Docker e Docker Compose

## Subir o ambiente
```bash
docker compose up -d --build
```

A stack sobe:
- **Django**: http://localhost:8000
- **Elasticsearch**: http://localhost:9200
- **Solr**: http://localhost:8983/solr

Por padrão, `SEARCH_ENGINE=elasticsearch` (veja `docker-compose.yml`).

## Testar a API
- Reindex (carrega documentos de exemplo):  
  - `GET/POST http://localhost:8000/search/reindex/`
- Buscar:  
  - `GET http://localhost:8000/search/?q=ciência`

Exemplo de troca para Solr:
```bash
docker compose down
SEARCH_ENGINE=solr docker compose up -d --build
```

Agora `/search/` usa Solr automaticamente.

## Observações
- O Solr core `search_core` é criado pelo comando `solr-precreate` do container.
- Para Elasticsearch, o índice é criado automaticamente com mapeamento simples.
- Código de backend em `search/search_backend.py`.
- Comando de inicialização/população: `python manage.py init_search` (executado automaticamente no entrypoint do serviço).