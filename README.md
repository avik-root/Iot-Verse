# 🚀 IoT Verse - Smart Product Management & AI Chatbot Platform

<div align="center">

![IoT Verse](https://img.shields.io/badge/IoT%20Verse-v2.8-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9+-green?style=for-the-badge)
![Flask](https://img.shields.io/badge/Flask-2.3.3-lightblue?style=for-the-badge)
![AI](https://img.shields.io/badge/AI-Google%20Gemini-orange?style=for-the-badge)

**A comprehensive IoT product management platform with integrated AI chatbot, analytics, and professional dark mode UI**

**Developed and Secured by MintFire**

[Features](#-features) • [Tech Stack](#-tech-stack) • [Installation](#-installation) • [Usage](#-usage) • [Phases](#-development-phases)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Use Cases](#-use-cases)
- [Installation Guide](#-installation-guide)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Development Phases](#-development-phases)
- [Project Structure](#-project-structure)
- [API Routes](#-api-routes)
- [Database Schema](#-database-schema)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**IoT Verse** is a full-featured, enterprise-grade product management platform designed specifically for Internet of Things (IoT) businesses. It combines a robust backend with an intuitive frontend, featuring real-time price tracking, inventory management, AI-powered chatbot support, and comprehensive admin analytics.

### Key Highlights
- 🔐 **Secure Admin Panel** with role-based access control
- 🤖 **Volta AI Chatbot** powered by Google Gemini 2.5 Flash
- 📊 **Advanced Analytics** with real-time price tracking and charts
- 🌙 **Professional Dark Mode** with seamless theme switching
- 📱 **Fully Responsive Design** for desktop, tablet, and mobile
- 🖼️ **Product Image Management** with optimized storage
- 💾 **JSON-based Database** for easy data portability
- 🔍 **Smart Search & Filtering** by device type and properties

---

## 📅 Recent Updates (Feb 8, 2026)

### 🎨 WebUI Modernization - Complete Overhaul
- **Premium Header Design** - Completely rebuilt navigation with:
  - Animated brand logo with shimmer effect
  - Pill-style navigation with smooth hover states
  - Integrated search box with glassmorphism
  - Dynamic currency selector with 14+ currencies
  - Responsive hamburger menu for mobile
  - Scroll shadow effects and performance optimizations

- **New IoT-Centric Branding**
  - Custom IoT logo (circuit yin-yang design with microchip icons)
  - Matching favicon with glowing neon effect
  - Indigo-to-cyan gradient color scheme throughout
  - Apple touch icon support for mobile devices

- **Enhanced Dark Mode**
  - Rich dark navy backgrounds (#0f172a, #1e293b)
  - Glowing accent effects on interactive elements
  - Improved text visibility for all dashboard elements
  - Comprehensive border visibility fixes
  - Smooth theme transition animations

- **Modern CSS Enhancements**
  - CSS custom properties for consistent theming
  - Glassmorphism effects on cards and navigation
  - Micro-animations for improved UX
  - React/Next.js-inspired premium aesthetic

### 💱 Currency System Improvements
- Dynamic currency symbol display in header (₹, $, €, £, ¥, etc.)
- Fixed double ₹ symbol display bug
- Currency persists across page navigation via localStorage
- Real-time price conversion with API integration

### 🐛 Bug Fixes & Improvements
- Fixed admin login form field names (`email` vs `username`)
- Fixed product detail page double currency symbol issue
- Fixed currency.js adding duplicate ₹ symbols
- Fixed ASCII art box outline in dark mode
- Improved form input styling in dark mode
- Enhanced table border visibility in dark mode

---

## 🚀 Upcoming Features

### Phase 6: Deployment & Scaling (Q2 2026)
- [ ] **Docker Containerization** - Containerized deployment for easy scaling
- [ ] **Kubernetes Orchestration** - Cloud-native infrastructure
- [ ] **CI/CD Pipeline** - Automated testing and deployment with GitHub Actions
- [ ] **Database Migration** - PostgreSQL for production workloads
- [ ] **Redis Caching** - Performance optimization layer

### Phase 7: Enterprise Features (Q3 2026)
- [ ] **Multi-User Support** - Team collaboration features
- [ ] **Role-Based Permissions** - Admin, Manager, Viewer roles
- [ ] **Audit Logging** - Complete activity tracking
- [ ] **API Rate Limiting** - Protection against abuse
- [ ] **Webhook Integrations** - External service notifications

### Phase 8: Advanced Analytics (Q4 2026)
- [ ] **Machine Learning Insights** - Price prediction and trend analysis
- [ ] **Custom Dashboards** - Drag-and-drop analytics builder
- [ ] **Export Reports** - PDF/Excel export functionality
- [ ] **Real-time Notifications** - Push notifications for alerts

---

## 🔧 Recent Bug Fixes (Feb 2026)

| Issue | Status | Fix Details |
|-------|--------|-------------|
| Double ₹ symbol on prices | ✅ Fixed | Removed duplicate CSS `::before` and JS symbol addition |
| Admin login form not working | ✅ Fixed | Changed form field from `username` to `email` |
| ASCII art box outline in dark mode | ✅ Fixed | Added explicit `border: none` and `background: transparent` |
| Currency dropdown showing INR only | ✅ Fixed | Added dynamic symbol mapping for 14 currencies |
| Dark mode text visibility | ✅ Fixed | Added comprehensive text color overrides |
| Form inputs in dark mode | ✅ Fixed | Added proper background and text colors |
| Table borders in dark mode | ✅ Fixed | Added border-color overrides |
| Logo background animation | ✅ Fixed | Removed gradient background, show only logo |

---

## ✨ Features

### Core Features
- ✅ **Product Management**
  - Add, edit, delete products with detailed specifications
  - Bulk CSV import/export functionality
  - Real-time inventory tracking
  - Product categorization by device type
  
- ✅ **Admin Dashboard**
  - Comprehensive system statistics
  - Real-time price history tracking
  - Sales metrics and analytics
  - User activity monitoring
  - Quick action buttons

- ✅ **Volta AI Chatbot**
  - Intelligent responses powered by Google Gemini API
  - Specialized in IoT, AI/ML, Cyber Security, and CSE topics
  - Conversation history management
  - Real-time typing indicators
  - Code syntax highlighting in responses

- ✅ **User Interface**
  - Professional dark/light theme support
  - Responsive design for all devices
  - Interactive product cards with real-time updates
  - Advanced filtering and search
  - Smooth animations and transitions

- ✅ **Admin Features**
  - Secure login authentication with bcrypt encryption
  - Admin settings and configuration management
  - API key management for Volta chatbot
  - System information display
  - **NEW:** Automatic session timeout (30 min inactivity)
  - **NEW:** Session timeout warning with countdown
  - **NEW:** Fast product search with real-time filtering
  - **NEW:** Drag-and-drop product reordering
  - **NEW:** Secure session cookies (HttpOnly, SameSite)

### Advanced Features
- 🔄 Real-time price history and trend analysis
- 📈 Interactive charts using Matplotlib
- 🖼️ Image processing and optimization with Pillow
- 📊 CSV data import with pandas
- 🔒 Password-protected admin credentials
- 💾 Persistent data storage with JSON
- 🌐 RESTful API endpoints
- 🔍 **NEW:** Smart product search functionality with multiple field support
- ⏱️ **NEW:** Automatic session timeout with inactivity detection
- ⚠️ **NEW:** Session expiration warning modal
- 💱 **NEW:** Global currency dropdown on all pages (11 currencies supported)

---

## 🛠️ Tech Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| **Flask** | 2.3.3 | Web framework |
| **Flask-Bcrypt** | 1.0.1 | Password hashing and security |
| **Flask-Login** | 0.6.2 | User session management |
| **Python** | 3.9+ | Programming language |
| **Python-dotenv** | 1.0.0 | Environment variable management |

### Data & Processing
| Technology | Version | Purpose |
|------------|---------|---------|
| **Pandas** | 2.0.3 | Data analysis and CSV processing |
| **Matplotlib** | 3.7.2 | Chart generation and visualization |
| **Pillow** | 10.0.0 | Image processing and optimization |
| **JSON** | Built-in | Data storage format |

### AI & Machine Learning
| Technology | Version | Purpose |
|------------|---------|---------|
| **Google Gemini API** | 0.1.1 | AI chatbot backend |
| **Genai Client** | Latest | Google AI integration |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| **HTML5** | Latest | Markup |
| **CSS3** | Latest | Styling (with dark mode support) |
| **JavaScript** | ES6+ | Interactivity |
| **Bootstrap 5** | Latest | UI Framework |
| **Bootstrap Icons** | Latest | Icon library |

### Development & Deployment
| Technology | Purpose |
|------------|---------|
| **Jinja2** | Server-side templating |
| **Werkzeug** | WSGI utilities |
| **Gunicorn** | Production WSGI server (optional) |

---

## 💡 Use Cases

### E-Commerce & Retail
- IoT device marketplace with inventory management
- Real-time price tracking and competitor analysis
- Automated product recommendations through AI

### Manufacturing & Supply Chain
- IoT equipment catalog management
- Price history analysis for cost optimization
- Vendor management system

### Smart Home & Automation
- Product catalog for smart home devices
- Customer support through intelligent chatbot
- Usage analytics and trend analysis

### Education & Research
- IoT device database for educational institutions
- AI chatbot for technical support and learning
- Data analysis tools for research projects

### Enterprise Solutions
- Internal product management system
- Employee support via AI chatbot
- Department-specific inventory tracking
- Budget monitoring through analytics

---

## 📦 Installation Guide

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Git
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/iot-verse.git
cd iot-verse
```

### Step 2: Create Virtual Environment
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup Environment Variables
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
FLASK_ENV=development
FLASK_DEBUG=True
```

### Step 5: Initialize Data Directories
```bash
mkdir -p data uploads/product_images static/css static/js static/images
```

### Step 6: Run the Application
```bash
python3 app.py
```

The application will be available at `http://localhost:5000`

---

## ⚙️ Configuration

### Environment Variables (.env)
```env
# Google Gemini AI API Key (Required for Volta chatbot)
GEMINI_API_KEY=your_api_key_here

# Flask Configuration
FLASK_ENV=development          # development or production
FLASK_DEBUG=True              # Enable debug mode (disable in production)

# Application Settings
SECRET_KEY=your-secret-key    # Change this in production
MAX_UPLOAD_SIZE=16777216      # Maximum upload size in bytes (16MB)
```

### Getting Google Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key and add to `.env` file

### Admin Credentials
First time setup:
1. Go to `/admin-login`
2. Create initial admin account
3. Credentials are hashed with bcrypt for security

---

## 🚀 Usage

### Accessing the Application

#### Home Page
- **URL:** `http://localhost:5000/`
- View all available IoT products
- Search and filter by device type
- Click on products for detailed information
- Access Volta AI chatbot from the sidebar

#### Product Details
- **URL:** `http://localhost:5000/product/<product_id>`
- View comprehensive product information
- Check price history and trends
- See inventory status
- Chat with Volta AI about the product

#### Admin Dashboard
- **URL:** `http://localhost:5000/admin-dashboard`
- System statistics and analytics
- Price history charts
- Product management tools
- User activity monitoring

#### Admin Product Management
- **URL:** `http://localhost:5000/admin-products`
- Add new products with images
- Edit existing product information
- Delete products
- Bulk import via CSV
- Export product data

#### Volta Chatbot Settings
- **URL:** `http://localhost:5000/admin/volta-settings`
- Configure Google Gemini API key
- Enable/disable chatbot
- View system prompt
- Reset configuration
- Monitor Volta specializations

#### Chat Interface
- **URL:** `http://localhost:5000/chat`
- Full-screen chat with Volta AI
- Code syntax highlighting
- Conversation history
- Typing indicators

### Dark Mode
- Click the theme toggle button (☀️/🌙) in the navbar
- Preference is saved to browser localStorage
- Persists across sessions

### Session & Security Management
- **Automatic Session Timeout**: 30 minutes of inactivity
- **Timeout Warning**: Alert appears at 25 minutes with countdown timer
- **Activity Detection**: Session extends with any user activity (click, scroll, keyboard)
- **Session Options**:
  - Click "Stay Logged In" in warning modal to continue
  - Click "Logout Now" to logout manually
  - Let timer expire for automatic logout
- **Security Features**:
  - HttpOnly cookies prevent JavaScript access
  - SameSite protection against CSRF attacks
  - Secure flag enabled in production (HTTPS)
- **Configuration**: See [SESSION_TIMEOUT_CONFIG.md](SESSION_TIMEOUT_CONFIG.md) for customization

### Product Management Workflow
```
1. Navigate to Admin Products
2. Add Product → Fill Details → Upload Image → Save
3. View on Home Page
4. Edit from Admin Dashboard
5. Track Price Changes in Analytics
6. Get AI Insights from Volta
```

---

## 🎯 Development Phases

### Phase 1: Foundation & Core Features ✅
**Objective:** Build robust backend and basic UI
- [x] Flask application setup and configuration
- [x] User authentication system with bcrypt
- [x] Product database schema (JSON)
- [x] Admin CRUD operations
- [x] Basic responsive UI with Bootstrap
- [x] Image upload and management
- [x] CSV import functionality

**Technologies:** Flask, Flask-Login, Flask-Bcrypt, Pandas

### Phase 2: Analytics & Data Visualization ✅
**Objective:** Add business intelligence features
- [x] Price history tracking system
- [x] Real-time analytics dashboard
- [x] Interactive charts with Matplotlib
- [x] Statistical analysis
- [x] Trend analysis and predictions
- [x] Export functionality

**Technologies:** Matplotlib, Pandas, Python datetime

### Phase 3: AI Chatbot Integration ✅
**Objective:** Implement intelligent customer support
- [x] Google Gemini API integration
- [x] Volta AI chatbot setup
- [x] Specialized AI prompts (IoT, AI/ML, Security, CSE)
- [x] Conversation history management
- [x] Admin Volta configuration panel
- [x] API key management
- [x] Code syntax highlighting

**Technologies:** Google Genai, Flask-JSON, Environment variables

### Phase 4: UI/UX Enhancement ✅
**Objective:** Professional design and user experience
- [x] Professional dark mode implementation
- [x] Mobile responsive design
- [x] CSS animations and transitions
- [x] Icon integration (Bootstrap Icons)
- [x] Form validation and error handling
- [x] Toast notifications and alerts
- [x] Accessibility improvements

**Technologies:** CSS3, JavaScript ES6+, Bootstrap 5, Icons

### Phase 5: Advanced Features (Current) 🔄
**Objective:** Enterprise-grade capabilities
- [x] Advanced search and filtering
- [x] Batch operations
- [x] Real-time data updates
- [x] API endpoints for integrations
- [x] Performance optimization
- [x] Security hardening
- [ ] Multi-user support
- [ ] Role-based permissions
- [ ] Audit logging
- [ ] Caching layer (Redis)

### Phase 6: Deployment & Scaling (Upcoming)
**Objective:** Production-ready deployment
- [ ] Docker containerization
- [ ] Kubernetes orchestration
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Cloud deployment (AWS/Azure/GCP)
- [ ] Database migration (PostgreSQL)
- [ ] Performance monitoring
- [ ] Load balancing
- [ ] Backup and disaster recovery

**Technologies:** Docker, Kubernetes, GitHub Actions, Cloud providers

---

## 📁 Project Structure

```
iot-verse/
├── app.py                          # Main Flask application
├── app_error.py                    # Error handling
├── app1.py                         # Alternative app configuration
├── requirements.txt                # Python dependencies
├── setup.py                        # Setup configuration
├── .env                            # Environment variables
├── .gitignore                      # Git ignore rules
│
├── data/                           # Data storage
│   ├── admin_password.json         # Admin credentials (hashed)
│   ├── products.json               # Product database
│   ├── price_history.json          # Price tracking data
│   └── volta_config.json           # Chatbot configuration
│
├── static/                         # Static assets
│   ├── css/
│   │   ├── style.css              # Main styles
│   │   └── darkmode.css           # Dark mode styles
│   ├── js/
│   │   ├── main.js                # Core JavaScript
│   │   ├── admin.js               # Admin panel scripts
│   │   └── charts.js              # Chart rendering
│   ├── images/                    # Static images
│   └── stock_image.py             # Stock image generator
│
├── templates/                      # Jinja2 templates
│   ├── base.html                  # Base template
│   ├── home.html                  # Home page
│   ├── product_detail.html        # Product details
│   ├── add_product.html           # Product creation
│   ├── edit_product.html          # Product editing
│   ├── admin_login.html           # Admin login
│   ├── admin_dashboard.html       # Admin dashboard
│   ├── admin_products.html        # Product management
│   ├── admin_volta_settings.html  # Volta configuration
│   └── volta_chat.html            # Chat interface
│
├── uploads/
│   └── product_images/            # User uploaded images
│
├── __pycache__/                   # Python cache
└── Products.csv                   # Sample product data
```

---

## 🔌 API Routes

### Public Routes

#### Home & Products
```
GET  /                              # Home page with product listing
GET  /product/<product_id>          # Product detail page
GET  /chat                          # Volta chat interface
```

#### Chat API
```
POST /api/chat                      # Send message to Volta AI
     - body: { "message": "Your question" }
     - returns: { "response": "AI response" }

GET  /api/chat-history/<session>    # Get conversation history
```

#### Product API
```
GET  /api/products                  # Get all products (JSON)
GET  /api/product/<id>              # Get single product (JSON)
GET  /api/products/filter           # Filter products by type
GET  /api/price-history/<id>        # Get price history for product
POST /record-daily-price            # Record daily price for all products
```

**Price History Features:**
- Automatic daily price tracking
- Historical price data storage (up to 365 days)
- Price trend analysis
- Bulk price history management

### Admin Routes (Login Required)

#### Admin Dashboard
```
GET  /admin-login                   # Admin login page
POST /admin-login                   # Process admin login

GET  /admin-dashboard               # Admin dashboard
GET  /admin-dashboard/stats         # Dashboard statistics (JSON)

POST /logout                        # Logout admin
```

#### Product Management
```
GET  /admin-products                # Product management page with search
POST /add-product                   # Add new product
POST /edit-product/<id>             # Edit product
POST /delete-product/<id>           # Delete product
POST /import-csv                    # Bulk import from CSV
GET  /export-products               # Export products as CSV
POST /api/products/reorder          # Reorder products (drag-and-drop)
POST /clear-price-history/<id>      # Clear price history for product
```

**NEW Search Functionality:**
- Real-time product search on admin products page
- Search by: product name, description, price, type
- Instant filtering without page reload
- Clear button for quick search reset

#### Volta Settings
```
GET  /admin/volta-settings          # Volta configuration page
POST /admin/volta-settings          # Update Volta settings
     - Actions: update_api_key, toggle_status, reset_config
```

---

## 💾 Database Schema

### products.json
```json
{
  "products": [
    {
      "id": "unique-uuid",
      "name": "Product Name",
      "category": "Device Type",
      "description": "Product Description",
      "price": 299.99,
      "quantity": 50,
      "image": "filename.jpg",
      "specifications": {
        "connectivity": "WiFi",
        "power": "Battery",
        "features": ["Feature1", "Feature2"]
      },
      "created_at": "2024-12-29T10:30:00",
      "updated_at": "2024-12-29T10:30:00"
    }
  ]
}
```

### price_history.json
```json
{
  "product_id": [
    {
      "date": "2024-12-29",
      "price": 299.99,
      "quantity": 50
    }
  ]
}
```

### admin_password.json
```json
{
  "email": "admin@iotverse.com",
  "password_hash": "bcrypt_hashed_password",
  "created_at": "2024-12-29"
}
```

### volta_config.json
```json
{
  "enabled": true,
  "api_key": "cached_api_key",
  "system_prompt": "You are Volta...",
  "model": "gemini-2.5-flash",
  "specializations": ["IoT", "AI/ML", "Security", "CSE"]
}
```

---

## 🔒 Security Features

- **Password Hashing:** Bcrypt encryption for admin credentials
- **Session Management:** Flask-Login with secure session tokens
- **Environment Variables:** Sensitive data stored in .env (not in repo)
- **CSRF Protection:** Built into Flask forms
- **File Upload Validation:** Filename sanitization with Werkzeug
- **SQL Injection Prevention:** JSON-based storage (no SQL)
- **XSS Protection:** Jinja2 auto-escaping

---

## 🐛 Troubleshooting

### Issue: "API Key Not Configured" Error
**Solution:**
1. Generate API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Add to `.env` file: `GEMINI_API_KEY=your_key`
3. Restart the Flask application
4. Visit `/admin/volta-settings` to verify

### Issue: Image Upload Fails
**Solution:**
1. Check uploads directory permissions: `chmod 755 uploads/product_images`
2. Verify image format (jpg, png, gif supported)
3. Check file size (max 16MB)
4. Clear browser cache

### Issue: Admin Login Not Working
**Solution:**
1. Delete `data/admin_password.json`
2. Restart application
3. Create new admin account at `/admin-login`
4. Clear browser cookies

### Issue: Dark Mode Not Persisting
**Solution:**
1. Enable localStorage in browser
2. Check browser privacy settings
3. Clear browser cache and try again
4. Disable browser extensions that block storage

### Issue: Charts Not Displaying
**Solution:**
1. Verify Matplotlib installation: `pip install matplotlib`
2. Check `static/images` directory exists and has write permissions
3. Restart Flask application
4. Clear browser cache

### Issue: Product Search Not Working
**Solution:**
1. Ensure JavaScript is enabled in your browser
2. Check browser console for errors (F12)
3. Verify product data is loaded in `products.json`
4. Clear browser cache and reload admin products page
5. Try searching with simple keywords first

### Issue: Price History Data Missing
**Solution:**
1. Verify `data/price_history.json` exists
2. Check file permissions: `chmod 644 data/price_history.json`
3. Run price recording script manually:
   ```bash
   python3 -c "from app import record_daily_price, load_products; record_daily_price(load_products())"
   ```
4. Verify cron job is running (if automated)

### Issue: Session Timeout Not Working
**Solution:**
1. Verify `SESSION_REFRESH_EACH_REQUEST = True` in app.py
2. Check `session_manager.js` is loaded: Open DevTools (F12) and check Scripts tab
3. Ensure JavaScript is enabled in browser
4. Verify timeout settings in `session_manager.js`
5. Clear browser cookies and restart Flask app
6. Check browser console for JavaScript errors

### Issue: Session Timeout Warning Modal Not Appearing
**Solution:**
1. Verify Bootstrap is loaded: Check DevTools > Network tab
2. Check browser console for errors (F12)
3. Verify `session_manager.js` is included in base.html
4. Ensure admin route check is working: `if window.location.pathname.startsWith('/admin')`
5. Test on `/admin/dashboard` page (modal only shows on admin routes)

### Issue: Session Expires Immediately
**Solution:**
1. Check `PERMANENT_SESSION_LIFETIME` setting (should be 30 minutes)
2. Verify `SESSION_REFRESH_EACH_REQUEST = True`
3. Check if server time is correct
4. Ensure session cookies are not blocked
5. Try in incognito/private browser mode

### Issue: Port 5000 Already in Use
**Solution:**
```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>

# Or run on different port
python3 app.py --port 5001
```

---

## 🚀 Performance Optimization

### For Development
- Enable debug mode for hot-reload
- Use development WSGI server
- Browser caching disabled

### For Production
- Disable debug mode
- Use Gunicorn WSGI server
- Enable compression
- Minimize CSS/JavaScript
- Implement caching (Redis)
- Use CDN for static assets
- Enable HTTPS

### Recommended Production Setup
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

---

## 📚 Additional Resources

### API Documentation
- [Google Gemini API](https://ai.google.dev)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Bootstrap 5](https://getbootstrap.com/docs/5.0/)

### Tutorials & Guides
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [Dark Mode Implementation](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme)
- [Image Processing with Pillow](https://pillow.readthedocs.io/)

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Fork & Clone
```bash
git clone https://github.com/yourusername/iot-verse.git
cd iot-verse
```

### Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### Make Changes & Commit
```bash
git add .
git commit -m "feat: add new feature"
```

### Push & Create Pull Request
```bash
git push origin feature/your-feature-name
```

### Contribution Guidelines
- Follow PEP 8 for Python code
- Add comments for complex logic
- Update README.md if adding features
- Test thoroughly before submitting PR
- Write descriptive commit messages

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### Summary
- ✅ Free to use, modify, and distribute
- ✅ Must include license and copyright notice
- ✅ No liability or warranty

---

## 📞 Support & Contact

- **Issues:** [GitHub Issues](https://github.com/avik-root/iot-verse/issues)
- **Discussions:** [GitHub Discussions](https://github.com/avik-root/iot-verse/discussions)
- **Email:** work.aviksamanta@gmail.com

---

## 🙏 Acknowledgments

- [Google Gemini API](https://ai.google.dev) for AI capabilities
- [Flask Community](https://palletsprojects.com/) for the amazing framework
- [Bootstrap Team](https://getbootstrap.com/) for UI components
- All contributors and users of IoT Verse

---

<div align="center">

**Made with ❤️ by the IoT Verse Team**

Star ⭐ us on GitHub if you find this project helpful!

[⬆ Back to Top](#-iot-verse---smart-product-management--ai-chatbot-platform)

</div>
