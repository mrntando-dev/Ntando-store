# app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
from datetime import datetime
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Sample data for services
SERVICES = {
    'domains': {
        'title': 'Premium Domains',
        'description': 'Get the perfect domain name for your business',
        'icon': '🌐',
        'features': ['Memorable names', 'SEO-friendly', 'Instant transfer', 'Secure ownership'],
        'details': 'Stand out with a premium domain name that represents your brand perfectly. Our curated collection includes short, memorable domains that boost credibility and SEO rankings.'
    },
    'apps': {
        'title': 'Premium Apps',
        'description': 'Professional mobile and web applications',
        'icon': '📱',
        'features': ['Custom development', 'Cross-platform', 'Modern UI/UX', 'Full support'],
        'details': 'Transform your ideas into powerful applications. We develop custom mobile and web apps using the latest technologies, ensuring scalability, security, and exceptional user experience.'
    },
    'phone_numbers': {
        'title': 'Premium Phone Numbers',
        'description': 'Exclusive memorable phone numbers',
        'icon': '📞',
        'features': ['Easy to remember', 'Professional image', 'Instant activation', 'Multiple carriers'],
        'details': 'Enhance your business image with a premium phone number that customers will remember. Choose from vanity numbers, repeating digits, or sequential patterns.'
    },
    'uptime_monitoring': {
        'title': 'Uptime Robot Monitoring',
        'description': 'Monitor your bots and websites 24/7',
        'icon': '⚡',
        'features': ['Real-time alerts', 'Free & Premium plans', '99.9% uptime', 'Detailed reports'],
        'details': 'Never miss downtime again. Our advanced monitoring system checks your websites and bots every minute, sending instant alerts via email, SMS, or Slack when issues arise.'
    },
    'website_design': {
        'title': 'Premium Website Design',
        'description': 'Beautiful, responsive websites that convert',
        'icon': '💻',
        'features': ['Responsive design', 'SEO optimized', 'Fast loading', 'Modern layouts'],
        'details': 'Create a stunning online presence with our custom website design services. We craft beautiful, conversion-focused websites that work flawlessly across all devices.'
    },
    'hosting': {
        'title': 'Premium Hosting',
        'description': 'Fast, secure, and reliable hosting',
        'icon': '🚀',
        'features': ['99.9% uptime', 'SSD storage', 'Free SSL', '24/7 support'],
        'details': 'Host your website on lightning-fast servers with guaranteed uptime. Enjoy free SSL certificates, daily backups, and expert support whenever you need it.'
    },
    'updates': {
        'title': 'Premium Updates',
        'description': 'Keep your systems current and secure',
        'icon': '🔄',
        'features': ['Regular updates', 'Security patches', 'Feature additions', 'Priority support'],
        'details': 'Stay ahead with regular updates and maintenance. We ensure your software stays secure, fast, and equipped with the latest features.'
    },
    'whatsapp_bot': {
        'title': 'Premium WhatsApp Bot',
        'description': 'Automate your WhatsApp business',
        'icon': '💬',
        'features': ['Auto-replies', 'Customer support', 'Broadcast messages', 'Analytics'],
        'details': 'Automate customer interactions on WhatsApp with intelligent bots. Handle inquiries, send promotions, and provide 24/7 support to boost customer satisfaction.'
    },
    'business_cards': {
        'title': 'Business Cards Design & Print',
        'description': 'Professional business cards that stand out',
        'icon': '🎨',
        'features': ['Custom designs', 'High-quality print', 'Fast delivery', 'Multiple finishes'],
        'details': 'Make a lasting first impression with professionally designed business cards. Choose from various finishes including matte, glossy, embossed, and metallic options.'
    }
}

