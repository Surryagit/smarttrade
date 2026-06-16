from django.shortcuts import render

def login_page(request):
    return render(request, 'login.html')

def dashboard_page(request):
    return render(request, 'dashboard.html')

def portfolio_page(request):
    return render(request, 'portfolio.html')

def analytics_page(request):
    return render(request, 'analytics.html')