#!/bin/bash

# SA7BA Custom App Deployment Script
# This script helps deploy the app to production ERPNext server

set -e

echo "🚀 Starting SA7BA Custom App Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in a frappe-bench
if [ ! -d "apps" ] || [ ! -f "bench.py" ]; then
    print_error "This script must be run from within a frappe-bench directory"
    exit 1
fi

print_status "Checking prerequisites..."

# Check if app directory exists
if [ ! -d "apps/sa7ba_custom" ]; then
    print_error "SA7BA Custom app not found in apps directory"
    print_status "Please install the app first using: bench get-app sa7ba_custom <repository-url>"
    exit 1
fi

print_status "Stopping services..."
bench stop

print_status "Installing app dependencies..."
bench setup requirements --apps sa7ba_custom

print_status "Running database migrations..."
bench migrate

print_status "Building assets..."
bench build

print_status "Setting up initial data..."
bench --site $1 execute sa7ba_custom.sa7ba_custom.setup_data.delivery_areas.setup_initial_data

print_status "Clearing cache..."
bench --site $1 clear-cache

print_status "Starting services..."
bench start

print_status "Verifying installation..."

# Check if Delivery Area doctype exists
if bench --site $1 frappe doctype exists "Delivery Area" > /dev/null 2>&1; then
    print_status "✓ Delivery Area doctype created successfully"
else
    print_error "✗ Delivery Area doctype not found"
fi

# Check if delivery areas exist
area_count=$(bench --site $1 frappe db count "Delivery Area" 2>/dev/null || echo "0")
if [ "$area_count" -gt "0" ]; then
    print_status "✓ $area_count delivery areas created successfully"
else
    print_warning "⚠ No delivery areas found - please run setup script manually"
fi

# Check if delivery charge item exists
if bench --site $1 frappe db exists "Item" "DELIVERY-CHARGE" > /dev/null 2>&1; then
    print_status "✓ Delivery charge item created successfully"
else
    print_warning "⚠ Delivery charge item not found - please run setup script manually"
fi

print_status "🎉 SA7BA Custom App deployment completed successfully!"
print_status ""
print_status "Next steps:"
print_status "1. Verify guest checkout functionality on your website"
print_status "2. Test delivery area selection and charge calculation"
print_status "3. Monitor the Delivery Charges Summary report"
print_status "4. Configure email templates for guest order confirmations"
print_status ""
print_status "For support, contact: dev@sa7ba.com"
