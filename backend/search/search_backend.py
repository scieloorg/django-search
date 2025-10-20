import os
from typing import List, Dict
import pysolr
from elasticsearch import Elasticsearch, NotFoundError
from django.conf import settings

SAMPLE_DOCS: List[Dict] = [
    {"id": 1, "title": "Ciência e Sociedade", "content": "Análise sobre inovação e impacto social."},
    {"id": 2, "title": "Django com Solr e Elasticsearch", "content": "Guia prático de integração híbrida."},
    {"id": 3, "title": "Elasticsearch para iniciantes", "content": "Conceitos de índice, documento e consulta."},
    {"id": 4, "title": "Solr avançado", "content": "Schema, copyField e relevância."},
    {"id": 5, "title": "Pesquisa full-text", "content": "Tokenização, stemming e stopwords."},
]

class SearchEngine:
    def __init__(self):
        self.backend = settings.SEARCH_ENGINE.lower()
        if self.backend == "solr":
            self.client = pysolr.Solr(settings.SOLR_URL, always_commit=True, timeout=10)
        else:
            # default elasticsearch
            self.client = Elasticsearch(settings.ELASTIC_URL)
            self.index_name = getattr(settings, "ELASTIC_INDEX", "search_index")

    def ensure_index(self):
        if self.backend == "solr":
            # core is precreated via docker-compose (solr-precreate search_core)
            # we can try a ping
            try:
                self.client.ping()
            except Exception as e:
                raise RuntimeError(f"Solr core not ready: {e}")
        else:
            # ensure elastic index exists with a simple mapping
            if not self.client.indices.exists(index=self.index_name):
                body = {
                    "settings": {"number_of_shards": 1, "number_of_replicas": 0},
                    "mappings": {
                        "properties": {
                            "title": {"type": "text"},
                            "content": {"type": "text"}
                        }
                    }
                }
                self.client.indices.create(index=self.index_name, body=body)

    def clear_index(self):
        if self.backend == "solr":
            self.client.delete(q="*:*")
        else:
            try:
                self.client.delete_by_query(index=self.index_name, body={"query": {"match_all": {}}})
            except NotFoundError:
                pass

    def index(self, doc_id, body):
        if self.backend == "solr":
            # Solr expects 'id' field
            if "id" not in body:
                body = {**body, "id": doc_id}
            self.client.add([body])
        else:
            self.client.index(index=self.index_name, id=doc_id, document=body, refresh=True)

    def search(self, query):
        if self.backend == "solr":
            # Default search across all text fields
            results = self.client.search(query)
            out = []
            for r in results:
                # normalize keys for output parity
                item = {"id": r.get("id")}
                if "title" in r:
                    item["title"] = r["title"][0] if isinstance(r["title"], list) else r["title"]
                if "content" in r:
                    item["content"] = r["content"][0] if isinstance(r["content"], list) else r["content"]
                out.append(item)
            return out
        else:
            q = {"query": {"multi_match": {"query": query, "fields": ["title", "content"]}}}
            res = self.client.search(index=self.index_name, body=q)
            return [hit["_source"] for hit in res["hits"]["hits"]]