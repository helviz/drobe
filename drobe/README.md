# SHOPPIE

## Functional Specification

### Overview

This web platform aims to connect customers to basic necessities and needs all at their convenience through services like online ordering, delivery or booking services.

### User Roles

1. _Guest User:_
    - Can browse products.
    - Can register or log in.
2. _- Registered User(Customer):_
    - Inherits guest user privileges.
    - Can add/remove products to/from the shopping cart.
    - Can place orders.
3. _Registered User(Business):_
    - Inherits guest user privileges and registered user privileges for a customer.
    - Can setup, manage, and maintain online stores on the web platform.
4. _Admin User:_
    - Inherits registered user privileges.
    - Can add/update/remove products and also online stores
    - Can manage user accounts and orders

### Features

1. _Product Catalog:_
   - Display products with details.
   - Filter and search functionality.
2. _User Authentication:_
   - Registration and login.
   - Password reset functionality.
3. _Shopping Cart:_
   - Add/remove products.
   - Adjust quantities.
   - Calculate total price.
   - Rate products.
4. _Order Processing:_
   - Confirm order details.
   - Payment integration (Paypal).
   - Order confirmation and tracking.
5. _Admin Panel:_
   - Manage products.
   - View and process orders.
   - User management.

## Technological Specification

1.  _Backend:_
    - Django
    - Django REST Framework for APIs.
2.  _Frontend:_
    - HTML, CSS, JavaScript.
3.  _Database:_
    - MySQL for data storage
    - Authentication:
    - Django's built-in authentication system.
4.  _Misc:_
    - Payment Integration: Paypal
    - Email API like Sendgrid, Mailgun for email related tasks

## Development Methodology:

        - Pair Programming: This involves collaboration on gitlab so as to ease tasks and ensure agile development and high quality code.
        - Testing the platform: User acceptance testing to ensure platform functionality and stability.

## Evaluation Criteria:

        - Ease of use of the platform
        - Technical Implementation
        - Deployment and Scalability
        - Functionality
