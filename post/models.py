from django.db import models
from django.utils import timezone


class BeforeAfter(models.Model):
    """Model to store before and after photos"""
    title = models.CharField(max_length=200, blank=True, help_text="Optional title for this before/after")
    before_image = models.ImageField(upload_to='before_after/before/', help_text="Before photo")
    after_image = models.ImageField(upload_to='before_after/after/', help_text="After photo")
    description = models.TextField(blank=True, help_text="Optional description")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, help_text="Show this before/after on the website")
    order = models.IntegerField(default=0, help_text="Order for display (lower numbers appear first)")

    class Meta:
        verbose_name = "Before & After"
        verbose_name_plural = "Before & After"
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title if self.title else f"Before & After #{self.id}"





class Testimonial(models.Model):
    """Customer testimonial with star rating."""

    STAR_CHOICES = [(i, str(i)) for i in range(1, 6)]

    name = models.CharField(max_length=120)
    rating = models.PositiveSmallIntegerField(choices=STAR_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.rating}★)"


class ContactForm(models.Model):
    """Contact form submissions"""
    
    SERVICE_CHOICES = [
        ('mowing', 'Mowing'),
        ('edging', 'Edging'),
        ('weeding', 'Weeding'),
        ('trimming', 'Trimming'),
        ('cleanup', 'Clean Up'),
        ('mulch', 'Mulch'),
        ('irrigation', 'Irrigation'),
        ('patios', 'Patios'),
        ('christmas_lights', 'Christmas Lights'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Form"
        verbose_name_plural = "Contact Forms"
    
    def __str__(self):
        return f"{self.name} - {self.get_service_type_display()} ({self.created_at.strftime('%Y-%m-%d')})"


class Portfolio(models.Model):
    """Model to store portfolio projects"""
    title = models.CharField(max_length=200, help_text="Project title")
    photo = models.ImageField(upload_to='portfolio/', help_text="Project photo")
    description = models.TextField(blank=True, help_text="Optional project description")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, help_text="Show this project on the website")
    order = models.IntegerField(default=0, help_text="Order for display (lower numbers appear first)")

    class Meta:
        verbose_name = "Portfolio Project"
        verbose_name_plural = "Portfolio Projects"
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title