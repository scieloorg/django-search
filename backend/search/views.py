from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from .search_backend import SearchEngine, SAMPLE_DOCS

@api_view(['GET'])
def search_view(request):
    q = request.GET.get('q')
    if not q:
        return Response({"error": "Missing query parameter 'q'"}, status=400)

    engine = SearchEngine()
    results = engine.search(q)
    return Response({"backend": engine.backend, "results": results})

@api_view(['POST', 'GET'])
def reindex_view(request):
    engine = SearchEngine()
    engine.ensure_index()
    # index sample docs
    for doc in SAMPLE_DOCS:
        engine.index(str(doc["id"]), doc)
    return Response({"status": "ok", "backend": engine.backend, "indexed": len(SAMPLE_DOCS)})