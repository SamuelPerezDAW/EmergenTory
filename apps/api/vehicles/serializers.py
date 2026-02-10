from shared.serializers import BaseSerializer
from users.serializers import UserSerializer


class VehicleSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'matricula': instance.matricula,
            'marca': instance.marca,
            'modelo': instance.modelo,
            'categoria': instance.categoria,
            'usuario': UserSerializer(instance.usuario).serialize(),
        }
