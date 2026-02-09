from shared.serializers import BaseSerializer
from users.serializers import UserSerializer
from vehicles.serializers import VehicleSerializer


class CheckitemSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'title': instance.title,
            'slug': instance.slug,
            'content': instance.content,
            'created_at': instance.created_at.isoformat(),
            'updated_at': instance.updated_at.isoformat(),
        }


class ChecklistSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'user': UserSerializer(instance.user).serialize(),
            'vehicle': VehicleSerializer(instance.vehicle).serialize(),
            'checkitem': CheckitemSerializer(instance.checkitem).serialize(),
            'created_at': instance.created_at.isoformat(),
            'updated_at': instance.updated_at.isoformat(),
        }
