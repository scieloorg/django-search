# SciELO Search (Elasticsearch + Solr)

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

## Requisitos Funcionais

- **Interface gráfica de pesquisa** amigável e responsiva  
- **Pesquisa integrada e contextualizada** (suporte a *clusters*)  
- **Suporte a estratégias de busca** com operadores booleanos  
  - Exemplo: `dengue OR malaria`, `dengue AND malaria`  
- **Consulta flexível**, sem a complexidade de uma pesquisa avançada, mas com liberdade para uso de estratégias personalizadas  
- **Exportação de clusters (conjuntos)** em CSV e **geração de gráficos** dinâmicos  
- **Ordenação** de resultados  
- **Paginação** configurável  
- **Alteração da quantidade de itens por página**  
- **Internacionalização (i18n)** — suporte a múltiplos idiomas  
- **Clusters colapsáveis** (expandir/recolher)  
- **Tipos de cluster configuráveis:** *listbox*, *checkbox* e *multi-select*  
- **Filtro por intervalo de datas**  
- **Ações em massa:** selecionar itens para **Imprimir**, **Enviar por e-mail**, **Exportar** ou **Compartilhar**  
- **Destaque do termo buscado** nos resultados de pesquisa  


## Requisitos Não Funcionais

- **Compatibilidade com Django** — deve ser possível integrar a solução como um app Django  
- **Compatibilidade com mecanismos de busca**: Solr, Elasticsearch e OpenSearch  
- **Instalação via `INSTALLED_APPS`** no Django  
- **Geração de logs de pesquisa**  
- **Suporte a busca por proximidade (proximity search)**  
- **Clusters dinâmicos** — capacidade de **adicionar e remover** clusters em tempo de execução  
- **Configuração dinâmica de parâmetros de pesquisa padrão**  
- **Capacidade de exclusão dinâmica de conteúdos**  
- **Ordenação dinâmica dos clusters**  

## Fluxo de trabalho

- **Criar EPIC a partir da branch develop**
  git checkout develop
  git pull origin develop
  git checkout -b EPICNAME

- **Criar as features**
  git checkout EPICNAME
  git checkout -b TASKNAME

- **Após o desenvolvimento**
  git add .
  git commit -m "feat: implementação inicial da UI de clusters"
  git push -u origin EPICNAME

- **Revisão do EPIC**

- **Merge para EPIC em develop**
  git checkout develop
  git pull origin develop
  git merge --no-ff epic/<nome-epic> -m "merge: incorporação do EPIC <nome-epic>"
  git push origin develop

- **Após aprovado em develop merge para a Main**
  git checkout main
  git pull origin main
  git merge --no-ff develop -m "release: integração do EPIC <nome-epic>"
  git push origin main
