# account/views.py
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect

from user.models import User
from front.forms import DeleteAccountForm
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def delete_account(request):
    form = DeleteAccountForm()
    error_message = ''
    if request.method == 'POST':
        form = DeleteAccountForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.filter(email=email).first()
            if user is not None and check_password(password, user.password):
                user.delete()
                return render(None, 'account_deleted.html')

            error_message = 'Yaroqsiz elektron pochta yoki parol. Iltimos, yana bir bor urinib ko\'ring.'

    return render(request, 'delete_account.html', {'form': form, 'error_message': error_message})
