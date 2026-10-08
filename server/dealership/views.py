from textblob import TextBlob
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import json

from .models import Dealer, CarMake, CarModel, Review


# -------------------------
# HTML PAGES
# -------------------------

def home(request):
    return render(request, "dealership/home.html")


def about(request):
    return render(request, "dealership/About.html")


def contact(request):
    return render(request, "dealership/Contact.html")


# -------------------------
# DEALER APIs
# -------------------------

def get_all_dealers(request):
    dealers = Dealer.objects.all()

    data = []

    for dealer in dealers:
        data.append({
            "id": dealer.id,
            "full_name": dealer.full_name,
            "city": dealer.city,
            "state": dealer.state,
            "address": dealer.address,
            "zip": dealer.zip,
            "lat": dealer.lat,
            "lng": dealer.lng
        })

    return JsonResponse(data, safe=False)


def get_dealer_by_id(request, dealer_id):
    try:
        dealer = Dealer.objects.get(id=dealer_id)
    except Dealer.DoesNotExist:
        return JsonResponse(
            {"error": "Dealer not found"},
            status=404
        )

    return JsonResponse({
        "id": dealer.id,
        "full_name": dealer.full_name,
        "city": dealer.city,
        "state": dealer.state,
        "address": dealer.address,
        "zip": dealer.zip,
        "lat": dealer.lat,
        "lng": dealer.lng
    })


def get_dealers_by_state(request, state):
    dealers = Dealer.objects.filter(state__iexact=state)

    data = []

    for dealer in dealers:
        data.append({
            "id": dealer.id,
            "full_name": dealer.full_name,
            "city": dealer.city,
            "state": dealer.state,
            "address": dealer.address,
            "zip": dealer.zip
        })

    return JsonResponse(data, safe=False)


def get_dealer_reviews(request, dealer_id):
    reviews = Review.objects.filter(
        dealer_id=dealer_id
    ).select_related("user")

    data = []

    for review in reviews:
        data.append({
            "id": review.id,
            "dealer_id": review.dealer_id,
            "username": review.user.username,
            "review": review.review,
            "sentiment": review.sentiment,
            "created_at": review.created_at.isoformat()
        })

    return JsonResponse(data, safe=False)


# -------------------------
# CAR MAKE / MODEL API
# -------------------------

def get_all_car_makes(request):
    makes = CarMake.objects.prefetch_related("models")

    data = []

    for make in makes:
        data.append({
            "id": make.id,
            "name": make.name,
            "models": [
                {
                    "id": model.id,
                    "name": model.name
                }
                for model in make.models.all()
            ]
        })

    return JsonResponse(data, safe=False)


# -------------------------
# USER REGISTRATION
# -------------------------

@csrf_exempt
def register_user(request):

    if request.method != "POST":
        return JsonResponse(
            {"error": "POST required"},
            status=405
        )

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    username = body.get("username")
    password = body.get("password")
    email = body.get("email", "")

    if not username or not password:
        return JsonResponse(
            {"error": "Username and password are required"},
            status=400
        )

    if User.objects.filter(username=username).exists():
        return JsonResponse(
            {"error": "Username already exists"},
            status=400
        )

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email
    )

    return JsonResponse({
        "message": "User registered successfully",
        "username": user.username
    }, status=201)


# -------------------------
# LOGIN
# -------------------------

@csrf_exempt
def login_user(request):

    if request.method != "POST":
        return JsonResponse(
            {"error": "POST required"},
            status=405
        )

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    username = body.get("username")
    password = body.get("password")

    user = authenticate(
        request,
        username=username,
        password=password
    )

    if user is None:
        return JsonResponse(
            {"error": "Invalid credentials"},
            status=401
        )

    login(request, user)

    return JsonResponse({
        "message": "Login successful",
        "username": user.username
    })


# -------------------------
# LOGOUT
# -------------------------

@csrf_exempt
def logout_user(request):

    logout(request)

    return JsonResponse({
        "message": "Logout successful"
    })

@csrf_exempt
def create_review(request, dealer_id):
    if request.method != "POST":
        return JsonResponse(
            {"error": "POST required"},
            status=405
        )

    if not request.user.is_authenticated:
        return JsonResponse(
            {"error": "Authentication required"},
            status=401
        )

    try:
        dealer = Dealer.objects.get(id=dealer_id)
    except Dealer.DoesNotExist:
        return JsonResponse(
            {"error": "Dealer not found"},
            status=404
        )

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    review_text = body.get("review", "").strip()

    if not review_text:
        return JsonResponse(
            {"error": "Review is required"},
            status=400
        )

    review = Review.objects.create(
        dealer=dealer,
        user=request.user,
        review=review_text,
        sentiment=""
    )

    return JsonResponse({
        "message": "Review created successfully",
        "id": review.id,
        "dealer_id": dealer.id,
        "username": request.user.username,
        "review": review.review,
        "sentiment": review.sentiment
    }, status=201)
def analyze_review(request):
    review_text = request.GET.get("review", "").strip()

    if not review_text:
        return JsonResponse(
            {"error": "Review text is required"},
            status=400
        )

    polarity = TextBlob(review_text).sentiment.polarity

    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return JsonResponse({
        "review": review_text,
        "sentiment": sentiment,
        "polarity": polarity
    })