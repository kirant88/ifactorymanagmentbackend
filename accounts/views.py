from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    CustomTokenObtainPairSerializer,
    AdminChangePasswordSerializer,
)
from .permissions import IsSuperAdmin, IsLocationAdminOrSuperAdmin

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom login view that returns JWT tokens with user data."""

    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    """
    Register a new user.
    Only authenticated users with appropriate permissions can create new users.
    """

    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsLocationAdminOrSuperAdmin]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "user": UserSerializer(user).data,
                "message": "User created successfully.",
            },
            status=status.HTTP_201_CREATED,
        )


class LogoutView(APIView):
    """Logout view that blacklists the refresh token."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Successfully logged out."}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get and update current user's profile."""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        """Update user profile (limited fields)."""
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        # Use limited update serializer
        serializer = UserUpdateSerializer(
            instance, data=request.data, partial=partial, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Return full user data
        return Response(UserSerializer(instance).data)


class ChangePasswordView(APIView):
    """Change password for authenticated user."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Password changed successfully."}, status=status.HTTP_200_OK
        )


class UserListView(generics.ListAPIView):
    """
    List all users.
    SuperAdmins see all users.
    LocationAdmins see users from their location.
    """

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsLocationAdminOrSuperAdmin]

    def get_queryset(self):
        user = self.request.user

        if user.is_superadmin:
            # SuperAdmins see all users
            queryset = User.objects.all()
        elif user.is_location_admin:
            # LocationAdmins see users from their location
            queryset = User.objects.filter(location=user.location)
        else:
            # Viewers see no users (shouldn't reach here due to permissions)
            queryset = User.objects.none()

        # Filter by location if provided
        location = self.request.query_params.get("location", None)
        if location and location != "All Locations" and user.is_superadmin:
            queryset = queryset.filter(location=location)

        # Filter by role if provided
        role = self.request.query_params.get("role", None)
        if role:
            queryset = queryset.filter(role=role)

        return queryset


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a user.
    SuperAdmins can manage all users.
    LocationAdmins can manage users from their location.
    """

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsLocationAdminOrSuperAdmin]

    def get_queryset(self):
        user = self.request.user

        if user.is_superadmin:
            return User.objects.all()
        elif user.is_location_admin:
            return User.objects.filter(location=user.location)
        else:
            return User.objects.none()

    def update(self, request, *args, **kwargs):
        """Update user with permission checks."""
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        serializer = UserUpdateSerializer(
            instance, data=request.data, partial=partial, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(UserSerializer(instance).data)

    def destroy(self, request, *args, **kwargs):
        """Delete user with permission checks."""
        instance = self.get_object()

        # Prevent deleting yourself
        if instance == request.user:
            return Response(
                {"error": "You cannot delete your own account."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Only superadmins can delete other superadmins
        if instance.is_superadmin and not request.user.is_superadmin:
            return Response(
                {"error": "Only super admins can delete other super admins."},
                status=status.HTTP_403_FORBIDDEN,
            )

        self.perform_destroy(instance)
        return Response(
            {"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )


class UserResetPasswordView(APIView):
    """Admin endpoint to reset a user's password."""

    permission_classes = [permissions.IsAuthenticated, IsLocationAdminOrSuperAdmin]

    def post(self, request, pk):
        user = generics.get_object_or_404(User, pk=pk)

        # Permission check: can the current user manage this user?
        curr_user = request.user
        if not curr_user.is_superadmin and user.location != curr_user.location:
            return Response(
                {"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
            )

        serializer = AdminChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)

        return Response(
            {"message": "Password reset successfully."}, status=status.HTTP_200_OK
        )


class UserStatsView(APIView):
    """Get user statistics (for dashboard)."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.is_superadmin:
            queryset = User.objects.all()
            # Respect location filter for superadmin if provided
            location = request.query_params.get("location")
            if location and location != "All Locations":
                queryset = queryset.filter(location=location)
        elif user.is_location_admin:
            queryset = User.objects.filter(location=user.location)
        else:
            return Response(
                {"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
            )

        stats = {
            "total_users": queryset.count(),
            "active_users": queryset.filter(is_active=True).count(),
            "inactive_users": queryset.filter(is_active=False).count(),
            "admins_count": queryset.filter(
                role__in=["SUPERADMIN", "LOCATIONADMIN"]
            ).count(),
            "by_role": {
                "superadmin": queryset.filter(role="SUPERADMIN").count(),
                "locationadmin": queryset.filter(role="LOCATIONADMIN").count(),
                "viewer": queryset.filter(role="VIEWER").count(),
            },
        }

        return Response(stats, status=status.HTTP_200_OK)


class LocationListView(APIView):
    """
    Returns a list of all unique locations registered in the system.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from django.apps import apps

        # Models to check for locations
        models_to_check = [
            ("accounts", "User"),
            ("visitors", "Visitor"),
            ("training", "Training"),
            ("maintenance", "Maintenance"),
            ("engagement", "Event"),
            ("engagement", "Collaboration"),
            ("engagement", "SocialMediaPost"),
            ("training", "DigitalMaturityAssessment"),
        ]

        locations = set()
        for app_label, model_name in models_to_check:
            try:
                model = apps.get_model(app_label, model_name)
                # Get distinct values for location field
                locs = (
                    model.objects.exclude(location__isnull=True)
                    .exclude(location="")
                    .values_list("location", flat=True)
                    .distinct()
                )
                locations.update(locs)
            except (LookupError, Exception):
                continue

        return Response(sorted(list(locations)), status=status.HTTP_200_OK)
