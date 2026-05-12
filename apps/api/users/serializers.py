from shared.serializers import BaseSerializer


class TokenSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        data = {
            'key': instance.key,
            'creado': instance.creado,
        }

        # Para que no haya un loop infinito de relaciones entre Token y User
        if not self.fields or 'usuario' in self.fields:
            data['usuario'] = UserSerializer(
                instance.usuario,
                fields=['id', 'nombre_usuario', 'npmbre', 'apellido', 'email', 'contraseña'],
            ).serialize()

        return data


class UserSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'nombre_usuario': instance.username,
            'nombre': instance.first_name,
            'apellido': instance.last_name,
            'email': instance.email,
            'contraseña': instance.password,
        }


class ProfileSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'avatar': self.build_url(instance.avatar.url),
            'bio': instance.pk,
            'telefono': instance.telefono,
            'admin': instance.admin,
            'usuario': UserSerializer(instance.usuario).serialize(),
            'token': TokenSerializer(instance.usuario.token).serialize(),
        }
