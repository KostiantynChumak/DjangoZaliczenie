from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.db.models import Avg, query 

def home(request):
    query = request.GET.get("title")
    allRestaurants = None
    if query:
        allRestaurants = Restaurant.objects.filter(name__icontains=query)
    else:
        allRestaurants = Restaurant.objects.all()

    context = {
        "restaurants": allRestaurants,
    }
    return render(request, 'main/index.html', context)

def detail(request, id):
    restaurant = Restaurant.objects.get(id=id)
    reviews = Review.objects.filter(restaurant=id).order_by("-comment")

    average = reviews.aggregate(Avg("rating"))["rating__avg"]
    if average == None:
        average = 0
    average = round(average, 2)
    print(average)
    context = {
        "restaurant": restaurant,
        "reviews": reviews,
        "average": average
    }
    return render(request, 'main/details.html', context)

def add_restaurants(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == "POST":
                form = RestaurantForm(request.POST or None)

                if form.is_valid():
                    data = form.save(commit=False)
                    data.save()
                    return redirect("main:home")
            else:
                form = RestaurantForm()
            return render(request, 'main/addrestaurants.html', {"form": form, "controller": "Add Restaurants"})
        else:
            return redirect("main:home")
        return redirect("accounts:login")

def edit_restaurants(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            restaurant = Restaurant.objects.get(id=id)

            if request.method == "POST":
                form = RestaurantForm(request.POST or None, instance=restaurant)
                if form.is_valid():
                    data = form.save(commit=False)
                    data.save()
                    return redirect("main:detail", id)
            else:
                form = RestaurantForm(instance=restaurant)
            return render(request, 'main/addrestaurants.html', {"form": form, "controller": "Edit Restaurants"})
        else:
            return redirect("main:home")
    return redirect("accounts:login")

def delete_restaurants(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            restaurant = Restaurant.objects.get(id=id)
            restaurant.delete()
            return redirect("main:home")
        else:
            return redirect("main:home")
        return redirect("accounts:login")

def add_review(request, id):
    if request.user.is_authenticated:
        restaurant = Restaurant.objects.get(id=id)
        if request.method == "POST":
            form = ReviewForm(request.POST or None)
            if form.is_valid():
                data = form.save(commit=False)
                data.comment = request.POST["comment"]
                data.rating = request.POST["rating"]
                data.user = request.user
                data.restaurant = restaurant
                data.save()
                return redirect("main:detail", id)
        else:
            form = ReviewForm()
        return render(request, 'main/details.html', {"form": form})
    else:
        return redirect("accounts:login")


def edit_review(request, restaurant_id, review_id):
    if request.user.is_authenticated:
        restaurant = Restaurant.objects.get(id=restaurant_id)

        review = Review.objects.get(restaurant=restaurant, id=review_id)
        if request.user == review.user:
            if request.method == "POST":
                form = ReviewForm(request.POST, instance=review)
                if form.is_valid():
                    data = form.save(commit=False)
                    if (data.rating > 10) or (data.rating < 0):
                         error = "Out or range. Please select rating from 0 to 10."
                         return render(request, 'main/editreview.html', {"error": error, "form": form})
                    else:
                        data.save()
                        return redirect("main:detail", restaurant_id)
            else:
                form = ReviewForm(instance=review)
            return render(request, 'main/editreview.html', {"form": form})
        else:
            return redirect("main:detail", restaurant_id)
    else:
        return redirect("accounts:login")

def delete_review(request, restaurant_id, review_id):
    if request.user.is_authenticated:
        restaurant = Restaurant.objects.get(id=restaurant_id)
        # review
        review = Review.objects.get(restaurant=restaurant, id=review_id)

        # check if the review was done by the logged in user
        if request.user == review.user:
            # grant permission to delete
            review.delete()

        return redirect("main:detail", restaurant_id)
            
    else:
        return redirect("accounts:login")

def edit_review(request, restaurant_id, review_id):
    if request.user.is_authenticated:
        restaurant = Restaurant.objects.get(id=restaurant_id)
        review = Review.objects.get(restaurant=restaurant, id=review_id)
        if request.user == review.user:
            if request.method == "POST":
                form = ReviewForm(request.POST, instance=review)
                if form.is_valid():
                    data = form.save(commit=False)
                    if (data.rating > 10) or (data.rating < 0):
                        error = "Out of range. Please select rating from 0 to 5."
                        return render(request, 'main/editreview.html', {"error": error, "form": form})
                    else:
                        data.save()
                        return redirect("main:detail", restaurant_id)
            else:
                form = ReviewForm(instance=review)
            return render(request, 'main/editreview.html', {"form": form})
        else:
            return redirect("main:detail", restaurant_id)
    else:
        return redirect("account:login")

def delete_review(request, restaurant_id, review_id):
    if request.user.is_authenticated:
        restaurant = Restaurant.objects.get(id=restaurant_id)
        review = Review.objects.get(restaurant=restaurant, id=review_id)
        if request.user == review.user:
            review.delete()
        return redirect("main:detail", restaurant_id)
    else:
        return redirect("account:login")
