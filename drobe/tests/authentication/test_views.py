from django.urls import reverse
from django.test import Client
from pytest_django.asserts import assertTemplateUsed

client = Client()

def test_profile(client):
    # Test profile view redirects if user is not authenticated
    response = client.get(reverse('profile'))
    assert response.status_code == 302

def test_login_user(client):
    # Test login view returns status code 200 and correct template used
    response = client.get(reverse('login'))
    assert response.status_code == 200
    assertTemplateUsed(response, "authentication/login.html")
    
def test_signup_user(client):
    # Test signup view for user returns status code 200 and correct template used
    response = client.get(reverse('signup'))
    assert response.status_code == 200
    assertTemplateUsed(response, "authentication/signup-user.html")
    
def test_signup_business(client):
    # Test signup view for business returns status code 200 and correct template used
    response = client.get(reverse('signup-b'))
    assert response.status_code == 200
    assertTemplateUsed(response, "authentication/signup-business.html")

def test_logout_u(client):
    # Test logout view redirects
    response = client.get(reverse('logout'))
    assert response.status_code == 302
