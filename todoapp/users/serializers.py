from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token


# Add your serializers
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=self.context.get(
            'request'), email=email, password=password)

        if not user:
            msg = 'Unable to log in with provided credentials.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=get_user_model().objects.all())
        ]
    )
    token = serializers.SerializerMethodField(
        method_name='get_auth_token', read_only=True)

    def get_auth_token(self, instance):
        token = Token.objects.get_or_create(user=instance)
        return token[0].key

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name',
                  'date_joined', 'password', 'email', 'token']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['date_joined']
