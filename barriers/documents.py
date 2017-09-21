# documents.py
#
# for django-elasticsearch-dsl

from elasticsearch_dsl import analyzer  # tokenizer, filter, stemmer
from django_elasticsearch_dsl import DocType, Index, fields
from .models import MarketAccessBarrier

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

    # remember Django gives us an 'id' primary key by default, we don't have to define one
    wto_symbol = fields.TextField()
    # turn this into a country lookup code?? make it one:many?
    notifying_member = fields.TextField()
    title = fields.TextField()
    description = fields.TextField()
    distribution_date = fields.DateField()
    products_text = fields.TextField()
    product_codes = fields.TextField()
    objectives = fields.TextField()
    # SPS only
    keywords = fields.TextField()
    # SPS only
    regions_affected = fields.TextField()
    comments_due_date = fields.TextField()
    notification_type = fields.TextField()
    # don't need to index this?
    # document_link = fields.TextField()
    # wto_link = fields.TextField()

    class Meta:
        model = MarketAccessBarrier  # The model associate with this DocType
        # The fields of the model you want to be indexed in Elasticsearch
        #fields = [
        #    # The only one left that isn't a custom field!
        #]

        # To ignore auto updating of Elasticsearch when a model is save
        # or delete
        # ignore_signals = True
        # Don't perform an index refresh after every update
        # (overrides global setting)
        # auto_refresh = False
