from django.shortcuts import render, HttpResponse, redirect
import bcrypt
from django.contrib import messages
from apps.quoteDash_app.models import *

def index(request):

    return render(request, "index.html")

def success(request):
    # recent = Review.objects.all().order_by('-id')
    # print("recent reviews",recent)
    context = {
        "quotes" : Quote.objects.all()
    }
    return render(request, "quotes.html", context)

def register(request):
    errors = User.objects.basic_validatorRegister(request.POST)
    print(errors)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
            print("message are:", messages)
        return redirect("/")
    else:
        User.objects.create(
            first_name = request.POST["first_name"],
            last_name = request.POST["last_name"],
            email = request.POST["email1"],
            password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
            )
        request.session["first_name"] = request.POST["first_name"]
        request.session["user_id"] = User.objects.get(email=request.POST["email1"]).id
        messages.success(request, "User successfully created")
    return redirect("/quotes")

def validate_login(request):
    errors = User.objects.basic_validatorLogin(request.POST)
    print(errors)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
            print("message are:", messages)
        return redirect("/")
    else:
        request.session["first_name"] = User.objects.get(email=request.POST["email2"]).first_name
        request.session["user_id"] = User.objects.get(email=request.POST["email2"]).id
        return redirect("/quotes")

def addquote(request):
    errors = Quote.objects.basic_validatorAddQuote(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
            print("message are:", messages)
        return redirect("/quotes")
    else:
        user = User.objects.get(id=request.session["user_id"])
        quote = Quote.objects.create(
            quote_text = request.POST["quoteText"],
            author = request.POST["author"],
            posted_by = user
        )
    return redirect("/quotes")

def userPage(request, id):
    user = User.objects.get(id=id)
    context = {
        "user" : user,
        "quotes" : user.quotes.all()
    }
    return render(request, "userPage.html", context)


def editMyaccountPage(request, id):
    user = User.objects.get(id=id)
    context = {
        "user" : user
    }
    return render(request, "myAccount.html", context)

def updateAccount(request):
    user = User.objects.get(id=request.session["user_id"])
    user_id = str(user.id)
    errors = Quote.objects.basic_validatorUpdateAccount(request.POST, user_id)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
            print("message are:", messages)
        return redirect("/myaccount/"+user_id)
    else:
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        request.session["first_name"] = first_name
        messages.success(request, "User successfully updated")
    return redirect("/myaccount/"+user_id)

def delete_quote(request, id):
    quote = Quote.objects.get(id=request.POST["quote_id"]).delete()
    return redirect("/quotes")

def like_quote(request, id):
    quote = Quote.objects.get(id=id)
    user = User.objects.get(id=request.session["user_id"])
    quote.liked_users.add(user)
    return redirect("/quotes")

def logout(request):
    request.session.clear()
    return redirect("/")