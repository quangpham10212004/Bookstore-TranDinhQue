from django.db import models
from users.models import Customer

class Author(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    def __str__(self):
        return self.name

class Category(models.Model):
    type = models.CharField(max_length=100)
    def __str__(self):
        return self.type

class Book(models.Model):
    title = models.CharField(max_length=255)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, null=True, blank=True)
    stock = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    authors = models.ManyToManyField(Author, through='BookAuthor')
    categories = models.ManyToManyField(Category, through='BookCategory')
    
    def __str__(self):
        return self.title

class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

class BookCategory(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class BookEdition(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    edition = models.CharField(max_length=50)

class BookFormat(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    format_type = models.CharField(max_length=50) # e.g., Hardcover, Paperback

class BookImage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    img_url = models.URLField()

class BookTag(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class BookTagMap(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    tag = models.ForeignKey(BookTag, on_delete=models.CASCADE)

class BookLanguage(models.Model):
    code = models.CharField(max_length=10) # e.g., en, vi
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class BookLanguageMap(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    language = models.ForeignKey(BookLanguage, on_delete=models.CASCADE)

class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
