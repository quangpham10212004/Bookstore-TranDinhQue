from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Book, Review
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import Customer

def home_view(request):
    # CategoryService.getAllCategories()
    categories = Category.objects.all()
    
    # BookService.getFeaturedBooks()
    # We'll treat the most recent books as featured
    featured_books = Book.objects.order_by('-id')[:8]
    
    # UserRecommendation.RecommendedBook logic
    recommendations = []
    if request.user.is_authenticated:
        # Simple recommendation: books in categories user has reviewed
        customer, _ = Customer.objects.get_or_create(member=request.user)
        reviewed_categories = Category.objects.filter(bookcategory__book__reviews__customer=customer).distinct()
        if reviewed_categories:
            recommendations = Book.objects.filter(categories__in=reviewed_categories).exclude(reviews__customer=customer).distinct()[:4]

    context = {
        'categories': categories,
        'featured_books': featured_books,
        'recommendations': recommendations,
    }
    return render(request, 'home.html', context)

def book_detail_view(request, book_id):
    # BookController.getBookDetail(bookId)
    book = get_object_or_404(Book, id=book_id)
    reviews = book.reviews.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    # Related books (recommendations based on category)
    related_books = Book.objects.filter(categories__in=book.categories.all()).exclude(id=book.id).distinct()[:4]

    context = {
        'book': book,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'related_books': related_books,
    }
    return render(request, 'catalog/book_detail.html', context)

@login_required
def add_review_view(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        customer, _ = Customer.objects.get_or_create(member=request.user)
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '')
        
        Review.objects.create(
            customer=customer,
            book=book,
            rating=rating,
            comment=comment
        )
        messages.success(request, "Review submitted successfully!")
    return redirect('book_detail', book_id=book_id)

def category_books_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    books = Book.objects.filter(categories=category)
    return render(request, 'catalog/category_books.html', {'category': category, 'books': books})
