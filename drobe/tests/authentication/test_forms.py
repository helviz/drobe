import pytest
from faker import Faker
from authentication.forms import *
from django.test import Client

# Instantiate Faker for generating fake data
fake = Faker()

# Marking all tests to use Django DB
pytestmark = pytest.mark.django_db

class TestUserLoginForm:
    
    client = Client()
    
    def test_valid_form(self):
        """Test if the user login form is valid with valid data."""
        form_data = {"username":"mulin", "password":"1234"}
        form = UserLoginForm(data=form_data)
        assert form.is_valid() == True
        
    def test_invalid_form(self):
        """Test if the user login form is invalid with missing username."""
        form_data = {"username":"", "password":"1234"}
        form = UserLoginForm(data=form_data)
        assert form.is_valid() == False
    
    def test_form_submission(self):
        """Test if the user login form submission redirects properly."""
        form_data = {"username":"mulin", "password":"1234"}
        response = self.client.post('/auth/login', data=form_data)
        assert response.status_code == 301

class TestCustomerRegistrationForm:
    
    client = Client()
    
    def test_valid_form(self):
        """Test if the customer registration form is valid with valid data."""
        password = fake.password()
        form_data = {"username":fake.user_name(), "first_name":fake.first_name(), "last_name": fake.last_name(), "email":fake.email(), "password1":password, "password2":password}
        form = CustomerRegisterForm(data=form_data)
        assert form.is_valid() == True
        
    def test_invalid_form(self):
        """Test if the customer registration form is invalid with missing email and last name."""
        form_data = {"email":"", "first_name":fake.first_name(), "last_name": ""}
        form = CustomerRegisterForm(data=form_data)
        assert form.is_valid() == False
    
    def test_form_submission(self):
        """Test if the customer registration form submission redirects properly."""
        form_data = {"username":fake.user_name(), "email":fake.email(), "first_name":fake.first_name(), "last_name": fake.last_name(), "password1":"1234", "password2":"1234"}
        response = self.client.post('/auth/signup-u', data=form_data)
        assert response.status_code == 301
        
class TestBusinessRegisterForm:
    
    client = Client()
    
    def test_form_valid(self):
        """Test if the business registration form is valid with valid data."""
        form_data = {"business_name":fake.company()}
        form = BusinessRegisterForm(data=form_data)
        assert form.is_valid() == True
        
    def test_form_invalid(self):
        """Test if the business registration form is invalid with missing business name."""
        form_data = {"business_name":""}
        form = BusinessRegisterForm(data=form_data)
        assert form.is_valid() == False
        
    def test_form_submission(self):
        """Test if the business registration form submission redirects properly."""
        password = fake.password()
        form_data_c = {"username":fake.user_name(), "first_name":fake.first_name(), "last_name": fake.last_name(), "email":fake.email(), "password1":password, "password2":password}
        form_data_b = {"business_name":fake.company()}
        response_1 = self.client.post('/auth/signup-b', data=form_data_c)
        response_2 = self.client.post('/auth/signup-b', data=form_data_b)
        assert response_1.status_code == 301
        assert response_2.status_code == 301
