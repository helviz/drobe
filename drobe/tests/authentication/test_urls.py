from django.urls import resolve
from authentication.views import *

class TestUrls:
    def test_profile_url(self):
        url = resolve('/auth/profile/')
        assert url.func == profile
        assert url.view_name == 'profile'
        
    def test_login_url(self):
        url = resolve('/auth/login/')
        assert url.func == login_user
        assert url.view_name == 'login'
        
    def test_signup_user_url(self):
        url = resolve('/auth/signup-u/')
        assert url.func == signup_user
        assert url.view_name == 'signup'
        
    def test_signup_business_url(self):
        url = resolve('/auth/signup-b/')
        assert url.func == signup_business
        assert url.view_name == 'signup-b'
        
    def test_logout_url(self):
        url = resolve('/auth/logout/')
        assert url.func == logout_u
        assert url.view_name == 'logout'