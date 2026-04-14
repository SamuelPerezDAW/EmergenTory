from shared.serializers import BaseSerializer


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
        }
