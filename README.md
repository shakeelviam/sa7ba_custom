# SA7BA Custom App for ERPNext v15

## Overview

SA7BA Custom is a custom ERPNext app that implements guest checkout functionality and area-based delivery charges for the SA7BA Hookah e-commerce platform (sa7ba.com).

## Features

### 1. Dual Checkout System
- **Guest Checkout**: Customers can complete purchases without creating an account
- **Account Checkout**: Existing Webshop account-based checkout (preserved)
- **Toggle Interface**: Users can choose between guest and account checkout
- **Seamless Integration**: Both options work with area-based delivery charges

### 2. Area-Based Delivery Charges
- **No Free Delivery**: Every order pays delivery charges (critical business requirement)
- **Kuwait Area Coverage**: 24 delivery areas with specific charges
- **Dynamic Pricing**: Delivery charges automatically calculated based on selected area
- **Real-time Updates**: Cart totals update immediately when area is selected

### 3. Bilingual Support (English/Arabic)
- **Language Toggle**: Switch between English and Arabic on checkout and cart pages
- **RTL Support**: Right-to-left layout for Arabic text
- **Complete Translation**: All UI elements translated
- **Persistent Language**: Language preference maintained during session

### 4. Enhanced User Experience
- **Modern UI**: Clean, responsive interface with smooth animations
- **Mobile Optimized**: Works seamlessly on all devices
- **Error Handling**: Comprehensive validation and user feedback
- **Progress Indicators**: Loading states and progress feedback

## Technical Architecture

### Backend Components
- **Custom Doctypes**: Delivery Area management
- **API Endpoints**: Guest checkout and delivery area management
- **Hooks & Overrides**: Integration with Webshop cart functionality
- **Data Validation**: Comprehensive input validation and sanitization

### Frontend Components
- **JavaScript Manager**: DeliveryAreaManager class for area selection
- **Template Overrides**: Custom checkout and cart pages
- **CSS Styling**: Modern, responsive design system
- **Form Validation**: Client-side validation with server-side verification

## Installation

### Prerequisites
- ERPNext v15
- Webshop App (latest version)
- Python 3.10+
- Node.js 18+

### Step 1: App Installation
```bash
# Navigate to your frappe-bench directory
cd /path/to/your/frappe-bench

# Clone the app
bench get-app sa7ba_custom https://github.com/your-org/sa7ba_custom.git

# Install the app
bench install-app sa7ba_custom

# Migrate database
bench migrate
```

### Step 2: Setup Initial Data
```bash
# Run the setup script to create delivery areas and delivery charge item
bench --site your-site.domain execute sa7ba_custom.sa7ba_custom.setup_data.delivery_areas.setup_initial_data
```

### Step 3: Configure Settings
1. **Enable Guest Checkout**: Go to Website Settings and ensure guest access is enabled
2. **Configure Item Groups**: Ensure "Services" item group exists for delivery charges
3. **Set Up Email Templates**: Create "Guest Order Confirmation" email template
4. **Configure Taxes**: Set up tax rules if applicable

### Step 4: Verify Installation
1. Check that Delivery Area doctype is available
2. Verify delivery areas are created (24 Kuwait areas)
3. Confirm "DELIVERY-CHARGE" item exists
4. Test guest checkout flow

## Configuration

### Delivery Areas
Delivery areas can be managed through the Delivery Area doctype:
- Go to Delivery Area list
- Add/edit areas with specific charges
- Set estimated delivery times
- Enable/disable areas as needed

### Custom Fields
The app adds the following custom fields:
- **Customer**: `custom_is_guest_customer`, `custom_guest_checkout_count`
- **Sales Order**: `custom_is_guest_order`, `custom_guest_email`, `custom_guest_phone`
- **Address**: `custom_delivery_area`
- **Sales Order Item**: `custom_is_delivery_charge`

### API Endpoints
- `GET /api/method/sa7ba_custom.api.get_delivery_areas` - Get all active delivery areas
- `POST /api/method/sa7ba_custom.api.process_guest_checkout` - Process guest checkout
- `POST /api/method/sa7ba_custom.api.update_cart_delivery` - Update cart with delivery charge
- `POST /api/method/sa7ba_custom.api.validate_guest_info` - Validate guest information

## Usage

### For Customers
1. **Add items to cart** - Normal shopping cart experience
2. **Select delivery area** - Choose from dropdown during checkout
3. **Choose checkout method** - Toggle between Guest or Account checkout
4. **Complete purchase** - Pay with delivery charge included

#### Guest Checkout Flow
```
Add to Cart → Cart Page → Choose Guest Checkout → Fill Form → Payment
```

#### Account Checkout Flow
```
Add to Cart → Cart Page → Choose Account Checkout → Login → Payment
```

### For Administrators
1. **Manage delivery areas** - Update charges and delivery times
2. **Monitor both checkout types** - Track guest and account orders
3. **View reports** - Access delivery charges summary report
4. **Configure settings** - Adjust app behavior as needed

## Reports

### Delivery Charges Summary
- **Location**: Reports > Delivery Charges Summary
- **Purpose**: Analyze delivery charges by area
- **Metrics**: Order count, total charges, average order value
- **Filters**: Date range, specific areas

## Troubleshooting

### Common Issues

#### Guest Checkout Not Working
1. Verify guest access is enabled in Website Settings
2. Check that API endpoints are whitelisted
3. Ensure custom fields are created properly

#### Delivery Charges Not Calculating
1. Verify delivery areas are set up correctly
2. Check that "DELIVERY-CHARGE" item exists
3. Ensure cart overrides are working

#### Template Overrides Not Applied
1. Verify app is installed and enabled
2. Check template file permissions
3. Clear browser cache and restart bench

### Debug Mode
Enable debug mode for detailed error information:
```bash
bench --site your-site.domain set-config developer_mode 1
bench --site your-site.domain clear-cache
```

## Support

### Log Files
- ERPNext logs: `bench --site your-site.domain show-logs`
- App-specific logs: Check Frappe logs for "sa7ba_custom" entries

### Common Commands
```bash
# Restart bench
bench restart

# Clear cache
bench --site your-site.domain clear-cache

# Migrate database
bench migrate

# Check app status
bench show-apps
```

## Development

### File Structure
```
sa7ba_custom/
├── sa7ba_custom/
│   ├── custom/           # Business logic
│   ├── overrides/        # Webshop overrides
│   ├── doctype/          # Custom doctypes
│   ├── api.py           # API endpoints
│   └── setup_data/      # Initial data setup
├── public/
│   ├── js/              # Frontend JavaScript
│   └── css/             # Stylesheets
├── templates/           # Template overrides
├── fixtures/           # Data fixtures
└── reports/            # Custom reports
```

### Testing
```bash
# Run tests
bench --site your-site.domain test sa7ba_custom

# Test specific functionality
bench --site your-site.domain execute sa7ba_custom.sa7ba_custom.api.get_delivery_areas
```

## Version History

### v1.0.0 (2024-03-15)
- Initial release
- Guest checkout functionality
- Area-based delivery charges
- Kuwait delivery areas (24 areas)
- Delivery charges summary report

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Contact

- **Support**: dev@sa7ba.com
- **Repository**: https://github.com/your-org/sa7ba_custom
- **Documentation**: https://docs.sa7ba.com