PRICING = {
    'domains': [
        {'name': 'Basic Domain', 'price': '$99', 'period': 'one-time', 'features': ['.com or .net extension', 'Free WHOIS privacy', '1-year registration', 'Email support']},
        {'name': 'Premium Domain', 'price': '$499', 'period': 'one-time', 'features': ['Short memorable name', 'Free WHOIS privacy', '2-year registration', 'Priority support', 'Free logo design']},
        {'name': 'Elite Domain', 'price': '$2,999+', 'period': 'one-time', 'features': ['Ultra-premium names', 'Complete privacy', 'Lifetime support', 'Brand consultation', 'Marketing package']}
    ],
    'apps': [
        {'name': 'Basic App', 'price': '$999', 'period': 'one-time', 'features': ['Up to 5 screens', 'Basic features', 'Android or iOS', '3 months support', 'Source code']},
        {'name': 'Professional App', 'price': '$2,999', 'period': 'one-time', 'features': ['Up to 15 screens', 'Advanced features', 'Android & iOS', '6 months support', 'Backend included', 'Admin panel']},
        {'name': 'Enterprise App', 'price': '$9,999+', 'period': 'one-time', 'features': ['Unlimited screens', 'Custom features', 'Multi-platform', '12 months support', 'Full backend', 'API integration', 'White-label option']}
    ],
    'phone_numbers': [
        {'name': 'Basic Number', 'price': '$49', 'period': '/month', 'features': ['Local numbers', 'Call forwarding', 'Voicemail', 'Basic support']},
        {'name': 'Premium Number', 'price': '$199', 'period': '/month', 'features': ['Vanity numbers', 'Advanced routing', 'Call recording', 'SMS included', 'Priority support']},
        {'name': 'Elite Number', 'price': '$999+', 'period': '/month', 'features': ['Ultra-premium numbers', 'All features included', 'Dedicated support', 'Custom integration']}
    ],
    'uptime_monitoring': [
        {'name': 'Free Plan', 'price': '$0', 'period': '/month', 'monitors': '5 monitors', 'features': ['5-minute checks', 'Email alerts', 'Basic reporting', '50 SMS alerts/month']},
        {'name': 'Starter', 'price': '$9.99', 'period': '/month', 'monitors': '20 monitors', 'features': ['1-minute checks', 'Email & SMS alerts', 'Advanced reporting', '500 SMS alerts/month', 'Status page']},
        {'name': 'Pro', 'price': '$29.99', 'period': '/month', 'monitors': '100 monitors', 'features': ['30-second checks', 'All alert types', 'Custom reporting', 'Unlimited SMS alerts', 'Priority support', 'API access']},
        {'name': 'Business', 'price': '$99.99', 'period': '/month', 'monitors': 'Unlimited', 'features': ['10-second checks', 'White-label option', 'Custom integrations', 'Dedicated support', 'SLA guarantee', 'Team collaboration']}
    ],
    'hosting': [
        {'name': 'Starter', 'price': '$9.99', 'period': '/month', 'features': ['10 GB SSD storage', '100 GB bandwidth', '5 websites', 'Free SSL', 'Daily backups', 'Email support']},
        {'name': 'Professional', 'price': '$29.99', 'period': '/month', 'features': ['50 GB SSD storage', 'Unlimited bandwidth', '25 websites', 'Free SSL', 'Hourly backups', 'Priority support', 'CDN included']},
        {'name': 'Business', 'price': '$79.99', 'period': '/month', 'features': ['200 GB SSD storage', 'Unlimited bandwidth', 'Unlimited websites', 'Free SSL', 'Real-time backups', '24/7 phone support', 'Dedicated IP', 'Advanced security']}
    ],
    'website_design': [
        {'name': 'Landing Page', 'price': '$499', 'period': 'one-time', 'features': ['1 page design', 'Mobile responsive', 'Contact form', 'SEO basics', '2 revisions']},
        {'name': 'Business Website', 'price': '$1,999', 'period': 'one-time', 'features': ['Up to 10 pages', 'Custom design', 'CMS integration', 'Advanced SEO', '4 revisions', '3 months support']},
        {'name': 'E-commerce', 'price': '$4,999+', 'period': 'one-time', 'features': ['Unlimited pages', 'Custom e-commerce', 'Payment gateway', 'Product management', 'Unlimited revisions', '12 months support']}
    ],
    'whatsapp_bot': [
        {'name': 'Basic Bot', 'price': '$299', 'period': '/month', 'features': ['Auto-replies', 'Up to 1000 chats/month', 'Basic analytics', 'Email support']},
        {'name': 'Pro Bot', 'price': '$699', 'period': '/month', 'features': ['Advanced AI', 'Up to 10000 chats/month', 'Detailed analytics', 'Custom integrations', 'Priority support']},
        {'name': 'Enterprise Bot', 'price': '$1,999+', 'period': '/month', 'features': ['Custom AI training', 'Unlimited chats', 'Advanced features', 'API access', 'Dedicated support', 'White-label option']}
    ],
    'business_cards': [
        {'name': 'Standard', 'price': '$49', 'period': 'per 100 cards', 'features': ['Standard paper', 'Single-sided', 'Basic design', '3-5 day delivery']},
        {'name': 'Premium', 'price': '$99', 'period': 'per 100 cards', 'features': ['Premium paper', 'Double-sided', 'Custom design', 'Matte/Glossy finish', '2-3 day delivery']},
        {'name': 'Luxury', 'price': '$299', 'period': 'per 100 cards', 'features': ['Luxury stock', 'Special finishes', 'Embossing/Foil', 'Unique shapes', 'Rush delivery', 'Designer consultation']}
    ]
}

