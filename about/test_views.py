from django.test import TestCase
from django.urls import reverse
from datetime import datetime
from .models import About
from .forms import CollaborateForm

# Create your tests here.


class TestAboutViews(TestCase):

    def setUp(self):
        self.about = About(
            title="Primordia",
            updated_on=datetime.now(),
            content="Starting zone",
            profile_image="path/to/fake/tyrant.jpg",
        )
        self.about.save()

    def test_render_about_page_with_collaborate_form(self):
        response = self.client.get(reverse("about"))
        print(response.context)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Primordia", response.content)
        self.assertIsInstance(response.context["collaborate_form"], CollaborateForm)

    def test_successful_collaboration_submission(self):
        """
        Test for succesfull submission of collaboration request on about page.
        """
        collaborate_data = {
            "name": "Curtis",
            "email": "lol@gmail.com",
            "message": "This is a test comment.",
        }
        response = self.client.post(reverse("about"), collaborate_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"Collaboration request received! I endeavour to respond within 2 working days.",
            response.content,
        )
