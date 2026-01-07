# SA7BA Custom App - Production Deployment Guide

## 🚀 Quick Start Deployment

### Step 1: Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `sa7ba_custom`
3. Description: "ERPNext v15 custom app for SA7BA.com - Guest checkout and area-based delivery charges"
4. Visibility: Private (recommended)
5. **Do not** initialize with README, .gitignore, or license
6. Click "Create repository"

### Step 2: Push Code to GitHub
```bash
# Navigate to your app directory
cd /home/shakeel/CascadeProjects/sa7ba_custom

# Add remote repository (replace with your repo URL)
git remote add origin https://github.com/shakeelviam/sa7ba_custom.git

# Push to GitHub
git push -u origin master
```

### Step 3: Deploy to Production Server

#### Option A: Using the Deployment Script (Recommended)
```bash
# On production server
cd /path/to/your/erpnext-bench

# Clone the app
bench get-app https://github.com/shakeelviam/sa7ba_custom.git

# Install the app
bench install-app sa7ba_custom

# Run setup script
bench --site sa7ba.com execute sa7ba_custom.setup_data.delivery_areas.setup

# Migrate database
bench --site sa7ba.com migrate

# Build assets
bench build

# Restart services
bench restart
```

#### Option B: Manual Installation
```bash
# On production server
cd /path/to/your/erpnext-bench/apps

# Clone the app
git clone https://github.com/shakeelviam/sa7ba_custom.git

# Install dependencies
cd ../..
bench setup requirements --dev

# Install the app
bench install-app sa7ba_custom

# Run setup
bench --site sa7ba.com execute sa7ba_custom.setup_data.delivery_areas.setup

# Migrate
bench --site sa7ba.com migrate

# Build and restart
bench build
bench restart
```

### Step 4: Post-Deployment Configuration

#### 1. Verify Installation
```bash
# Check if app is installed
bench --site sa7ba.com list-apps | grep sa7ba_custom

# Check delivery areas
bench --site sa7ba.com console
>>> frappe.get_all('Delivery Area')
```

#### 2. Configure Webshop
1. Go to your ERPNext instance: `https://sa7ba.com/desk`
2. Navigate to **Website > Web Settings**
3. Ensure **Enable Shopping Cart** is checked
4. Clear website cache: `bench --site sa7ba.com clear-cache`

#### 3. Test Functionality
1. **Guest Checkout**: Add product to cart → Checkout → Select Guest option
2. **Account Checkout**: Add product to cart → Checkout → Select Account option
3. **Language Toggle**: Test English/Arabic switching
4. **Delivery Areas**: Verify all 24 areas appear with correct charges

## 🔧 Detailed Configuration

### Webshop Settings
```bash
# Enable Webshop if not already enabled
bench --site sa7ba.com set-config "enable_shopping_cart" 1

# Set default currency to KWD
bench --site sa7ba.com set-config "default_currency" "KWD"

# Enable guest checkout
bench --site sa7ba.com set-config "allow_guest_checkout" 1
```

### Delivery Areas Verification
```bash
# Check delivery areas in console
bench --site sa7ba.com console
>>> areas = frappe.get_all('Delivery Area', fields=['area_code', 'area_name', 'delivery_charge'])
>>> for area in areas:
...     print(f"{area.area_code}: {area.area_name} - KWD {area.delivery_charge}")
```

### Custom Fields Verification
```bash
# Verify custom fields were created
bench --site sa7ba.com console
>>> frappe.get_meta('Customer').fields
>>> frappe.get_meta('Sales Order').fields
>>> frappe.get_meta('Address').fields
```

## 🚨 Troubleshooting

### Common Issues

#### 1. App Installation Fails
```bash
# Check permissions
ls -la /path/to/your/erpnext-bench/apps/sa7ba_custom

# Check Python syntax
cd /path/to/your/erpnext-bench/apps/sa7ba_custom
python -m py_compile sa7ba_custom/api.py
```

#### 2. Delivery Areas Not Showing
```bash
# Run setup script again
bench --site sa7ba.com execute sa7ba_custom.setup_data.delivery_areas.setup

# Check if doctype exists
bench --site sa7ba.com console
>>> frappe.get_meta('Delivery Area')
```

#### 3. Template Override Not Working
```bash
# Clear cache and rebuild
bench --site sa7ba.com clear-cache
bench build
bench restart

# Check hooks
bench --site sa7ba.com console
>>> frappe.get_hooks('app_include')
```

#### 4. API Endpoints Not Working
```bash
# Check if API is whitelisted
bench --site sa7ba.com console
>>> frappe.get_hooks('whitelisted_methods')
```

## 📊 Monitoring & Maintenance

### Daily Checks
```bash
# Check app status
bench --site sa7ba.com list-apps

# Check delivery area data
bench --site sa7ba.com console
>>> frappe.db.count('Delivery Area')
```

### Weekly Maintenance
```bash
# Clear cache
bench --site sa7ba.com clear-cache

# Restart services
bench restart

# Check logs
tail -f /path/to/your/erpnext-bench/logs/web.log
```

### Monthly Updates
```bash
# Pull latest updates
cd /path/to/your/erpnext-bench/apps/sa7ba_custom
git pull origin master

# Migrate if needed
bench --site sa7ba.com migrate

# Build and restart
bench build
bench restart
```

## 🔄 Backup & Recovery

### Before Updates
```bash
# Backup database
bench --site sa7ba.com backup

# Backup app files
cp -r /path/to/your/erpnext-bench/apps/sa7ba_custom /backup/path/
```

### Rollback Procedure
```bash
# If issues occur, rollback to previous version
cd /path/to/your/erpnext-bench/apps/sa7ba_custom
git log --oneline
git checkout <previous-commit-hash>

# Restore database if needed
bench --site sa7ba.com --force restore /path/to/backup/database.sql
```

## 📞 Support

### For Issues:
1. Check logs: `/path/to/your/erpnext-bench/logs/`
2. Review this guide
3. Check GitHub repository for updates
4. Contact development team

### Success Indicators:
- ✅ App appears in `bench list-apps`
- ✅ Delivery areas show in Delivery Area doctype
- ✅ Guest checkout toggle appears on checkout page
- ✅ Language toggle works (English/Arabic)
- ✅ Delivery charges calculate correctly
- ✅ Both checkout options function properly

---

**Next Steps**: After successful deployment, monitor the first few orders to ensure everything works as expected. Check the delivery charges summary report to verify data collection.
