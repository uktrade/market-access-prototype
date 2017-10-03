# documents.py
#
# for django-elasticsearch-dsl

from elasticsearch_dsl import analyzer  # tokenizer, filter, stemmer
from django_elasticsearch_dsl import DocType, Index, fields
from .models import BarrierRecord

# Name of the Elasticsearch index
case = Index('market-access-barriers-demo')

# See Elasticsearch Indices API reference for available settings
case.settings(
    number_of_shards=1,
    number_of_replicas=0
)

# not used yet
custom_analyzer = analyzer(
    'custom_analyzer',
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    # char_filter=["html_strip"]
)


@case.doc_type
class CaseDocument(DocType):

    class Meta:
        model = BarrierRecord  # The model associate with this DocType
        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'title', 'description',
            # actually these should be facets
            'products_text', 'sectors_text',
        ]

        # To ignore auto updating of Elasticsearch when a model is save
        # or delete
        # ignore_signals = True
        # Don't perform an index refresh after every update
        # (overrides global setting)
        # auto_refresh = False
