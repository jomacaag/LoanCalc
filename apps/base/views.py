from django.shortcuts import render
from .models import Loan


def home(request):
    loans = Loan.objects.all()
    return render(request, 'home.html')

def calculator(request):
    return render(request, 'base/calculator.html')
