import pytest
import faker

pytestmark = pytest.mark.django_db

class TestProfileModel:
    def test_str_return(self, profile_factory, user_factory):
        # Create a user and profile using factories
        user = user_factory(username="mulin")
        profile = profile_factory(user=user)
        # Check if the __str__ method returns the expected string
        assert profile.__str__() == "mulin Profile."
        
    def test_imageurl_return(self, profile_factory, faker):
        # Generate a random image path using faker
        image_path = faker.image_url()
        # Create a profile with the generated image path
        profile_one = profile_factory(image=image_path)
        # Check if the imageurl property is not equal to the image path
        assert profile_one.imageurl != image_path
        
    def test_save_method(self, profile_factory, faker):
        # Generate a random image path using faker
        image = faker.image_url().replace("https://","")
        image = image.replace("/","") + ".jpg"
        # Create a profile with the generated image path
        profile = profile_factory(image=image)
        # Check if the image name property is not equal to the image path
        assert profile.image.name != image
        
class TestCustomerModel:
    def test_name_return(self, customer_factory):
        # Create a customer with specified first and last names
        customer = customer_factory(first_name="Sulaiman", last_name="Ashley")
        # Check if the name property returns the full name
        assert customer.name == "Sulaiman Ashley"
    
    def test_str_return(self, customer_factory):
        # Create a customer with specified first and last names
        customer = customer_factory(first_name="Sulaiman", last_name="Ashley")
        # Check if the __str__ method returns the full name
        assert customer.__str__() == "Sulaiman Ashley"
        
class TestBusinessModel:
    def test_str_return(self, business_factory, faker):
        # Generate a random company name using faker
        company = faker.company()
        # Create a business with the generated company name
        business = business_factory(business_name=company)
        # Check if the __str__ method returns the company name
        assert business.__str__() == company


