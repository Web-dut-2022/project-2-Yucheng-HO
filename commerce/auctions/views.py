from itertools import chain
import string
from tracemalloc import is_tracing
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
import array as arr

from .models import User, Watch_list, auction_listings,bid_record,commits
from .forms import CreateForm


def index(request):

    # if request.user.is_authenticated:
    #     data = auction_listings.objects.exclude(uid = request.user.id)
    # else:
    #     data = auction_listings.objects.all()

    data = auction_listings.objects.filter(is_active = True)
    
    return render(request, "auctions/index.html", {
        "data":data,
        "title": "Active"
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url='/login')
def create_listing(request):
    if request.method == 'GET':
        form = CreateForm()
        return render(request, "auctions/create.html", {
            "form": form
        })
    else:
        name = request.POST['name']
        detail = request.POST['detail']
        imgURL = request.POST['imgURL']
        starting = request.POST['starting']
        user = User.objects.get(id = request.user.id)
        auction_listing = auction_listings(name=name,imgURL=imgURL, detail=detail,starting=starting, is_active = True)
        auction_listing.uid = user
        auction_listing.save()
        return redirect('/')



@login_required(login_url='/login')
def listings(request, auction_id):
    data = auction_listings.objects.filter(id = auction_id)
    return render (request, "auctions/detail.html", {
        "data": data[0]
    })


def addWatch(request, auction_id):
    aid = auction_listings.objects.get(id = auction_id)
    uid = User.objects.get(id = request.user.id)
    watched = Watch_list()
    watched.aid = aid
    watched.uid = uid
    watched.save()
    return redirect('/listings/'+str(auction_id)+'/')


# # python 如何迭代查询呢
def watchList(request):
    lists = Watch_list.objects.filter(uid = request.user.id)
    # print(lists[0].aid.name)
    # data = auction_listings.objects.filter(id = lists[0].aid)
    # for list in lists[1:]:
    #     data = chain(data,auction_listings.objects.filter(id = list.aid))

    return render(request, "auctions/watchlist.html", {
        "title": "Watched",
        "data": lists
    })
