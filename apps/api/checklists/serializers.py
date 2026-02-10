from shared.serializers import BaseSerializer
from users.serializers import UserSerializer
from vehicles.serializers import VehicleSerializer


class CheckitemSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'nombre': instance.nombre,
            'activo': instance.activo,
        }


class ChecklistSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'usuario': UserSerializer(instance.usuario).serialize(),
            'vehiculo': VehicleSerializer(instance.vehiculo).serialize(),
            'item': CheckitemSerializer(instance.item).serialize(),
            'creado': instance.creado.isoformat(),
            'actualizado': instance.actualizado.isoformat(),
        }
