from django.views.generic.base import TemplateView

class UI_Service(TemplateView):
    template_name = 'index.html'

class Chatbot_Service(TemplateView):
    template_name = 'chatbot/index.html'