# views.py

from django.shortcuts import render, redirect
from django.db import connection


def movie_detail(request, movie_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Movie WHERE MovieID = %s", [movie_id])
        movie = cursor.fetchone()

        cursor.execute("SELECT * FROM Review WHERE MovieID = %s", [movie_id])
        reviews = cursor.fetchall()

    return render(request, 'movie_detail.html', {'movie': movie, 'reviews': reviews})


def add_review(request, movie_id):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Review (UserID, MovieID, Rating, Comment, ReviewDate) VALUES (%s, %s, %s, %s, NOW())",
                [user_id, movie_id, rating, comment]
            )

    return redirect('movie_detail', movie_id=movie_id)
