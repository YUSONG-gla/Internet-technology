from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User

class TrackerViewTests(TestCase):
    def setUp(self):
        
        self.user = User.objects.create_user(username='testviewuser', password='testpassword123')

    def test_dashboard_view_unauthenticated_redirect(self):
        url = reverse('dashboard') 
        response = self.client.get(url)
        
       
        self.assertEqual(response.status_code, 302)

    def test_dashboard_view_authenticated_access(self):
        
        self.client.login(username='testviewuser', password='testpassword123')
        
       
        url = reverse('dashboard')
        response = self.client.get(url)
        
        
        self.assertEqual(response.status_code, 200)
        