# Testimonials
TESTIMONIALS = [
    {
        'name': 'John Davis',
        'company': 'Tech Startup Inc',
        'text': 'Ntandomods delivered an exceptional website that exceeded our expectations. Their attention to detail and professionalism is unmatched.',
        'rating': 5,
        'service': 'Website Design'
    },
    {
        'name': 'Sarah Johnson',
        'company': 'Marketing Pro',
        'text': 'The premium domain we purchased has significantly boosted our brand credibility. Great investment!',
        'rating': 5,
        'service': 'Premium Domains'
    },
    {
        'name': 'Michael Chen',
        'company': 'E-commerce Solutions',
        'text': 'Their hosting service is incredibly fast and reliable. We\'ve experienced zero downtime since switching.',
        'rating': 5,
        'service': 'Premium Hosting'
    }
]

# FAQ
FAQ = [
    {
        'question': 'How long does it take to deliver a service?',
        'answer': 'Delivery time varies by service. Domains transfer instantly, websites take 2-4 weeks, and apps take 4-12 weeks depending on complexity.'
    },
    {
        'question': 'Do you offer refunds?',
        'answer': 'Yes, we offer a 30-day money-back guarantee on most services. Contact us for specific terms.'
    },
    {
        'question': 'Can I upgrade my plan later?',
        'answer': 'Absolutely! You can upgrade your plan at any time. We\'ll prorate the charges accordingly.'
    },
    {
        'question': 'What payment methods do you accept?',
        'answer': 'We accept credit cards, PayPal, bank transfers, and cryptocurrency for your convenience.'
    },
    {
        'question': 'Do you provide ongoing support?',
        'answer': 'Yes, all our services include support. Premium plans get priority support with faster response times.'
    }
]

@app.context_processor
def inject_globals():
    """Make variables available to all templates"""
    return {
        'current_year': datetime.now().year,
        'site_name': 'Ntandomods',
        'contact_email': 'info@ntandomods.com',
        'contact_phone': '+1 (555) 123-4567'
    }

@app.route('/')
def index():
    """Homepage"""
    featured_services = {k: v for k, v in list(SERVICES.items())[:6]}
    return render_template('index.html', 
                         services=featured_services, 
                         testimonials=TESTIMONIALS[:3])

@app.route('/services')
def services():
    """All services page"""
    return render_template('services.html', services=SERVICES)

