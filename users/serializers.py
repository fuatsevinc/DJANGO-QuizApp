from rest_framework import serializers, validators
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'},
        label='Password', 
        help_text='Enter Password',
        validators=[validate_password]
        )
    password2 = serializers.CharField(
        style={'input_type': 'password'}, 
        write_only=True,
        required=True,
        label='Password Confirmation',
        help_text='Enter Password again to confirm',
        validators=[validate_password],
        )
    username = serializers.CharField(


        validators=[validators.UniqueValidator(
            queryset=User.objects.all(),
            message='Username already exists'
            )]
    )
    email = serializers.CharField(
        required=True,
        allow_blank=False,
        label='Email',
        help_text='Email',
        validators=[
            validators.UniqueValidator(
                queryset=User.objects.all(),
                message='This email is already in use.'
            )
            ])

    class Meta:
        model = User
        fields = (
            'username', 
            'email',
            "first_name",
            "last_name",
            'password',
            "password2"
            )

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("password2")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')