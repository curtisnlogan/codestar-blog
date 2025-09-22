from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import About
from .forms import CollaborateForm

# Create your views here.


def about(request):
    """
    Display About page content and handle collaboration requests.

    Retrieves the About instance from the database and renders
    it on the about page along with the collaboration form.
    Handles POST requests for collaboration form submission.

    **Context**

    ``about``
        The most recent instance of :model:`about.About`.
    ``collaborate_form``
        An instance of :model:`about.CollaborateRequest`

    **Template:**

    :template:`about/about.html`
    """

    about = get_object_or_404(About)

    if request.method == "POST":
        collaborate_form = CollaborateForm(data=request.POST)
        if collaborate_form.is_valid():
            collaborate_form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Collaboration request received! I endeavour to respond within 2 working days.",
            )
    collaborate_form = CollaborateForm()

    return render(
        request,
        "about/about.html",
        {"about": about, "collaborate_form": collaborate_form},
    )
