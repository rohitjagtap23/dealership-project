from django.contrib import admin
from django.urls import path

from dealership import views


urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.home, name="home"),

    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),

    path(
        "api/dealers",
        views.get_all_dealers,
        name="get_all_dealers"
    ),

    path(
        "api/dealers/<int:dealer_id>",
        views.get_dealer_by_id,
        name="get_dealer_by_id"
    ),

    path(
        "api/dealers/state/<str:state>",
        views.get_dealers_by_state,
        name="get_dealers_by_state"
    ),

    path(
        "api/dealers/<int:dealer_id>/reviews",
        views.get_dealer_reviews,
        name="get_dealer_reviews"
    ),

    path(
        "api/carmakes",
        views.get_all_car_makes,
        name="get_all_car_makes"
    ),

    path(
        "api/register",
        views.register_user,
        name="register_user"
    ),

    path(
        "api/login",
        views.login_user,
        name="login_user"
    ),

    path(
        "api/logout",
        views.logout_user,
        name="logout_user"
    ),
    
    path(
    "api/dealers/<int:dealer_id>/reviews/create",
    views.create_review,
    name="create_review"
    ),
    path(
    "api/analyze-review",
    views.analyze_review,
    name="analyze_review"
    ),
]