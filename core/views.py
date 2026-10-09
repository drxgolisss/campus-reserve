from django.shortcuts import render


def home(request):
    """Render the public project introduction page."""
    return render(request, "core/home.html")
