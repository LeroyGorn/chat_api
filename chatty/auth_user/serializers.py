from auth_user.models import CustomUser
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    """
    This serializer is used for serializing and validating data related to the CustomUser model.
    It also has a create method that creates a CustomUser object with validated data and
    a validate method that ensures password and check_password fields match.
    """
    check_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'password',
            'check_password',
            'first_name',
            'last_name',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        return CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['check_password']:
            raise serializers.ValidationError({'password': 'Password fields did not match.'})
        return attrs


class CustomObtainTokenSerializer(TokenObtainPairSerializer):
    """
    This serializer is used for obtaining JWT tokens for a given user.
    It extends the TokenObtainPairSerializer provided by rest_framework_simplejwt library and
    adds more user-related data to the token payload.
    It includes id, email, first_name, and last_name fields in the returned token.
    It also has a validate method that gets the token from the parent class and
    adds the additional user-related data to the token payload.
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['id'] = self.user.id
        data['email'] = self.user.email
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        return data

    @classmethod
    def get_token(cls, user):
        token = super(CustomObtainTokenSerializer, cls).get_token(user)
        token['id'] = user.id
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        return token
