from rest_framework import serializers

from constants import help_text
from data import Publication
from interfaces.serializers.base import BaseSerializer, URLField
from interfaces.serializers.relationships import RelationshipSerializer


class PublicationListSerializer(BaseSerializer):
    _data_model = Publication

    # properties
    pmid = serializers.IntegerField(required=True, min_value=0, help_text=help_text.pmid)
    doi = serializers.CharField(required=False, max_length=250, help_text=help_text.doi)
    title = serializers.CharField(required=False, max_length=500, help_text=help_text.title)
    author = serializers.CharField(required=False, max_length=250, help_text=help_text.author)
    year = serializers.IntegerField(required=False, min_value=0, help_text=help_text.year)

    # url
    url = URLField(read_only=True,
                   view_name='publications-detail',
                   lookup_field='protrend_id',
                   lookup_url_kwarg='protrend_id')


class PublicationDetailSerializer(PublicationListSerializer):
    url = None

    # relationships
    tfbs = RelationshipSerializer(read_only=True,
                                  child=serializers.HyperlinkedRelatedField(
                                      read_only=True,
                                      view_name='binding-sites-detail',
                                      lookup_field='protrend_id',
                                      lookup_url_kwarg='protrend_id'))
    regulatory_interaction = RelationshipSerializer(read_only=True,
                                                    child=serializers.HyperlinkedRelatedField(
                                                        read_only=True,
                                                        view_name='interactions-detail',
                                                        lookup_field='protrend_id',
                                                        lookup_url_kwarg='protrend_id'))
