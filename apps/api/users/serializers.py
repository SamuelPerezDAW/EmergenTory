from shared.serializers import BaseSerializer


class UserSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'username': instance.username,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'email': instance.email,
        }


class ProfileSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'avatar': self.build_url(instance.avatar.url),
            'bio': instance.pk,
            'phone_number': instance.phone_number,
            'admin': instance.admin,
            'user': UserSerializer(instance.user).serialize(),
        }
