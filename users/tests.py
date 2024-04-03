from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

class UserSignUpTests(TestCase):

    def setUp(self):
        self.username = 'newuser'
        self.password = 'testpass123'

    def test_signup_page_url(self):
        response = self.client.get("/users/signup/")
        self.assertEqual(response.status_code, 200)

    def test_signup_page_template(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_signup_form(self):
        response = self.client.post(reverse('signup'), data={
            'username': self.username,
            'password1': self.password,
            'password2': self.password,
        })

        # Check the user was created
        self.assertTrue(get_user_model().objects.filter(username=self.username).exists())
        
        # Verify redirect to the login page
        self.assertRedirects(response, reverse('login'))

    def test_signup_form_error(self):
        response = self.client.post(reverse('signup'), data={
            'username': 'testuser',
            'password1': 'testpass123',
            'password2': 'differentpass',
        })
        
        # Check the response context for form errors
        self.assertTrue(response.context['form'].errors)
        
        # Specifically check for password mismatch error
        self.assertTrue('password2' in response.context['form'].errors)
        self.assertIn("The two password fields didn’t match.", response.context['form'].errors['password2'])



class ProfilePageTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_profile_page_status_code(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_profile_page_template(self):
        response = self.client.get(reverse('profile'))
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_profile_page_contains_user_details(self):
        response = self.client.get(reverse('profile'))
        self.assertContains(response, 'testuser')


class ProfileUpdateTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', email='test@example.com', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_profile_update_page_status_code(self):
        response = self.client.get("/users/profile/edit/")
        self.assertEqual(response.status_code, 200)

    def test_profile_update(self):
        response = self.client.post("/users/profile/edit/", {'username': 'newusername', 'email': 'new@example.com'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')
        self.assertEqual(self.user.email, 'new@example.com')
