from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def booking(request):
    return render(request, 'booking/booking_page.html')


def select_seat(request, showtime_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'status': 'error', 'message': 'User not logged in'})

    if request.method == 'POST':
        seat_id = request.POST.get('seat_id')

        if is_seat_available(showtime_id, seat_id):
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO booking (ShowtimeID, SeatID, Statut) VALUES (%s, %s, 'booked')",
                               [showtime_id, seat_id])

            user_email = get_user_email(user_id)

            if user_email:
                subject = 'Booking Confirmation'
                message = f'Thank you for booking a ticket! Your seat number is {seat_id}.'
                from_email = 'your@gmail.com'
                recipient_list = [user_email]
                html_message = render_to_string('booking/ticket_template.html', {'seat_number': seat_id})
                plain_message = strip_tags(html_message)
                send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)

            return JsonResponse({'status': 'success'})

        return JsonResponse({'status': 'error', 'message': 'Seat not available'})

    return render(request, 'booking/select_seat.html', {'showtime_id': showtime_id})


def is_seat_available(showtime_id, seat_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM booking WHERE ShowtimeID = %s AND SeatID = %s", [showtime_id, seat_id])
        count = cursor.fetchone()[0]

    return count == 0


def get_user_email(user_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT email FROM user WHERE UserID = %s", [user_id])
        result = cursor.fetchone()
        user_email = result[0] if result else None

    return user_email
