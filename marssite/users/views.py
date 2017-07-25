from django.shortcuts import render


def index(request):

    return render(request, "users.html", {})

def admin(request):

    return render(request, "admin.html", {})
