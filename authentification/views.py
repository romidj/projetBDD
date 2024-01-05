from django.shortcuts import render
from django.http import HttpResponse
from django.db import connections
from django.db import connection
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from typing import TypedDict, Any


def landing(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM WeeklyMovies")
        movies = cursor.fetchall()

    return render(request, 'landing.html', {'movies': movies})


def signin(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        lastName = request.POST.get('lastName', '')
        userName = request.POST.get('userName', '')
        phoneNumber = request.POST.get('phoneNumber', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        passwordConfirm = request.POST.get('passwordConfirm', '')

        if password != passwordConfirm:
            return render(request, 'authentification/signin.html', {'error': 'Passwords do not match'})
        hashed_password = make_password(password)
        query = f"INSERT INTO user (Username, email, password, role, phoneNumber) VALUES ('{name} {lastName}', '{email}', '{hashed_password}', 'customer', '{phoneNumber}')"

        try:
            with connections['default'].cursor() as cursor:
                cursor.execute(query)
            return redirect('authentification/landing.html')

        except Exception as e:
            # Handle database error
            print(f"Error: {e}")

    return render(request, 'authentification/signin.html')


class UserDict(TypedDict):
    id: int
    username: str
    role: str


def login(request, user_id):
    if request.method == 'POST':
        request.session['user_id'] = user_id
        username = request.POST['username']
        password = request.POST['password']
        with connection.cursor() as cursor:
            cursor.execute("SELECT UserID, username, role FROM user WHERE username = %s AND password = %s",
                           [username, password])
            user_data = cursor.fetchone()

        if user_data:

            user: UserDict = {
                'id': user_data[0],
                'username': user_data[1],
                'role': user_data[2],  # type: ignore[attr-defined]
            }

            login(request, user)

            if user.role == 'adminn':
                return redirect('admin_dashboard')
            elif user.role == 'customer':
                return redirect('customer_dashboard')
        else:
            # Handle invalid login credentials
            return render(request, 'authentification/login.html', {'error_message': 'Invalid login credentials'})

    return render(request, 'authentification/login.html')


def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']

    return redirect('landing.html')
