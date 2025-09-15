# Drobe Clothing Application

## Project Overview
Drobe is a modular e-commerce platform for clothing, built with Django MVC architecture. It supports user authentication, product catalog management, shopping cart, and order processing, with a scalable structure for future enhancements.

## Features
- **User Authentication & Profile Management**: Registration, login, password reset, profile editing, address management, order history, dashboard.
- **Product Catalog**: Category and brand management, product listing, filtering, search, product variants, reviews, admin product management.
- **Shopping Cart**: Add/update/remove items, persistent carts, discount codes, cart-to-checkout flow.
- **Order Processing**: Multi-step checkout, payment integration, order tracking, admin order management, email notifications.
- **Global Features**: Responsive navigation, static files, security, performance optimizations.

## Modular Apps
- `users`: Handles authentication, profile, addresses, preferences.
- `products`: Manages categories, brands, products, variants, images, reviews.
- `cart`: Shopping cart logic, discount codes, cart persistence.
- `orders`: Checkout, payment, shipping, order management.

## Database Relationships
- User ↔ Addresses, Preferences, Orders, Cart, Reviews, Saved Items
- Category ↔ Products, Subcategories
- Brand ↔ Products
- Product ↔ Images, Variants, Reviews
- Cart ↔ CartItems, Discounts
- Order ↔ OrderItems, Payment, Shipping, StatusHistory, Discounts


## Contributors

- **ABWOR TINA MARION**  
	Registration No: 2300704872  
	Student No: 23/U/04872/EVE

- **KAMPI GLORIA BULAMU**  
	Registration No: 2300700503  
	Student No: 23/U/0503

- **NTONDE EDGAR ISINGOMA**  
	Registration No: 2300724810  
	Student No: 23/U/24810/EVE

- **TWOMO ELVIS RODNEY**  
	Registration No: 2300701505  
	Student No: 23/U/1505


