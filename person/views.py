import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from .models import Customer
from django.contrib.auth.models import User


# Form customer searching
def search_customer_by_phone(request):
    fragment = request.GET.get('phone', '')
    customers = (Customer.objects
          .filter(phone__icontains=fragment)
          .values('id', 'name', 'surname', 'phone', 'email', 'address')[:5])
    return JsonResponse(list(customers), safe=False)

# Searching the customer id of curently logged user
@login_required
def get_customer_id(request):
    try:
        customer = Customer.objects.get(email=request.user.email)
        return JsonResponse({'customer_id': customer.id})
    except Customer.DoesNotExist:
        return JsonResponse({'customer_id': None})

# Customer credentials edit
@require_POST
def update_customer(request):
    data = json.loads(request.body)
    try:
        c = Customer.objects.get(pk=data['id'])
        c.name = data['name']
        c.surname = data['surname']
        c.email = data['email']
        c.address = data['address']
        c.save()
        return JsonResponse({'success': True})
    except:
        return JsonResponse({'success': False})

# Customer profile
@login_required
def profile(request):
    user = request.user
    customer = None

    try:
        customer = Customer.objects.get(email=user.email)
    except Customer.DoesNotExist:
        pass

    return render(request, 'user_profile.html', {
        'user':     user,
        'customer': customer,
    })



# Profile editation with validation on the user side
@login_required
@require_http_methods(["GET", "POST"])
def edit_profile(request):
    try:
        customer = Customer.objects.get(email=request.user.email)
    except Customer.DoesNotExist:
        return redirect('profile')

    errors = {}
    
    values = {
        'username': request.user.username,
        'email': request.user.email,
        'name': customer.name,
        'surname': customer.surname,
        'birthdays': customer.birthdays or '',
        'phone': customer.phone,
        'address': customer.address,
        'newsletters': customer.newsletters,
    }

    if request.method == "POST":
        username = request.POST.get('username','').strip()
        email = request.POST.get('email','').strip()
        name = request.POST.get('name','').strip()
        surname = request.POST.get('surname','').strip()
        birthdays = request.POST.get('birthdays') or None
        phone = request.POST.get('phone','').strip()
        address = request.POST.get('address','').strip()
        newsletters = 'newsletters' in request.POST

        values.update({
            'username': username,
            'email': email,
            'name': name,
            'surname': surname,
            'birthdays': birthdays or '',
            'phone': phone,
            'address': address,
            'newsletters': newsletters,
        })

        if not username:
            errors['username'] = "Uživatelské jméno je povinné."
        elif (User.objects
              .exclude(pk=request.user.pk)
              .filter(username=username)
              .exists()):
            errors['username'] = "Toto uživatelské jméno už existuje."

        if not email:
            errors['email'] = "Email je povinný."

        if not name:
            errors['name'] = "Jméno je povinné."
        if not surname:
            errors['surname'] = "Příjmení je povinné."
        if not phone:
            errors['phone'] = "Telefon je povinný."
        if not address:
            errors['address'] = "Adresa je povinná."

        if not errors:
            user = request.user
            user.username = username
            user.email = email
            user.save()
            customer.name        = name
            customer.surname     = surname
            customer.birthdays   = birthdays
            customer.email       = email
            customer.phone       = phone
            customer.address     = address
            customer.newsletters = newsletters
            customer.save()

            return redirect('profile')

    return render(request, 'edit_profile.html', {
        'errors': errors,
        'values': values,
    })


# Login
@require_http_methods(["GET", "POST"])
def login(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('home')
        context['error'] = "Neplatné uživatelské jméno nebo heslo."
    return render(request, 'login.html', context)


# Logout
@login_required
@require_GET
def logout(request):
    auth_logout(request)
    return redirect('login')


# Registration
@require_http_methods(["GET", "POST"])
def register(request):
    errors = {}
    values = {
        'username': '',
        'name': '',
        'surname': '',
        'birthdays': '',
        'email': '',
        'phone': '',
        'address': '',
        'newsletters': False,
    }

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        name = request.POST.get('name', '').strip()
        surname = request.POST.get('surname', '').strip()
        birthdays = request.POST.get('birthdays', '') or None
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        newsletters = request.POST.get('newsletters') == 'on'

        values.update({
            'username': username,
            'name': name,
            'surname': surname,
            'birthdays': birthdays or '',
            'email': email,
            'phone': phone,
            'address': address,
            'newsletters': newsletters,
        })

        if not username:
            errors['username'] = "Uživatelské jméno je povinné."
        elif User.objects.filter(username=username).exists():
            errors['username'] = "Toto uživatelské jméno již existuje."

        if not password1:
            errors['password1'] = "Heslo je povinné."
        elif password1 != password2:
            errors['password2'] = "Hesla se neshodují."
        elif len(password1) < 8:
            errors['password1'] = "Heslo musí mít alespoň 8 znaků."

        if not name:
            errors['name'] = "Jméno je povinné."
        if not surname:
            errors['surname'] = "Příjmení je povinné."
        if not email:
            errors['email'] = "Email je povinný."
        if not phone:
            errors['phone'] = "Telefon je povinný."
        if not address:
            errors['address'] = "Adresa je povinná."

        if not errors:
            user = User.objects.create_user(
                username=username,
                password=password1,
                email=email,
            )

            Customer.objects.create(
                name=name,
                surname=surname,
                birthdays=birthdays,
                email=email,
                phone=phone,
                address=address,
                newsletters=newsletters,
            )

            auth_login(request, user)
            return redirect('profile')


    return render(request, 'register.html', {
        'errors': errors,
        'values': values,
    })
