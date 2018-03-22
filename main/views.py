from django.shortcuts import render
from django.views import  View

# Create your views here.

class Main(View):

    def get(self, request):
        context = {
        }
        return render(request, 'main/index.html', context=context)
