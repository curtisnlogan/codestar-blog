from django.shortcuts import render, get_object_or_404
from .models import About
from .forms import CollaborateForm

# Create your views here.


def about(request):
    """
    Display the About page content.

    Retrieves the first About instance from the database and renders
    it on the about page.

    **Context**

    ``about``
        An instance of :model:`about.About`.

    **Template:**

    :template:`about/about.html`
    """

    about = get_object_or_404(About)
    collaborate = CollaborateForm()

    return render(
        request,
        "about/about.html",
        {"about": about, "collaborate_form": collaborate},
    )
