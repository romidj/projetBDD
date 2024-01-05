from django.shortcuts import render, redirect
from django.db import connections
from django.db import connection


def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')


def add_movie(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        release_date = request.POST.get('release_date')

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO movies (title, description, release_date) VALUES (%s, %s, %s)",
                [title, description, release_date]
            )

        return redirect('admin_dashboard')

    return render(request, 'admin/add_movie.html')


def remove_movie(request, movie_id):
    with connection.cursor() as cursor:

        cursor.execute("DELETE FROM movies WHERE MovieID = %s", [movie_id])

    return redirect('admin_dashboard')


def remove_user(request, user_id):
    with connection.cursor() as cursor:

        cursor.execute("DELETE FROM user WHERE UserID = %s", [user_id])

    return redirect('admin_dashboard')
