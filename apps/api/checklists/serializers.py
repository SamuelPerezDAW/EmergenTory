from shared.serializers import BaseSerializer
from users.serializers import UserSerializer
from vehicles.serializers import VehicleSerializer

from .models import Checkitem


class ChecklistSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        items = Checkitem.objects.filter(checklist=instance)
        data = {
            'id': instance.pk,
            'usuario': UserSerializer(instance.usuario).serialize() if instance.usuario else None,
            'creado': instance.creado.isoformat(),
            'actualizado': instance.actualizado.isoformat(),
        }

        # Para que no haya un loop infinito de relaciones entre Checklist y items/vehiculo
        if not self.fields or 'items' in self.fields:
            data['items'] = CheckitemSerializer(
                items, fields=['id', 'nombre', 'activo']
            ).serialize()

        if not self.fields or 'vehiculo' in self.fields:
            data['vehiculo'] = VehicleSerializer(
                instance.vehiculo,
                fields=['id', 'matricula', 'imagen', 'marca', 'modelo', 'categoria'],
            ).serialize()

        return data


class CheckitemSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        data = {
            'id': instance.pk,
            'nombre': instance.nombre,
            'activo': instance.activo,
        }

        if not self.fields or 'checklist' in self.fields:
            data['checklist'] = ChecklistSerializer(
                instance.checklist,
                fields=['id', 'vehiculo'],
            ).serialize()

        return data
