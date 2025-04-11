from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

# Sample book data for demonstration
BOOKS = [
    {'id': 1, 'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'publication': 'J.B. Lippincott & Co.', 'price': 10},
    {'id': 2, 'title': '1984', 'author': 'George Orwell', 'publication': 'Secker & Warburg', 'price': 15},
    {'id': 3, 'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'publication': 'Charles Scribner\'s Sons', 'price': 12},
    {'id': 4, 'title': 'Pride and Prejudice', 'author': 'Jane Austen', 'publication': 'T. Egerton', 'price': 8},
    {'id': 5, 'title': 'Moby-Dick', 'author': 'Herman Melville', 'publication': 'Harper & Brothers', 'price': 18},
]

def book_list(request):
    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}
    request.session['cart'] = cart  # Ensure cart is always a dictionary
    logger.debug(f"Cart data sent to template: {cart}")
    return render(request, 'store/book_list.html', {'books': BOOKS, 'cart': cart})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('book_list')
        else:
            return HttpResponse('Invalid login credentials')
    return render(request, 'store/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def add_to_cart(request, book_id):
    logger.debug(f"Book ID received: {book_id}")
    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}
    book_id_str = str(book_id)  # Convert book_id to string
    if book_id_str in cart:
        cart[book_id_str] += 1
    else:
        cart[book_id_str] = 1
    request.session['cart'] = cart  # Save updated cart
    request.session.modified = True  # Mark session as modified
    logger.debug(f"Updated cart: {cart}")
    return redirect('book_list')

@login_required
def cart_list(request):
    cart = request.session.get('cart', {})
    cart_books = [
        {
            'book': book,
            'quantity': cart.get(str(book['id']), 0)  # Convert book ID to string
        }
        for book in BOOKS if str(book['id']) in cart
    ]
    logger.debug(f"Session cart data: {cart}")
    logger.debug(f"Books in cart sent to template: {cart_books}")
    return render(request, 'store/cart_list.html', {'cart_books': cart_books})

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('book_list')
        else:
            return render(request, 'store/signup.html', {'error': 'Username already exists'})
    return render(request, 'store/signup.html')

@login_required
def debug_cart(request):
    cart = request.session.get('cart', {})
    cart_books = [
        {
            'book': book,
            'quantity': cart.get(book['id'], 0)
        }
        for book in BOOKS if book['id'] in cart
    ]
    return JsonResponse({'cart': cart, 'cart_books': cart_books})

@login_required
def update_cart_quantity(request, book_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        if quantity > 0:
            cart[str(book_id)] = quantity
        else:
            cart.pop(str(book_id), None)
        request.session['cart'] = cart
    return redirect('cart_list')

@login_required
def delete_from_cart(request, book_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        cart.pop(str(book_id), None)
        request.session['cart'] = cart
    return redirect('cart_list')
