#!/usr/bin/env python
import os
import sys
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

BOOKS = [
    {'id': 1, 'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'price': 10, 'publication': 'J.B. Lippincott & Co.'},
    {'id': 2, 'title': '1984', 'author': 'George Orwell', 'price': 15, 'publication': 'Secker & Warburg'},
    {'id': 3, 'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'price': 12, 'publication': "Charles Scribner's Sons"},
]

@login_required
def cart_list(request):
    cart = request.session.get('cart', {})
    cart_books = [
        {
            'book': book,
            'quantity': cart.get(str(book['id']), 0)
        }
        for book in BOOKS if str(book['id']) in cart
    ]
    return render(request, 'store/cart_list.html', {'cart_books': cart_books})

@login_required
def remove_from_cart(request, book_id):
    cart = request.session.get('cart', {})
    if str(book_id) in cart:
        cart[str(book_id)] -= 1
        if cart[str(book_id)] <= 0:
            del cart[str(book_id)]
    request.session['cart'] = cart
    return redirect('cart_list')

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
