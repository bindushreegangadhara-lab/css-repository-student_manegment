from django.shortcuts import render, redirect
from .models import Expense
from django.db.models import Sum

def home(request):
    expenses = Expense.objects.all().order_by('-date')

    # Calculate daily and monthly totals
    from django.utils.timezone import now
    today = now().date()
    daily_total = Expense.objects.filter(date=today).aggregate(Sum('amount'))['amount__sum'] or 0
    monthly_total = Expense.objects.filter(date__month=today.month).aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'expenses': expenses,
        'daily_total': daily_total,
        'monthly_total': monthly_total,
    }
    return render(request, 'expenses/home.html', context)

def add_expense(request):
    if request.method == 'POST':
        title = request.POST['title']
        amount = float(request.POST['amount'])
        category = request.POST['category']
        date = request.POST['date']
        Expense.objects.create(title=title, amount=amount, category=category, date=date)
        return redirect('home')
    return render(request, 'expenses/add_expense.html')
