import os
import json
import csv
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from PIL import Image
import io
import base64
from google import genai
import os as os_env
from os import path as os_path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'iot-verse-secret-key-2024-mintfire'
app.config['UPLOAD_FOLDER'] = 'uploads/product_images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Session configuration for automatic timeout
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # 30 minutes
app.config['SESSION_REFRESH_EACH_REQUEST'] = True  # Refresh session on each request
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to session cookie
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection

# Ensure directories exist
os.makedirs('data', exist_ok=True)
os.makedirs('uploads/product_images', exist_ok=True)
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)
os.makedirs('static/images', exist_ok=True)

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

# Session timeout handler
@app.before_request
def before_request():
    """Make session permanent and check for session timeout"""
    from flask import session
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)

# Handle session timeout
@login_manager.unauthorized_handler
def unauthorized():
    """Handle unauthorized access with session timeout message"""
    flash('Your session has expired. Please log in again.', 'warning')
    return redirect(url_for('admin_login'))

# Context processor to make config available to all templates
@app.context_processor
def inject_config():
    """Make config available to all templates"""
    return {'config': load_volta_config()}

# Context processor for currency data
@app.context_processor
def inject_currencies():
    """Make currencies and symbols available to all templates"""
    return {
        'currencies': list(EXCHANGE_RATES.keys()),
        'symbols': CURRENCY_SYMBOLS
    }

# User class for admin
class AdminUser(UserMixin):
    def __init__(self, id, email):
        self.id = id
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    admin_data = load_admin_data()
    if admin_data.get('email') == user_id:
        return AdminUser(user_id, user_id)
    return None

