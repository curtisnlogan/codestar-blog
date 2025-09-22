from django.test import TestCase
from .forms import CollaborateForm


class TestCollaborateForm(TestCase):

    def test_form_is_valid(self):
        """Test for all fields"""
        form = CollaborateForm({"name": "Curtis", "email": "test@test.com", "message": "Hello!"})
        self.assertTrue(form.is_valid(), msg="Form is not valid")

    def test_form_is_invalid_name(self):
        """Test for name field"""
        form = CollaborateForm({"name": "", "email": "test@test.com", "message": "Hello!"})
        self.assertFalse(form.is_valid(), msg="Form is not valid")

    def test_form_is_invalid_email(self):
        """Test for email field"""
        form = CollaborateForm({"name": "Curtis", "email": "", "message": "Hello!"})
        self.assertFalse(form.is_valid(), msg="Form is not valid")

    def test_form_is_invalid_message(self):
        """Test for message field"""
        form = CollaborateForm({"name": "Curtis", "email": "test@test.com", "message": ""})
        self.assertFalse(form.is_valid(), msg="Form is not valid")