@app.route('/service/<service_id>')
def service_detail(service_id):
    """Individual service detail page"""
    if service_id not in SERVICES:
        flash('Service not found', 'error')
        return redirect(url_for('services'))
    
    service = SERVICES[service_id]
    pricing = PRICING.get(service_id, [])
    related_services = {k: v for k, v in SERVICES.items() if k != service_id}
    related_services = dict(list(related_services.items())[:3])
    
    return render_template('service_detail.html', 
                         service=service, 
                         service_id=service_id, 
                         pricing=pricing,
                         related_services=related_services)

@app.route('/pricing')
def pricing():
    """Pricing page"""
    return render_template('pricing.html', pricing=PRICING, services=SERVICES)

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html', testimonials=TESTIMONIALS)

@app.route('/faq')
def faq():
    """FAQ page"""
    return render_template('faq.html', faq=FAQ)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with form"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        service = request.form.get('service')
        message = request.form.get('message')
        
        # Validate form data
        if not all([name, email, service, message]):
            flash('Please fill in all required fields', 'error')
            return render_template('contact.html', success=False)
        
        # In production, save to database and send email
        # For now, just log it
        contact_data = {
            'name': name,
            'email': email,
            'phone': phone,
            'service': service,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"New contact form submission: {json.dumps(contact_data, indent=2)}")
        
        flash('Thank you for contacting us! We\'ll get back to you within 24 hours.', 'success')
        return render_template('contact.html', success=True)
    
    return render_template('contact.html', success=False)

@app.route('/api/quote', methods=['POST'])
def get_quote():
    """API endpoint for quote requests"""
    try:
        data = request.json
        service = data.get('service')
        
        if not service:
            return jsonify({'success': False, 'message': 'Service is required'}), 400
        
        # In production, process the quote request
        quote_data = {
            'service': service,
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"Quote request: {json.dumps(quote_data, indent=2)}")
        
        return jsonify({
            'success': True, 
            'message': 'Quote request received! We will contact you soon.'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/newsletter', methods=['POST'])
def subscribe_newsletter():
    """API endpoint for newsletter subscription"""
    try:
        data = request.json
        email = data.get('email')
        
        if not email:
            return jsonify({'success': False, 'message': 'Email is required'}), 400
        
        # In production, save to database
        print(f"Newsletter subscription: {email}")
        
        return jsonify({
            'success': True, 
            'message': 'Thank you for subscribing to our newsletter!'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 error page"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Custom 500 error page"""
    return render_template('500.html'), 500

@app.route('/sitemap.xml')
def sitemap():
    """Generate sitemap"""
    from flask import Response
    
    pages = []
    # Add all routes
    pages.append({'loc': url_for('index', _external=True), 'priority': '1.0'})
    pages.append({'loc': url_for('services', _external=True), 'priority': '0.9'})
    pages.append({'loc': url_for('pricing', _external=True), 'priority': '0.9'})
    pages.append({'loc': url_for('about', _external=True), 'priority': '0.8'})
    pages.append({'loc': url_for('contact', _external=True), 'priority': '0.8'})
    pages.append({'loc': url_for('faq', _external=True), 'priority': '0.7'})
    
    # Add service pages
    for service_id in SERVICES.keys():
        pages.append({
            'loc': url_for('service_detail', service_id=service_id, _external=True),
            'priority': '0.8'
        })
    
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for page in pages:
        sitemap_xml += '  <url>\n'
        sitemap_xml += f'    <loc>{page["loc"]}</loc>\n'
        sitemap_xml += f'    <priority>{page["priority"]}</priority>\n'
        sitemap_xml += '  </url>\n'
    
    sitemap_xml += '</urlset>'
    
    return Response(sitemap_xml, mimetype='application/xml')

@app.route('/robots.txt')
def robots():
    """Generate robots.txt"""
    from flask import Response
    
    robots_txt = """User-agent: *
Allow: /
Sitemap: {sitemap_url}
""".format(sitemap_url=url_for('sitemap', _external=True))
    
    return Response(robots_txt, mimetype='text/plain')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
