from django.contrib import admin
from .models import Dealer, CarMake, CarModel, Review


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "city", "state", "zip")
    search_fields = ("full_name", "city", "state")
    list_filter = ("state",)


@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "make")
    list_filter = ("make",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "dealer",
        "user",
        "review",
        "sentiment",
        "created_at",
    )