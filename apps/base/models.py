from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE





# Create your models here.
class Loan(models.Model):
    name = models.CharField(max_length=250)
    rate_choices = [
        ('hourly', 'Hourly'),
        ('weekly', 'Weekly'),
        ('biweekly', 'Biweekly'),
        ('monthly', 'Monthly'),
        ('salary', 'Salary')
    ] 
    loanType=[
        ('FHA','FHA'),
        ('Conventional','Conventional')
    ]
    #user who created loan query
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    #income per hr, month, salary etc etc.
    income = models.DecimalField(max_digits=10, decimal_places=2)
    #income rate eg(hr, biweekly, monthly etc etc.)
    income_rate = models.CharField(choices = rate_choices, max_length=100)
    #(monthy debts, credit cards, laons, installments)
    debts = models.DecimalField(max_digits=10, decimal_places=2)
    #downpayment percentageon house
    down_payment = models.DecimalField(max_digits=10, decimal_places=2)
    #FHA CONVENTIONAL USDA
    loan_type = models.CharField(choices= loanType , max_length=100)
    #monthly mortgage insurance
    mi= models.DecimalField(max_digits=10, decimal_places=2)
    #upfront mi
    Upfront_Mi = models.DecimalField(max_digits=10, decimal_places=2)
    #property taxes based on location
    taxes = models.DecimalField(max_digits=10, decimal_places=2)
    #any HOA or Condo Fees
    condo_fee_hoa = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Condo Fee/HOA'
    )
    #hazard insurance/flood insurance if required
    insurance = models.DecimalField(max_digits=10, decimal_places=2)
    #length of loan, in months, 360 for 30 years etc.
    term = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name