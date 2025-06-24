from datetime import datetime
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: str = None,
) -> Order:
    user = User.objects.get(username=username)

    if date:
        parsed_date = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order = Order(user=user)
        order.created_at = parsed_date
        order.save()
    else:
        order = Order.objects.create(user=user)

    for ticket_data in tickets:
        movie_session = MovieSession.objects.get(
            id=ticket_data["movie_session"]
        )
        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )

    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    else:
        return Order.objects.all()
