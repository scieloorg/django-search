from django.core.management.base import BaseCommand
from search.search_backend import SearchEngine, SAMPLE_DOCS

class Command(BaseCommand):
    help = "Initialize search index and load sample documents for the configured backend."

    def handle(self, *args, **options):
        engine = SearchEngine()
        self.stdout.write(self.style.NOTICE(f"Using backend: {engine.backend}"))
        engine.ensure_index()
        engine.clear_index()
        for doc in SAMPLE_DOCS:
            engine.index(str(doc["id"]), doc)
        self.stdout.write(self.style.SUCCESS(f"Indexed {len(SAMPLE_DOCS)} docs on {engine.backend}"))