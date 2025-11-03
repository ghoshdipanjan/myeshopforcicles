from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os

app = Flask(__name__)
# Use environment variable for secret key in production
# Generate a secure key with: python -c 'import secrets; print(secrets.token_hex())'
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Sample cycle data
CYCLES = [
    {
        'id': 1,
        'name': 'Mountain Explorer 3000',
        'category': 'Mountain Bike',
        'price': 599.99,
        'description': 'High-performance mountain bike with 21-speed gears and front suspension.',
        'image': 'mountain-bike.jpg',
        'stock': 15
    },
    {
        'id': 2,
        'name': 'City Cruiser Pro',
        'category': 'City Bike',
        'price': 399.99,
        'description': 'Comfortable city bike perfect for daily commutes and leisure rides.',
        'image': 'city-bike.jpg',
        'stock': 20
    },
    {
        'id': 3,
        'name': 'Road Racer Elite',
        'category': 'Road Bike',
        'price': 899.99,
        'description': 'Lightweight carbon frame road bike designed for speed and endurance.',
        'image': 'road-bike.jpg',
        'stock': 10
    },
    {
        'id': 4,
        'name': 'Kids Adventure 200',
        'category': 'Kids Bike',
        'price': 199.99,
        'description': 'Safe and fun bike for children aged 6-10 with training wheels included.',
        'image': 'kids-bike.jpg',
        'stock': 25
    },
    {
        'id': 5,
        'name': 'Electric Commuter',
        'category': 'E-Bike',
        'price': 1499.99,
        'description': 'Electric bike with 50-mile range, perfect for eco-friendly commuting.',
        'image': 'electric-bike.jpg',
        'stock': 8
    },
    {
        'id': 6,
        'name': 'Folding Compact 150',
        'category': 'Folding Bike',
        'price': 299.99,
        'description': 'Compact folding bike ideal for storage and multi-modal transport.',
        'image': 'folding-bike.jpg',
        'stock': 12
    }
]

def get_cart():
    """Get cart from session"""
    if 'cart' not in session:
        session['cart'] = []
    return session['cart']

def get_cart_total():
    """Calculate total price of items in cart"""
    cart = get_cart()
    total = 0
    for item in cart:
        cycle = next((c for c in CYCLES if c['id'] == item['id']), None)
        if cycle:
            total += cycle['price'] * item['quantity']
    return total

def get_cart_count():
    """Get total number of items in cart"""
    cart = get_cart()
    return sum(item['quantity'] for item in cart)

@app.route('/')
def index():
    """Home page with all cycles"""
    cart_count = get_cart_count()
    return render_template('index.html', cycles=CYCLES, cart_count=cart_count)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Product detail page"""
    cycle = next((c for c in CYCLES if c['id'] == product_id), None)
    if not cycle:
        flash('Product not found!', 'error')
        return redirect(url_for('index'))
    
    cart_count = get_cart_count()
    return render_template('product_detail.html', cycle=cycle, cart_count=cart_count)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    """Add item to cart"""
    cycle = next((c for c in CYCLES if c['id'] == product_id), None)
    if not cycle:
        flash('Product not found!', 'error')
        return redirect(url_for('index'))
    
    quantity = int(request.form.get('quantity', 1))
    
    if quantity > cycle['stock']:
        flash(f'Sorry, only {cycle["stock"]} items available in stock.', 'error')
        return redirect(url_for('product_detail', product_id=product_id))
    
    cart = get_cart()
    
    # Check if item already in cart
    existing_item = next((item for item in cart if item['id'] == product_id), None)
    if existing_item:
        new_quantity = existing_item['quantity'] + quantity
        if new_quantity > cycle['stock']:
            flash(f'Sorry, only {cycle["stock"]} items available in stock.', 'error')
            return redirect(url_for('product_detail', product_id=product_id))
        existing_item['quantity'] = new_quantity
    else:
        cart.append({'id': product_id, 'quantity': quantity})
    
    session['cart'] = cart
    flash(f'{cycle["name"]} added to cart!', 'success')
    return redirect(url_for('index'))

@app.route('/cart')
def view_cart():
    """View shopping cart"""
    cart = get_cart()
    cart_items = []
    
    for item in cart:
        cycle = next((c for c in CYCLES if c['id'] == item['id']), None)
        if cycle:
            cart_items.append({
                'cycle': cycle,
                'quantity': item['quantity'],
                'subtotal': cycle['price'] * item['quantity']
            })
    
    total = get_cart_total()
    cart_count = get_cart_count()
    
    return render_template('cart.html', cart_items=cart_items, total=total, cart_count=cart_count)

@app.route('/update_cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    """Update item quantity in cart"""
    quantity = int(request.form.get('quantity', 0))
    cycle = next((c for c in CYCLES if c['id'] == product_id), None)
    
    if not cycle:
        flash('Product not found!', 'error')
        return redirect(url_for('view_cart'))
    
    cart = get_cart()
    item = next((item for item in cart if item['id'] == product_id), None)
    
    if item:
        if quantity <= 0:
            cart.remove(item)
            flash(f'{cycle["name"]} removed from cart!', 'success')
        elif quantity > cycle['stock']:
            flash(f'Sorry, only {cycle["stock"]} items available in stock.', 'error')
        else:
            item['quantity'] = quantity
            flash('Cart updated!', 'success')
    
    session['cart'] = cart
    return redirect(url_for('view_cart'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    """Remove item from cart"""
    cart = get_cart()
    cart = [item for item in cart if item['id'] != product_id]
    session['cart'] = cart
    flash('Item removed from cart!', 'success')
    return redirect(url_for('view_cart'))

@app.route('/checkout')
def checkout():
    """Checkout page"""
    cart = get_cart()
    if not cart:
        flash('Your cart is empty!', 'error')
        return redirect(url_for('index'))
    
    cart_items = []
    for item in cart:
        cycle = next((c for c in CYCLES if c['id'] == item['id']), None)
        if cycle:
            cart_items.append({
                'cycle': cycle,
                'quantity': item['quantity'],
                'subtotal': cycle['price'] * item['quantity']
            })
    
    total = get_cart_total()
    cart_count = get_cart_count()
    
    return render_template('checkout.html', cart_items=cart_items, total=total, cart_count=cart_count)

@app.route('/place_order', methods=['POST'])
def place_order():
    """Process order"""
    cart = get_cart()
    if not cart:
        flash('Your cart is empty!', 'error')
        return redirect(url_for('index'))
    
    # In a real application, you would:
    # - Validate customer information
    # - Process payment
    # - Update inventory
    # - Send confirmation email
    # - Save order to database
    
    # Clear cart
    session['cart'] = []
    flash('Order placed successfully! Thank you for your purchase.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Debug mode is enabled for development/demo purposes
    # In production, set DEBUG=False or use environment variable
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() in ('true', '1', 'yes')
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
