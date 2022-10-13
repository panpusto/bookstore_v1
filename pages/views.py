# from django.shortcuts import render
# from django.views import View
from django.views.generic import TemplateView


# class HomePageView(View):
#     def get(self, request):
#         return render(request, 'home.html')

class HomePageView(TemplateView):
    template_name = "home.html"


class AboutPageView(TemplateView):
    template_name = "about.html"
