# gpt4_ecommerce/gpt4_ecommerce/views.py
from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = 'home.html'
