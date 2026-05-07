from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomTokenObtainPairView,
    RegisterView,
    LogoutView,
    UserProfileView,
    ChangePasswordView,
    UserListView,
    UserDetailView,
    UserStatsView,
    UserResetPasswordView,
    LocationListView,
)

urlpatterns = [
    # Authentication
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # User Profile
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    # User Management (Admins Only)
    path("users/", UserListView.as_view(), name="user_list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path(
        "users/<int:pk>/reset-password/",
        UserResetPasswordView.as_view(),
        name="user_reset_password",
    ),
    path("users/stats/", UserStatsView.as_view(), name="user_stats"),
    path("locations/", LocationListView.as_view(), name="location_list"),
]
