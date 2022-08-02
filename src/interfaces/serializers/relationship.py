from rest_framework import serializers


# --------------------------------------
# Relationship Serializers
# --------------------------------------
class RelationshipSerializer(serializers.ListSerializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class SourceRelationshipSerializer(RelationshipSerializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
