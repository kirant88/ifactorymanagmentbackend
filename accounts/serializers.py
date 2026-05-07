from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "role",
            "location",
            "organization_name",
            "phone",
            "is_active",
            "date_joined",
            "last_login",
        ]
        read_only_fields = ["id", "date_joined", "last_login"]

    def get_full_name(self, obj):
        return obj.get_full_name()


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new users."""

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "password_confirm",
            "first_name",
            "last_name",
            "role",
            "location",
            "organization_name",
            "phone",
        ]

    def validate(self, attrs):
        """Validate that passwords match."""
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def validate_role(self, value):
        """Validate role assignment based on requesting user's permissions."""
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            # Only superadmins can create other superadmins
            if value == "SUPERADMIN" and not request.user.is_superadmin:
                raise serializers.ValidationError(
                    "Only super admins can create other super admins."
                )
        return value

    def create(self, validated_data):
        """Create a new user with encrypted password."""
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user information."""

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "role",
            "location",
            "organization_name",
            "phone",
            "is_active",
        ]

    def validate_role(self, value):
        """Validate role changes based on requesting user's permissions."""
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            # Only superadmins can change roles to/from superadmin
            instance = self.instance
            if (
                value == "SUPERADMIN" or instance.role == "SUPERADMIN"
            ) and not request.user.is_superadmin:
                raise serializers.ValidationError(
                    "Only super admins can modify super admin roles."
                )
        return value


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change endpoint."""

    old_password = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(
        required=True, write_only=True, validators=[validate_password]
    )
    password_confirm = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        """Validate that passwords match."""
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def validate_old_password(self, value):
        """Validate that old password is correct."""
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def save(self, **kwargs):
        """Update user's password."""
        user = self.context["request"].user
        user.set_password(self.validated_data["password"])
        user.save()
        return user


class AdminChangePasswordSerializer(serializers.Serializer):
    """Serializer for admin to change another user's password."""

    password = serializers.CharField(
        required=True, write_only=True, validators=[validate_password]
    )
    password_confirm = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def save(self, user):
        user.set_password(self.validated_data["password"])
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT token serializer to include user data."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token["email"] = user.email
        token["role"] = user.role
        token["location"] = user.location
        token["organization_name"] = user.organization_name
        token["full_name"] = user.get_full_name()
        return token

    def validate(self, attrs):
        """Validate and return token with user data."""
        data = super().validate(attrs)
        # Add user data to response
        data["user"] = UserSerializer(self.user).data

        return data
