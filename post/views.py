from django.shortcuts import render
from .models import BeforeAfter, Testimonial, ContactForm, Portfolio
from django.shortcuts import redirect
from django.contrib import messages


  
def index(request):
    testimonial_errors = []
    testimonial_data = {'name': '', 'comment': '', 'rating': ''}
    contact_errors = []
    contact_data = {'name': '', 'phone': '', 'email': '', 'service_type': '', 'message': ''}
    contact_success = False

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'testimonial':
            name = request.POST.get('name', '').strip()
            rating = request.POST.get('rating')
            comment = request.POST.get('comment', '').strip()
            
            if not name:
                testimonial_errors.append('Name is required.')
            if not rating:
                testimonial_errors.append('Rating is required.')
            if not comment:
                testimonial_errors.append('Comment is required.')

        try:
            rating_value = int(rating) if rating else None
        except (TypeError, ValueError):
            rating_value = None
            testimonial_errors.append('Rating must be a number between 1 and 5.')

        if rating_value and not 1 <= rating_value <= 5:
            testimonial_errors.append('Rating must be between 1 and 5.')

        if not testimonial_errors:
            Testimonial.objects.create(
                name=name,
                rating=rating_value,
                comment=comment,
            )
            return redirect('index')
        
        elif form_type == 'contact':
            name = request.POST.get('name', '').strip()
            phone = request.POST.get('phone', '').strip()
            email = request.POST.get('email', '').strip()
            service_type = request.POST.get('service_type', '').strip()
            message = request.POST.get('message', '').strip()
            
            contact_data = {
                'name': name,
                'phone': phone,
                'email': email,
                'service_type': service_type,
                'message': message
            }
            
            if not name:
                contact_errors.append('Name is required.')
            if not phone:
                contact_errors.append('Phone number is required.')
            if not service_type:
                contact_errors.append('Please select a service type.')
            if not message:
                contact_errors.append('Please provide details about your project.')
            
            if not contact_errors:
                ContactForm.objects.create(
                    name=name,
                    phone=phone,
                    email=email if email else '',
                    service_type=service_type,
                    message=message,
                )
                contact_success = True
                contact_data = {'name': '', 'phone': '', 'email': '', 'service_type': '', 'message': ''}
                messages.success(request, 'Thank you! We will contact you soon.')

    before_after_items = (
        BeforeAfter.objects.filter(is_active=True)
        .order_by('order', '-created_at')
    )
    testimonials = Testimonial.objects.filter(is_published=True).order_by('-created_at')[:6]
    return render(
        request,
        'post/index.html',
        {
            'before_after_items': before_after_items,
            'testimonials': testimonials,
            'testimonial_errors': testimonial_errors,
            'testimonial_data': testimonial_data,
            'contact_errors': contact_errors,
            'contact_data': contact_data,
            'contact_success': contact_success,
        },
    )


def portfolio(request):
    """Display portfolio projects"""
    portfolio_projects = (
        Portfolio.objects.filter(is_active=True)
        .order_by('order', '-created_at')
    )
    return render(
        request,
        'post/portfolio.html',
        {
            'portfolio_projects': portfolio_projects,
        },
    )