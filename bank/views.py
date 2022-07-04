import datetime
import decimal
from datetime import datetime

import schedule
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from pytz import UTC

from .forms import Payment
from .models import customer


def process_payment(request):
    global payor, payee
    if request.method == 'POST':

        form = Payment(request.POST)

        if form.is_valid():
            x = form.cleaned_data['payor']
            y = form.cleaned_data['payee']
            z = decimal.Decimal(form.cleaned_data['amount'])
            PaymentDateTime = form.cleaned_data['split_date_time_field']
            if PaymentDateTime:
                now = datetime.utcnow().replace(tzinfo=UTC)
                sec = PaymentDateTime - now
                # hour_format = str(PaymentDateTime.hour) + ":" + str(PaymentDateTime.minute)
                # week_day = (calendar.day_name[PaymentDateTime.weekday()]).lower().strip('\"')
                sec = (PaymentDateTime.timestamp() - now.timestamp())

                if customer.objects.filter(name=x).exists() and customer.objects.filter(name=y).exists():
                    schedule.every(int(sec.seconds)).seconds.do(job, x, y, z)  # seconds
                    messages.success(request, 'Congratulations, Transaction Successful...!')
                    schedule.every().sunday.at("22:22").do(job, x, y, 100)  # weekday
                    all_jobs = schedule.get_jobs()
                    print(all_jobs)
                    return HttpResponseRedirect('/')
                else:
                    messages.warning(request, 'Invalid Information, Transaction Failed...!')  # recorded
                    return HttpResponseRedirect('/')
            else:
                if customer.objects.filter(name=x).exists() and customer.objects.filter(name=y).exists():
                    job(x, y, z)
                    messages.success(request, 'Congratulations, Transaction Successful...!')  # ignored

                    return HttpResponseRedirect('/')
                else:
                    messages.warning(request, 'Invalid Information, Transaction Failed...!')  # recorded
                    return HttpResponseRedirect('/')
        else:
            print("Invalid")
    else:
        form = Payment()
    return render(request, 'index.html', {'form': form})


def job(x, y, z):
    print(x, y, z)
    # payor = customer.objects.select_for_update().get(name=x)
    # payee = customer.objects.select_for_update().get(name=y)
    # with transaction.atomic():
    #     payor.balance -= z
    #     payor.save()
    #     payee.balance += z
    #     payee.save()
    #     print("successfull")
