# Cycle E-Shop - My E-Shop for Cycles

A simple and elegant web-based e-shop application built with Python Flask for selling bicycles.

## Features

- 🚴 Browse a collection of cycles with different categories
- 🔍 View detailed product information
- 🛒 Shopping cart functionality
- ➕ Add/update/remove items from cart
- 💳 Checkout process (demo)
- 📱 Responsive design

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/ghoshdipanjan/myeshopforcicles.git
cd myeshopforcicles
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Browse the catalog, add items to your cart, and proceed through the checkout process.

## Project Structure

```
myeshopforcicles/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Home page
│   ├── product_detail.html  # Product detail page
│   ├── cart.html        # Shopping cart
│   └── checkout.html    # Checkout page
└── static/              # Static files
    └── css/
        └── style.css    # Stylesheet
```

## Features Overview

### Home Page
- Display all available cycles
- Show product images, names, categories, prices, and stock availability
- Quick access to product details

### Product Detail Page
- Detailed product information
- Add to cart with quantity selection
- Stock availability check

### Shopping Cart
- View all items in cart
- Update quantities
- Remove items
- See total price
- Proceed to checkout

### Checkout
- Enter billing information
- View order summary
- Place order (demo mode)

## Technologies Used

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3
- **Session Management**: Flask sessions for cart functionality

## Notes

- This is a demo application. Payment processing is simulated and no real transactions occur.
- Product data is stored in-memory and will reset when the server restarts.
- Debug mode is enabled by default for development. For production deployment, set `FLASK_DEBUG=False` environment variable.
- For production use, consider adding:
  - Database integration (SQLite, PostgreSQL, etc.)
  - User authentication
  - Real payment processing
  - Order history
  - Admin panel for product management
  - Set `SECRET_KEY` environment variable to a secure random value
  - Disable debug mode (`FLASK_DEBUG=False`)
  - Use a production WSGI server (Gunicorn, uWSGI, etc.)
  - Add HTTPS/SSL certificates
  - Implement proper error handling and logging

## License

This project is open source and available for educational purposes.