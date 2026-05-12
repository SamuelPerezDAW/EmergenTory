from shared.serializers import BaseSerializer


class VehicleSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        data = {
            'id': instance.pk if not isinstance(instance, dict) else instance['pk'],
            'matricula': instance.matricula
            if not isinstance(instance, dict)
            else instance['matricula'],
            'marca': instance.marca if not isinstance(instance, dict) else instance['marca'],
            'modelo': instance.modelo if not isinstance(instance, dict) else instance['modelo'],
            'categoria': instance.categoria
            if not isinstance(instance, dict)
            else instance['categoria'],
        }

        if not isinstance(instance, dict):
            if instance.imagen:
                data['imagen'] = self.build_url(instance.imagen.url)

            else:
                data['imagen'] = ''

        else:
            if instance['imagen']:
                data['imagen'] = self.build_url(instance['imagen'].url)

            else:
                data['imagen'] = ''

        if not self.fields or 'lista' in self.fields:
            data['lista'] = instance['lista']

        return data
