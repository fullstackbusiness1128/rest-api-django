from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets

User = get_user_model()


# Both the .create() and .update() methods are optional. You can implement either none, one, or both of them,
# depending on the use-case for your serializer class.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'email', 'username', 'is_staff', 'is_superuser', 'status', 'role',
            'password'
        )

        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):  # .save() will create a new instance.
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):  # .save() will update the existing `user` instance.
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = {
            'id': instance.id,
            # 'full_name': instance.get_full_name(),
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'username': instance.username,
            'email': instance.email,
            'is_staff': instance.is_staff,
            'is_superuser': instance.is_superuser,
            # 'role': instance.get_role_display(),
            # 'status': instance.get_status_display(),
            'role': instance.role,
            'status': instance.status,
        }
        return representation


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer = UserSerializer()


class Comment:
    def __init__(self, email, content):
        self.email = email
        self.content = content


class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return Comment(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        return instance
