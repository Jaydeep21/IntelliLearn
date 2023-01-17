import json

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users
from .models import *


# Views and endpoints
def home(request):
    context_dict = {}
    return render(request, template_name='home.html', context=context_dict)


@unauthenticated_user
def sign_up(request, plan_subscribed=''):
    if request.method == 'POST':
        data = json.loads(request.body)
        first_name = data['first_name']
        last_name = data['last_name']
        college_name = data['college_name']
        email_id = data['email_id']
        password1 = data['password']
        phone_no = data['phone_no']
        card_no = data['card_no']
        card_cvv = data['card_cvv']
        plan_subscribed = data['plan_subscribed']

        # Process payment
        # This is just dummy code because I am not going to implement any actual
        # payment processing for this project
        pay_status_failed = False
        if pay_status_failed:
            return redirect(payment_failed)

        try:
            # register the User
            new_user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email_id,
                username=email_id,
            )
            new_user.set_password(password1)
            new_user.save()

            # Add this user to collegeadmin group
            collegeadmin_group = Group.objects.get(name='collegeadmin')
            collegeadmin_group.user_set.add(new_user)

            # get the plan_subscribed object
            plan = Plan.objects.get(name=plan_subscribed)
            plan.save()

            # register the User as College
            college = College.objects.create(
                user=new_user,
                plan_subscribed=plan,
                first_name=first_name,
                last_name=last_name,
                college_name=college_name,
                email=email_id,
                phone_no=phone_no,
                card_info=card_no,
            )
            college.save()

            # now at last the College as Customer
            customer = Customer.objects.create(
                user=new_user,
                plan_subscribed=plan,
                first_name=first_name,
                last_name=last_name,
                college_name=college_name,
                email=email_id,
                phone_no=phone_no,
            )
            customer.save()

            # Now log the user in
            auth_user = authenticate(request, username=email_id, password=password1)
            if auth_user is not None:
                login(request, auth_user)
                return redirect(college_page)
            else:
                return JsonResponse({'process': 'failed', 'error': 'User authentication system failed'})
        except IntegrityError:
            return JsonResponse({'process': 'failed', 'error': 'User already exists'})
        except Exception as err:
            return JsonResponse({'process': 'failed', 'error': f'{str(err)}'})
    plans = Plan.objects.all().values_list('name', flat=True)
    if plan_subscribed not in plans:
        return render(request, template_name='home.html')
    cost_of_selected_plan = Plan.objects.get(name=plan_subscribed).price_per_year
    context_dict = {'plan_selected': plan_subscribed, 'plan_cost': f'₹{int(cost_of_selected_plan)} / year'}
    return render(request, template_name='sign_up.html', context=context_dict)


@unauthenticated_user
def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('email')  # username and email are one and the same
        password = request.POST.get('password')
        try:
            # Log the user in
            auth_user = authenticate(request, username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect(college_page)
            else:
                if User.objects.filter(username=username).exists():
                    context_dict = {'msg': 'Email id or password is wrong'}
                    return render(request, template_name='sign_in.html', context=context_dict)
                else:
                    context_dict = {'msg': 'User does not exist please sign up first'}
                    return render(request, template_name='sign_in.html', context=context_dict)
        except Exception as e:
            context_dict = {'msg': 'Email id or password is wrong'}
            return render(request, template_name='sign_in.html', context=context_dict)
    context_dict = {}
    return render(request, template_name='sign_in.html', context=context_dict)


def sign_out(request):
    # sign out logic here
    logout(request)
    context_dict = {'msg': 'Logged out successfully'}
    return render(request, template_name='sign_in.html', context=context_dict)


def checkout_page(request):
    context_dict = {}
    return render(request, template_name='checkout/checkbout.html', context=context_dict)


@login_required
@allowed_users(allowed_roles=['sybadmin'])
def syb_admin_page(request):
    context_dict = {}
    return render(request, template_name='sybadmin/dashboard/dashboard.html', context=context_dict)


@login_required
@allowed_users(allowed_roles=['collegeadmin'])
def college_page(request):
    context_dict = {'new_user': True}
    return render(request, template_name='college/admin/college_admin.html', context=context_dict)


@login_required
@allowed_users(allowed_roles=['collegeadmin'])
def college_add_teachers(request):
    context_dict = {}
    return render(request, template_name='college/admin/admin_addteachers.html', context=context_dict)


@login_required
@allowed_users(allowed_roles=['collegeadmin'])
def college_add_classes(request):
    departments_list = [department['name'] for department in Department.objects.all().values('name')]
    if request.method == 'POST':
        # process request
        data = json.loads(request.body)
        form_type = data['form_type']
        if form_type == 'department':
            # this means that the request came from add new department form
            department_name = data['department_name']
            college = request.user.college
            try:
                Department.objects.get_or_create(
                    college=college,
                    name=department_name,
                )
                return JsonResponse({
                    'process': 'success',
                    'msg': f'Success! {department_name} department added to the database.',
                    'departments_list': departments_list,
                })
            except IntegrityError:
                return JsonResponse({'process': 'failed', 'msg': f'{department_name} already exists.'})
            except Exception as err:
                return JsonResponse({'process': 'failed', 'msg': f'{err}'})
    context_dict = {
        'departments_list': departments_list,
    }
    return render(request, template_name='college/admin/admin_addclasses.html', context=context_dict)


@login_required
@allowed_users(allowed_roles=['teacher'])
def college_teacher(request):
    context_dict = {}
    return render(request, template_name='college/teacher/teacher.html', context=context_dict)


@login_required
@allowed_users(allowed_roles=['student'])
def college_student(request):
    context_dict = {}
    return render(request, template_name='college/student/student.html', context=context_dict)


def payment_failed(request):
    return render(request, template_name='payment_failed.html')