# Helper functions
def load_admin_data():
    try:
        with open('data/admin_password.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Create default admin
        default_admin = {
            "email": "admin@iotverse.com",
            "password": bcrypt.generate_password_hash("admin123").decode('utf-8')
        }
        save_admin_data(default_admin)
        return default_admin

def save_admin_data(data):
    with open('data/admin_password.json', 'w') as f:
        json.dump(data, f, indent=4)

def load_products():
    try:
        with open('data/products.json', 'r') as f:
            products = json.load(f)
            # Ensure all products have required fields
            for idx, product in enumerate(products):
                if 'type' not in product:
                    product['type'] = ''
                if 'created_at' not in product:
                    product['created_at'] = datetime.now().isoformat()
                if 'last_updated' not in product:
                    product['last_updated'] = datetime.now().isoformat()
                if 'index' not in product:
                    product['index'] = idx
            return products
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_products(products):
    with open('data/products.json', 'w') as f:
        json.dump(products, f, indent=4, default=str)

def load_price_history():
    try:
        with open('data/price_history.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_price_history(history):
    with open('data/price_history.json', 'w') as f:
        json.dump(history, f, indent=4, default=str)

def clear_price_history_all():
    """Clear all price history for all products"""
    price_history = load_price_history()
    # Clear all entries but keep the keys to maintain structure
    for product_id in price_history:
        price_history[product_id] = []
    save_price_history(price_history)
    return True

def clear_price_history_individual(product_id):
    """Clear price history for a specific product"""
    price_history = load_price_history()
    if product_id in price_history:
        price_history[product_id] = []
        save_price_history(price_history)
        return True
    return False

def record_daily_price(products):
    """Automatically record today's price as history for each product"""
    price_history = load_price_history()
    today = datetime.now().strftime('%Y-%m-%d')
    
    for product in products:
        product_id = product['id']
        current_price = product['price']
        
        # Initialize if not exists
        if product_id not in price_history:
            price_history[product_id] = []
        
        # Check if price already recorded for today
        today_recorded = False
        if price_history[product_id]:
            last_entry = price_history[product_id][-1]
            last_date = last_entry.get('date', '')[:10]  # Get YYYY-MM-DD
            if last_date == today:
                today_recorded = True
        
        # If not recorded for today, record current price
        if not today_recorded:
            price_history[product_id].append({
                'date': datetime.now().isoformat(),
                'price': current_price
            })
            
            # Keep last 365 days of history (1 year)
            if len(price_history[product_id]) > 365:
                price_history[product_id] = price_history[product_id][-365:]
    
    save_price_history(price_history)

# Currency exchange rates (INR as base)
EXCHANGE_RATES = {
    'INR': 1.0,
    'USD': 0.012,      # 1 INR = 0.012 USD
    'EUR': 0.011,      # 1 INR = 0.011 EUR
    'GBP': 0.0095,     # 1 INR = 0.0095 GBP
    'JPY': 1.73,       # 1 INR = 1.73 JPY
    'AUD': 0.019,      # 1 INR = 0.019 AUD
    'CAD': 0.017,      # 1 INR = 0.017 CAD
    'SGD': 0.016,      # 1 INR = 0.016 SGD
    'HKD': 0.094,      # 1 INR = 0.094 HKD
    'NZD': 0.021,      # 1 INR = 0.021 NZD
    'CHF': 0.011,      # 1 INR = 0.011 CHF
}

CURRENCY_SYMBOLS = {
    'INR': '₹',
    'USD': '$',
    'EUR': '€',
    'GBP': '£',
    'JPY': '¥',
    'AUD': 'A$',
    'CAD': 'C$',
    'SGD': 'S$',
    'HKD': 'HK$',
    'NZD': 'NZ$',
    'CHF': 'Fr',
}

def convert_price(amount_inr, target_currency='INR'):
    """Convert price from INR to target currency"""
    if target_currency not in EXCHANGE_RATES:
        target_currency = 'INR'
    return round(amount_inr * EXCHANGE_RATES[target_currency], 2)

def get_currency_symbol(currency='INR'):
    """Get currency symbol"""
    return CURRENCY_SYMBOLS.get(currency, currency)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Volta Chatbot Configuration Functions
def load_volta_config():
    """Load Volta chatbot configuration"""
    try:
        with open('data/volta_config.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Create default config
        default_config = {
            'enabled': False,  # Disabled by default until admin enables it
            'version': '2.1.0.0',  # Default version
            'maintenance_mode': False,
            'system_prompt': """You are Volta, an intelligent IoT assistant specialized in IoT devices, Internet of Things, 
Artificial Intelligence (AI), Machine Learning (ML), Cyber Security, and Computer Science Engineering (CSE) topics.

Your role is to:
1. Provide accurate information about IoT devices, protocols, and architectures
2. Explain AI/ML concepts, algorithms, and applications
3. Discuss Cyber Security principles, threats, and mitigation strategies
4. Cover CSE fundamentals and advanced topics
5. Answer technical questions related to these domains
6. Provide guidance on implementations and best practices

Important: Only respond to questions related to IoT, AI/ML, Cyber Security, and CSE. 
For questions outside these domains, politely decline and redirect the conversation to these topics.
Keep responses concise, technical, and helpful.
Always provide relevant examples when possible."""
        }
        save_volta_config(default_config)
        return default_config

def save_volta_config(config):
    """Save Volta chatbot configuration"""
    with open('data/volta_config.json', 'w') as f:
        json.dump(config, f, indent=4)

def get_volta_api_key():
    """Get Volta API key from .env file or config"""
    from dotenv import load_dotenv
    load_dotenv()
    
    # First check environment variable
    env_key = os_env.getenv('GEMINI_API_KEY', '').strip()
    if env_key:
        return env_key
    
    # Then check if saved in volta config
    try:
        config = load_volta_config()
        if config.get('api_key'):
            return config['api_key'].strip()
    except:
        pass
    
    return ''

def save_api_key_to_config(api_key):
    """Save API key to volta config"""
    config = load_volta_config()
    config['api_key'] = api_key.strip()
    save_volta_config(config)
    
    # Also update .env file for persistence
    try:
        env_path = '.env'
        if os_path.exists(env_path):
            with open(env_path, 'r') as f:
                lines = f.readlines()
            
            updated = False
            new_lines = []
            for line in lines:
                if line.startswith('GEMINI_API_KEY='):
                    new_lines.append(f'GEMINI_API_KEY={api_key.strip()}\n')
                    updated = True
                else:
                    new_lines.append(line)
            
            if not updated:
                new_lines.append(f'GEMINI_API_KEY={api_key.strip()}\n')
            
            with open(env_path, 'w') as f:
                f.writelines(new_lines)
        else:
            with open(env_path, 'w') as f:
                f.write(f'GEMINI_API_KEY={api_key.strip()}\n')
    except Exception as e:
        print(f"Error updating .env file: {e}")
    
    # Reload environment
    from dotenv import load_dotenv
    load_dotenv()

def process_csv_file(filepath):
    """Convert your specific CSV format to JSON and update price history"""
    try:
        # Read CSV with proper encoding
        df = pd.read_csv(filepath, encoding='utf-8')
        
        print(f"CSV Columns: {df.columns.tolist()}")
        print(f"CSV Shape: {df.shape}")
        
        # Clean column names (strip whitespace)
        df.columns = df.columns.str.strip()
        
        # Rename columns to match our system
        column_mapping = {
            'IoT Name': 'name',
            'Price (INR)': 'price',
            'Quantity': 'quantity',
            'Availability': 'availability',
            'Type': 'type',
            'Description': 'description'
        }
        
        # Rename columns that exist in the CSV
        for old_col, new_col in column_mapping.items():
            if old_col in df.columns:
                df.rename(columns={old_col: new_col}, inplace=True)
        
        # Ensure required columns exist
        required_columns = ['name', 'price', 'quantity', 'availability', 'description']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing required column after mapping: {col}")
        
        # Clean the data
        df = df.dropna(subset=['name'])  # Remove rows without name
        df['name'] = df['name'].astype(str).str.strip()
        df['description'] = df['description'].astype(str).str.strip()
        
        # Convert TRUE/FALSE to In Stock/Out of Stock
        def convert_availability(val):
            if isinstance(val, bool):
                return 'In Stock' if val else 'Out of Stock'
            elif isinstance(val, str):
                val = val.strip().upper()
                if val == 'TRUE':
                    return 'In Stock'
                elif val == 'FALSE':
                    return 'Out of Stock'
                else:
                    return val
            else:
                return 'Out of Stock'
        
        df['availability'] = df['availability'].apply(convert_availability)
        
        # Convert price to float (remove any non-numeric characters)
        def clean_price(price):
            if isinstance(price, (int, float)):
                return float(price)
            elif isinstance(price, str):
                # Remove INR, ₹ symbols and commas
                price = price.replace('INR', '').replace('₹', '').replace(',', '').strip()
                try:
                    return float(price)
                except:
                    return 0.0
            else:
                return 0.0
        
        df['price'] = df['price'].apply(clean_price)
        
        # Convert quantity to int
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0).astype(int)
        
        products = load_products()
        price_history = load_price_history()
        
        existing_products = {p['name']: p for p in products}
        updated_count = 0
        created_count = 0
        
        for _, row in df.iterrows():
            product_name = str(row['name']).strip()
            if not product_name or product_name.lower() in ['nan', '']:
                continue
                
            # Check if product exists
            if product_name in existing_products:
                product = existing_products[product_name]
                old_price = product['price']
                new_price = float(row['price'])
                
                # Update product
                product.update({
                    'name': product_name,
                    'price': new_price,
                    'quantity': int(row['quantity']),
                    'availability': row['availability'],
                    'description': row['description'],
                    'type': row.get('type', ''),
                    'last_updated': datetime.now().isoformat()
                })
                
                # Update price history if price changed
                if old_price != new_price:
                    if product['id'] not in price_history:
                        price_history[product['id']] = []
                    
                    price_history[product['id']].append({
                        'date': datetime.now().isoformat(),
                        'price': old_price
                    })
                    
                    # Keep only last 20 price entries
                    if len(price_history[product['id']]) > 20:
                        price_history[product['id']] = price_history[product['id']][-20:]
                
                updated_count += 1
            else:
                # Create new product
                new_product = {
                    'id': str(uuid.uuid4()),
                    'name': product_name,
                    'price': float(row['price']),
                    'quantity': int(row['quantity']),
                    'availability': row['availability'],
                    'type': row.get('type', ''),
                    'description': row['description'],
                    'image': 'default.jpg',
                    'index': len(products),  # Add index for new products
                    'created_at': datetime.now().isoformat(),
                    'last_updated': datetime.now().isoformat()
                }
                products.append(new_product)
                
                # Initialize price history
                price_history[new_product['id']] = [{
                    'date': datetime.now().isoformat(),
                    'price': float(row['price'])
                }]
                
                created_count += 1
        
        save_products(products)
        save_price_history(price_history)
        
        message = f"CSV processed successfully. Created: {created_count}, Updated: {updated_count}"
        return True, message
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error processing CSV: {str(e)}")
        print(f"Error details: {error_details}")
        return False, f"Error processing CSV: {str(e)}"

def generate_price_graph(product_id):
    """Generate price history graph for a product"""
    price_history = load_price_history()
    
    if product_id not in price_history or len(price_history[product_id]) == 0:
        return None
    
    history = price_history[product_id]
    dates = []
    prices = []
    
    # Extract dates and prices from history
    for h in history:
        try:
            date_str = h['date'][:10]  # Get YYYY-MM-DD
            dates.append(date_str)
            prices.append(float(h['price']))
        except:
            continue
    
    # Add current price with today's date
    products = load_products()
    current_product = next((p for p in products if p['id'] == product_id), None)
    if current_product:
        current_date = datetime.now().strftime('%Y-%m-%d')
        # Only add current price if it's different from last date or if we need more data
        if not dates or dates[-1] != current_date:
            dates.append(current_date)
            prices.append(float(current_product['price']))
    
    # Need at least 2 points to draw a meaningful graph
    if len(dates) < 2:
        return None
    
    # Create figure with better size and formatting
    plt.figure(figsize=(12, 6))
    
    # Plot the line
    plt.plot(dates, prices, marker='o', linewidth=2.5, markersize=8, 
             color='#2563eb', markerfacecolor='#1e40af', markeredgewidth=2, markeredgecolor='#2563eb')
    
    # Fill area under the curve
    plt.fill_between(range(len(dates)), prices, alpha=0.2, color='#2563eb')
    
    # Formatting
    plt.title('Price History (INR)', fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('Date', fontsize=13, fontweight='bold')
    plt.ylabel('Price (₹)', fontsize=13, fontweight='bold')
    
    # Format y-axis to show prices with decimal values
    ax = plt.gca()
    def format_price(x, p):
        if x == int(x):
            return f'₹{int(x):,}'
        else:
            return f'₹{x:,.2f}'
    ax.yaxis.set_major_formatter(plt.FuncFormatter(format_price))
    
    # Rotate x-axis labels
    plt.xticks(rotation=45, ha='right')
    
    # Add grid
    plt.grid(True, alpha=0.3, linestyle='--', linewidth=0.7)
    
    # Add value labels on each point - show decimal values properly
    for i, (date, price) in enumerate(zip(dates, prices)):
        # Format price with decimals if needed
        if price == int(price):
            price_label = f'₹{int(price):,}'
        else:
            price_label = f'₹{price:,.2f}'
        
        ax.text(i, price, price_label, ha='center', va='bottom', fontsize=10, fontweight='bold', color='#1e40af')
    
    # Set y-axis to start from a reasonable minimum
    min_price = min(prices)
    max_price = max(prices)
    price_range = max_price - min_price
    if price_range > 0:
        padding = price_range * 0.15
    else:
        padding = max_price * 0.15 if max_price > 0 else 100
    plt.ylim(max(0, min_price - padding), max_price + padding)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save to bytes
    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png', dpi=100, facecolor='white', bbox_inches='tight')
    plt.close()
    img_bytes.seek(0)
    
    # Encode to base64
    img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"

# Routes
@app.route('/')
def home():
    products = load_products()
    # Record daily prices for all products
    record_daily_price(products)
    # Group by type for filtering
    types = sorted(list(set(p.get('type', '') for p in products if p.get('type'))))
    # Calculate total inventory value
    total_value = sum(p['price'] * p['quantity'] for p in products)
    return render_template('home.html', products=products, types=types, total_value=total_value)

@app.route('/product/<product_id>')
def product_detail(product_id):
    products = load_products()
    product = next((p for p in products if p['id'] == product_id), None)
    
    if not product:
        flash('Product not found', 'error')
        return redirect(url_for('home'))
    
    # Record daily price for this product
    record_daily_price([product])
    
    # Generate price graph
    price_graph = generate_price_graph(product_id)
    
    # Load price history
    price_history = load_price_history()
    product_history = price_history.get(product_id, [])
    
    # Calculate average price from history
    if product_history:
        average_price = sum(h['price'] for h in product_history) / len(product_history)
    else:
        average_price = product['price']
    
    return render_template('product_detail.html', 
                         product=product, 
                         price_graph=price_graph,
                         price_history=product_history,
                         average_price=average_price)

@app.route('/search')
def search():
    query = request.args.get('q', '').lower().strip()
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    availability = request.args.get('availability')
    device_type = request.args.get('type')
    
    products = load_products()
    types = sorted(list(set(p.get('type', '') for p in products if p.get('type'))))
    
    # Apply filters
    filtered_products = products
    
    # Enhanced search with word matching
    if query:
        query_words = [w.strip() for w in query.split() if w.strip()]
        filtered_by_search = []
        
        for p in filtered_products:
            name_lower = p['name'].lower()
            desc_lower = p['description'].lower()
            type_lower = p.get('type', '').lower()
            
            # Combine all searchable fields
            searchable = f"{name_lower} {desc_lower} {type_lower}"
            
            # Check if any query word matches
            match_score = 0
            for qword in query_words:
                # Exact word match (highest priority)
                if qword in [w.strip('.,!?;:') for w in searchable.split()]:
                    match_score += 3
                # Word beginning match
                elif any(w.startswith(qword) for w in searchable.split()):
                    match_score += 2
                # Substring match
                elif qword in searchable:
                    match_score += 1
            
            if match_score > 0:
                filtered_by_search.append((p, match_score))
        
        # Sort by match score (highest first)
        filtered_by_search.sort(key=lambda x: x[1], reverse=True)
        filtered_products = [p for p, _ in filtered_by_search]
    
    if min_price is not None:
        filtered_products = [p for p in filtered_products if p['price'] >= min_price]
    
    if max_price is not None:
        filtered_products = [p for p in filtered_products if p['price'] <= max_price]
    
    if availability and availability != 'all':
        filtered_products = [p for p in filtered_products if p['availability'] == availability]
    
    if device_type and device_type != 'all':
        filtered_products = [p for p in filtered_products if p.get('type') == device_type]
    
    # Calculate total inventory value for filtered products
    total_value = sum(p['price'] * p['quantity'] for p in filtered_products)
    
    return render_template('home.html', products=filtered_products, search_query=query, types=types, total_value=total_value)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        admin_data = load_admin_data()
        
        if email == admin_data['email'] and bcrypt.check_password_hash(admin_data['password'], password):
            user = AdminUser(email, email)
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('home'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    products = load_products()
    # Record daily prices for all products
    record_daily_price(products)
    config = load_volta_config()
    stats = {
        'total_products': len(products),
        'in_stock': sum(1 for p in products if p['availability'] == 'In Stock'),
        'out_of_stock': sum(1 for p in products if p['availability'] == 'Out of Stock'),
        'low_stock': sum(1 for p in products if p['quantity'] < 5 and p['quantity'] > 0),
        'total_value': sum(p['price'] * p['quantity'] for p in products),
        'unique_types': len(set(p.get('type', '') for p in products if p.get('type')))
    }
    return render_template('admin_dashboard.html', stats=stats, config=config)

@app.route('/admin/products')
@login_required
def admin_products():
    products = load_products()
    # Record daily prices for all products
    record_daily_price(products)
    return render_template('admin_products.html', products=products)

@app.route('/admin/product/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        products = load_products()
        price_history = load_price_history()
        
        new_product = {
            'id': str(uuid.uuid4()),
            'name': request.form.get('name'),
            'price': float(request.form.get('price', 0)),
            'quantity': int(request.form.get('quantity', 0)),
            'availability': request.form.get('availability'),
            'type': request.form.get('type', ''),
            'description': request.form.get('description'),
            'image': 'default.jpg',
            'index': len(products),  # Add index as the last position
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }
        
        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(f"{new_product['id']}_{file.filename}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                new_product['image'] = filename
        
        products.append(new_product)
        save_products(products)
        
        # Initialize price history
        price_history[new_product['id']] = [{
            'date': datetime.now().isoformat(),
            'price': new_product['price']
        }]
        save_price_history(price_history)
        
        flash('Product added successfully!', 'success')
        return redirect(url_for('admin_products'))
    
    return render_template('add_product.html')

@app.route('/admin/product/edit/<product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    products = load_products()
    product = next((p for p in products if p['id'] == product_id), None)
    price_history = load_price_history()
    
    if not product:
        flash('Product not found', 'error')
        return redirect(url_for('admin_products'))
    
    if request.method == 'POST':
        old_price = product['price']
        new_price = float(request.form.get('price', 0))
        
        # Update product
        product.update({
            'name': request.form.get('name'),
            'price': new_price,
            'quantity': int(request.form.get('quantity', 0)),
            'availability': request.form.get('availability'),
            'type': request.form.get('type', ''),
            'description': request.form.get('description'),
            'last_updated': datetime.now().isoformat()
        })
        
        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(f"{product_id}_{file.filename}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                product['image'] = filename
        
        # Update price history if price changed
        if old_price != new_price:
            if product_id not in price_history:
                price_history[product_id] = []
            
            price_history[product_id].append({
                'date': datetime.now().isoformat(),
                'price': old_price
            })
            
            # Keep only last 20 price entries
            if len(price_history[product_id]) > 20:
                price_history[product_id] = price_history[product_id][-20:]
            
            save_price_history(price_history)
        
        save_products(products)
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin_products'))
    
    return render_template('edit_product.html', product=product)

@app.route('/admin/product/delete/<product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    products = load_products()
    price_history = load_price_history()
    
    # Remove product
    products = [p for p in products if p['id'] != product_id]
    save_products(products)
    
    # Remove price history
    if product_id in price_history:
        del price_history[product_id]
        save_price_history(price_history)
    
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('admin_products'))

@app.route('/admin/upload_csv', methods=['POST'])
@login_required
def upload_csv():
    if 'csv_file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('admin_dashboard'))
    
    file = request.files['csv_file']
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('admin_dashboard'))
    
    if not file.filename.endswith('.csv'):
        flash('Please upload a CSV file', 'error')
        return redirect(url_for('admin_dashboard'))
    
    # Save the file temporarily
    filename = secure_filename(f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    filepath = os.path.join('uploads', filename)
    file.save(filepath)
    
    # Process the CSV
    success, message = process_csv_file(filepath)
    
    if success:
        flash(message, 'success')
    else:
        flash(f'Error processing CSV: {message}', 'error')
    
    # Clean up
    if os.path.exists(filepath):
        os.remove(filepath)
    
    return redirect(url_for('admin_dashboard'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/api/products')
def api_products():
    products = load_products()
    return jsonify(products)

@app.route('/api/product/<product_id>')
def api_product_detail(product_id):
    products = load_products()
    product = next((p for p in products if p['id'] == product_id), None)
    
    if product:
        price_history = load_price_history()
        product['price_history'] = price_history.get(product_id, [])
        return jsonify(product)
    
    return jsonify({'error': 'Product not found'}), 404

@app.route('/api/stats')
@login_required
def api_stats():
    products = load_products()
    stats = {
        'total_products': len(products),
        'in_stock': sum(1 for p in products if p['availability'] == 'In Stock'),
        'out_of_stock': sum(1 for p in products if p['availability'] == 'Out of Stock'),
        'low_stock': sum(1 for p in products if p['quantity'] < 5 and p['quantity'] > 0),
        'total_value': sum(p['price'] * p['quantity'] for p in products),
        'average_price': sum(p['price'] for p in products) / len(products) if products else 0,
        'total_quantity': sum(p['quantity'] for p in products)
    }
    return jsonify(stats)

@app.route('/api/convert-currency', methods=['POST'])
def convert_currency_api():
    """API endpoint to convert currency"""
    data = request.get_json()
    amount = float(data.get('amount', 0))
    target_currency = data.get('currency', 'INR')
    
    converted = convert_price(amount, target_currency)
    symbol = get_currency_symbol(target_currency)
    
    return jsonify({
        'original_amount': amount,
        'original_currency': 'INR',
        'converted_amount': converted,
        'target_currency': target_currency,
        'symbol': symbol
    })

@app.route('/api/currencies')
def get_currencies():
    """Get list of available currencies"""
    return jsonify({
        'currencies': list(EXCHANGE_RATES.keys()),
        'symbols': CURRENCY_SYMBOLS,
        'rates': EXCHANGE_RATES
    })

@app.route('/api/products/reorder', methods=['POST'])
@login_required
def reorder_products():
    """Reorder products by updating their index field"""
    try:
        data = request.get_json()
        product_order = data.get('order', [])
        
        if not product_order:
            return jsonify({'error': 'No product order provided'}), 400
        
        products = load_products()
        
        # Create a mapping of product ID to product
        product_map = {p['id']: p for p in products}
        
        # Update the index for each product in the new order
        for new_index, product_id in enumerate(product_order):
            if product_id in product_map:
                product_map[product_id]['index'] = new_index
        
        # Reconstruct products list in the new order
        products = [product_map[pid] for pid in product_order if pid in product_map]
        
        # Save the updated products
        save_products(products)
        
        return jsonify({'success': True, 'message': 'Products reordered successfully'})
    except Exception as e:
        print(f"Error reordering products: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/chat')
def chat():
    """Volta chatbot interface - PUBLIC"""
    config = load_volta_config()
    return render_template('volta_chat.html', chatbot_enabled=config['enabled'])

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """API endpoint for Volta chatbot - PUBLIC"""
    try:
        config = load_volta_config()
        
        # Check if chatbot is enabled
        if not config['enabled']:
            return jsonify({
                'success': False,
                'error': 'Volta is sleeping. The chatbot is currently in maintenance mode.',
                'status': 'maintenance'
            }), 503
        
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get API key from .env file
        api_key = get_volta_api_key()
        if not api_key:
            return jsonify({
                'success': False,
                'error': 'Volta is sleeping. API key not configured in environment.',
                'status': 'maintenance'
            }), 503
        
        # Initialize Gemini client
        client = genai.Client(api_key=api_key)
        
        # Send request to Gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {"text": f"{config['system_prompt']}\n\nUser question: {user_message}"}
                    ]
                }
            ]
        )
        
        bot_response = response.text
        
        return jsonify({
            'success': True,
            'response': bot_response,
            'user_message': user_message
        })
    
    except Exception as e:
        print(f"Error in chat: {str(e)}")
        return jsonify({
            'error': str(e),
            'success': False,
            'status': 'error'
        }), 500

# Admin Volta Control Routes
@app.route('/admin/volta/settings', methods=['GET', 'POST'])
@login_required
def volta_settings():
    """Admin page to manage Volta chatbot settings"""
    config = load_volta_config()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'update_api_key':
            api_key = request.form.get('api_key', '').strip()
            if api_key:
                save_api_key_to_config(api_key)
                flash('✓ API Key saved successfully!', 'success')
            else:
                flash('✗ API Key cannot be empty!', 'danger')
        
        elif action == 'toggle_status':
            config['enabled'] = not config['enabled']
            save_volta_config(config)
            status = 'enabled' if config['enabled'] else 'disabled'
            flash(f'Volta is now {status}!', 'info')
        
        elif action == 'reset_config':
            default_config = load_volta_config()
            default_config['enabled'] = False
            default_config['api_key'] = ''
            save_volta_config(default_config)
            flash('Volta configuration reset. Chatbot is now sleeping.', 'warning')
        
        return redirect(url_for('volta_settings'))
    
    api_key_set = bool(get_volta_api_key())
    
    return render_template('admin_volta_settings.html', 
                         config=config,
                         api_key_set=api_key_set)

# Price History Management Routes
@app.route('/admin/price-history/clear-all', methods=['POST'])
@login_required
def clear_all_price_history():
    """Clear all price history for all products"""
    try:
        clear_price_history_all()
        flash('✓ All price history cleared successfully!', 'success')
    except Exception as e:
        flash(f'✗ Error clearing price history: {str(e)}', 'danger')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/price-history/clear/<product_id>', methods=['POST'])
@login_required
def clear_price_history(product_id):
    """Clear price history for a specific product"""
    try:
        if clear_price_history_individual(product_id):
            flash('✓ Price history for this product cleared successfully!', 'success')
        else:
            flash('✗ Product not found', 'danger')
    except Exception as e:
        flash(f'✗ Error clearing price history: {str(e)}', 'danger')
    return redirect(url_for('admin_products'))

# Website Maintenance Mode Routes
@app.route('/admin/maintenance-mode/toggle', methods=['POST'])
@login_required
def toggle_maintenance_mode():
    """Toggle maintenance mode for the entire website"""
    try:
        config = load_volta_config()
        config['maintenance_mode'] = not config['maintenance_mode']
        save_volta_config(config)
        status = 'ON' if config['maintenance_mode'] else 'OFF'
        flash(f'✓ Maintenance mode turned {status}!', 'info')
    except Exception as e:
        flash(f'✗ Error toggling maintenance mode: {str(e)}', 'danger')
    return redirect(url_for('admin_dashboard'))

# Version Management Routes
@app.route('/admin/version/update', methods=['POST'])
@login_required
def update_version():
    """Update application version"""
    try:
        new_version = request.form.get('version', '').strip()
        if not new_version:
            flash('✗ Version cannot be empty', 'danger')
            return redirect(url_for('admin_dashboard'))
        
        config = load_volta_config()
        config['version'] = new_version
        save_volta_config(config)
        flash(f'✓ Version updated to {new_version}!', 'success')
    except Exception as e:
        flash(f'✗ Error updating version: {str(e)}', 'danger')
    return redirect(url_for('admin_dashboard'))

# Initialize on startup
"""@app.before_request
def initialize():
    # Create default files if they don't exist
    if not hasattr(app, 'initialized'):
        create_default_files()
        # Initialize with sample data if no products exist
        products = load_products()
        if len(products) == 0:
            initialize_sample_data()
        app.initialized = True"""

def create_default_files():
    """Create default files and directories"""
    # Create CSS files
    css_dir = 'static/css'
    os.makedirs(css_dir, exist_ok=True)
    
    # style.css
    style_css = """/* style.css - Main Stylesheet for IoT Verse */

:root {
    --primary-color: #2563eb;
    --primary-dark: #1d4ed8;
    --secondary-color: #64748b;
    --accent-color: #f59e0b;
    --success-color: #10b981;
    --danger-color: #ef4444;
    --warning-color: #f59e0b;
    --info-color: #3b82f6;
    --dark-color: #1e293b;
    --light-color: #f8fafc;
    --border-radius: 8px;
    --box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

body {
    background-color: var(--light-color);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

.navbar-brand {
    font-weight: bold;
    color: var(--primary-color) !important;
}

.navbar-brand img {
    height: 40px;
    width: auto;
}

.version-badge {
    font-size: 0.75rem;
    background: var(--accent-color);
    color: white;
    padding: 0.25rem 0.5rem;
    border-radius: 20px;
    margin-left: 0.5rem;
}

.nav-link {
    font-weight: 500;
    padding: 0.5rem 1rem !important;
    border-radius: var(--border-radius);
    transition: all 0.3s;
}

.nav-link:hover,
.nav-link.active {
    background-color: rgba(37, 99, 235, 0.1);
    color: var(--primary-color) !important;
}

.iot-card {
    transition: transform 0.3s, box-shadow 0.3s;
    border: none;
    border-radius: 15px;
    overflow: hidden;
    height: 100%;
}

.iot-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

.card-img-top {
    height: 200px;
    object-fit: cover;
    background-color: #f1f5f9;
}

.badge-availability {
    position: absolute;
    top: 10px;
    right: 10px;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.875rem;
}

.price-tag {
    color: var(--accent-color);
    font-weight: 700;
    font-size: 1.25rem;
}

.search-box {
    max-width: 800px;
    margin: 0 auto;
}

.footer {
    background-color: var(--dark-color);
    color: white;
    padding: 2rem 0;
    margin-top: auto;
}

.btn-primary {
    background-color: var(--primary-color);
    border-color: var(--primary-color);
}

.btn-primary:hover {
    background-color: var(--primary-dark);
    border-color: var(--primary-dark);
}

.alert {
    border: none;
    border-radius: var(--border-radius);
    padding: 1rem 1.5rem;
}

.table-hover tbody tr:hover {
    background-color: rgba(37, 99, 235, 0.05);
}

.chart-container {
    height: 300px;
    position: relative;
}

.stats-card {
    border-radius: var(--border-radius);
    padding: 1.5rem;
    color: white;
    position: relative;
    overflow: hidden;
    margin-bottom: 1rem;
}

.stats-card:nth-child(1) { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.stats-card:nth-child(2) { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
.stats-card:nth-child(3) { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
.stats-card:nth-child(4) { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }

.upload-zone {
    border: 2px dashed #cbd5e1;
    border-radius: var(--border-radius);
    padding: 2rem;
    text-align: center;
    background-color: #f8fafc;
    cursor: pointer;
    transition: all 0.3s;
}

.upload-zone:hover {
    border-color: var(--primary-color);
    background-color: rgba(37, 99, 235, 0.05);
}

.badge-instock { background-color: var(--success-color) !important; }
.badge-outofstock { background-color: var(--danger-color) !important; }
.badge-lowstock { background-color: var(--warning-color) !important; color: var(--dark-color); }"""
    
    with open(os.path.join(css_dir, 'style.css'), 'w', encoding='utf-8') as f:
        f.write(style_css)
    
    # Create JS files
    js_dir = 'static/js'
    os.makedirs(js_dir, exist_ok=True)
    
    # main.js
    main_js = """// main.js - Main JavaScript for IoT Verse

document.addEventListener('DOMContentLoaded', function() {
    console.log('IoT Verse - Developed by MintFire');
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.parentNode) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    });
    
    // Price filter range
    const minPriceInput = document.querySelector('input[name="min_price"]');
    const maxPriceInput = document.querySelector('input[name="max_price"]');
    const priceRange = document.getElementById('priceRange');
    
    if (priceRange && minPriceInput && maxPriceInput) {
        noUiSlider.create(priceRange, {
            start: [parseInt(minPriceInput.value) || 0, parseInt(maxPriceInput.value) || 100000],
            connect: true,
            range: {
                'min': 0,
                'max': 100000
            },
            step: 100
        });
        
        priceRange.noUiSlider.on('update', function(values) {
            minPriceInput.value = Math.round(values[0]);
            maxPriceInput.value = Math.round(values[1]);
        });
    }
});

function showNotification(message, type = 'info') {
    // Create notification container if it doesn't exist
    let container = document.getElementById('notification-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'notification-container';
        container.style.position = 'fixed';
        container.style.top = '20px';
        container.style.right = '20px';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
    }
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.style.minWidth = '300px';
    alert.style.marginBottom = '10px';
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    container.appendChild(alert);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, 5000);
}

function getAvailabilityClass(availability) {
    switch (availability) {
        case 'In Stock': return 'badge-instock';
        case 'Out of Stock': return 'badge-outofstock';
        case 'Low Stock': return 'badge-lowstock';
        default: return 'bg-secondary';
    }
}

window.iotVerse = {
    showNotification: showNotification
};"""
    
    with open(os.path.join(js_dir, 'main.js'), 'w', encoding='utf-8') as f:
        f.write(main_js)
    
    # admin.js
    admin_js = """// admin.js - Admin Panel JavaScript

document.addEventListener('DOMContentLoaded', function() {
    console.log('IoT Verse Admin Panel');
    
    // CSV upload zone
    const uploadZone = document.querySelector('.upload-zone');
    const fileInput = document.querySelector('input[name="csv_file"]');
    
    if (uploadZone && fileInput) {
        uploadZone.addEventListener('click', () => fileInput.click());
        
        uploadZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadZone.style.borderColor = '#2563eb';
            uploadZone.style.backgroundColor = 'rgba(37, 99, 235, 0.1)';
        });
        
        uploadZone.addEventListener('dragleave', () => {
            uploadZone.style.borderColor = '#cbd5e1';
            uploadZone.style.backgroundColor = '#f8fafc';
        });
        
        uploadZone.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadZone.style.borderColor = '#cbd5e1';
            uploadZone.style.backgroundColor = '#f8fafc';
            
            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                const fileName = e.dataTransfer.files[0].name;
                uploadZone.innerHTML = `
                    <i class="bi bi-file-earmark-check display-4 text-success"></i>
                    <p class="mt-2">${fileName}</p>
                    <small class="text-muted">Ready to upload</small>
                `;
            }
        });
        
        fileInput.addEventListener('change', function() {
            if (this.files.length) {
                const fileName = this.files[0].name;
                uploadZone.innerHTML = `
                    <i class="bi bi-file-earmark-check display-4 text-success"></i>
                    <p class="mt-2">${fileName}</p>
                    <small class="text-muted">Ready to upload</small>
                `;
            }
        });
    }
    
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            const requiredFields = this.querySelectorAll('[required]');
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                if (window.iotVerse && window.iotVerse.showNotification) {
                    window.iotVerse.showNotification('Please fill in all required fields', 'danger');
                } else {
                    alert('Please fill in all required fields');
                }
            }
        });
    });
    
    // Image preview
    const imageInputs = document.querySelectorAll('input[type="file"][accept="image/*"]');
    imageInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const preview = input.closest('.mb-3').querySelector('.image-preview');
                    if (!preview) {
                        const img = document.createElement('img');
                        img.className = 'image-preview img-thumbnail mt-2';
                        img.style.maxWidth = '200px';
                        input.closest('.mb-3').appendChild(img);
                    }
                    input.closest('.mb-3').querySelector('.image-preview').src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    });
});

function confirmDelete(message = 'Are you sure you want to delete this item?') {
    return confirm(message);
}

function exportData(format) {
    if (format === 'json') {
        window.open('/api/products', '_blank');
    } else if (format === 'csv') {
        // Convert JSON to CSV
        fetch('/api/products')
            .then(response => response.json())
            .then(data => {
                const csv = convertToCSV(data);
                downloadCSV(csv, 'iot_products.csv');
            });
    }
}

function convertToCSV(data) {
    const headers = ['ID', 'Name', 'Price (INR)', 'Quantity', 'Availability', 'Type', 'Description'];
    const rows = data.map(item => [
        item.id,
        `"${item.name.replace(/"/g, '""')}"`,
        item.price,
        item.quantity,
        item.availability,
        `"${item.type.replace(/"/g, '""')}"`,
        `"${item.description.replace(/"/g, '""')}"`
    ]);
    
    return [headers.join(','), ...rows.map(row => row.join(','))].join('\\n');
}

function downloadCSV(content, filename) {
    const blob = new Blob([content], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

window.admin = {
    confirmDelete: confirmDelete,
    exportData: exportData
};"""
    
    with open(os.path.join(js_dir, 'admin.js'), 'w', encoding='utf-8') as f:
        f.write(admin_js)
    
    # Create default images directory
    images_dir = 'static/images'
    os.makedirs(images_dir, exist_ok=True)
    
    # Create a simple logo if it doesn't exist
    logo_path = os.path.join(images_dir, 'logo.png')
    if not os.path.exists(logo_path):
        # Create a simple colored square as logo
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new('RGB', (200, 100), color='#2563eb')
        d = ImageDraw.Draw(img)
        try:
            # Try to use a font
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        d.text((10, 40), "IoT Verse", fill=(255, 255, 255), font=font)
        img.save(logo_path)
    
    # Create default device image
    '''default_device_path = os.path.join(images_dir, 'default-device.jpg')
    if not os.path.exists(default_device_path):
        img = Image.new('RGB', (400, 300), color='#f1f5f9')
        d = ImageDraw.Draw(img)
        d.rectangle([50, 50, 350, 250], outline='#cbd5e1', width=2)
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        d.text((120, 140), "IoT Device", fill='#64748b', font=font)
        img.save(default_device_path)'''
    
    print("Default files created successfully")

# Error Handlers
@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500

@app.errorhandler(503)
def service_unavailable(error):
    """Handle 503 errors"""
    return render_template('503.html'), 503

@app.before_request
def check_maintenance_mode():
    """Check if maintenance mode is enabled"""
    config = load_volta_config()
    if config.get('maintenance_mode', False):
        # Allow admin to access dashboard during maintenance
        if not request.path.startswith('/admin') and not request.path.startswith('/static'):
            return render_template('maintenance.html'), 503

if __name__ == '__main__':
    # Initialize on first run
    if not os.path.exists('data/admin_password.json'):
        create_default_files()
    
    app.run(debug=True,host='0.0.0.0', port=5900)