from shared.serializers import BaseSerializer


class VehicleSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'matricula': instance.matricula,
            'imagen': self.build_url(instance.imagen.url),
            'marca': instance.marca,
            'modelo': instance.modelo,
            'categoria': instance.categoria,
        }
