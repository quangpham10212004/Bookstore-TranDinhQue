from django.contrib import admin
from .models import Author, Publisher, Category, Book, BookAuthor, BookCategory, BookEdition, BookFormat, BookImage, BookTag, BookTagMap, BookLanguage, BookLanguageMap, Review

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'stock')

admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Category)
admin.site.register(BookAuthor)
admin.site.register(BookCategory)
admin.site.register(BookEdition)
admin.site.register(BookFormat)
admin.site.register(BookImage)
admin.site.register(BookTag)
admin.site.register(BookTagMap)
admin.site.register(BookLanguage)
admin.site.register(BookLanguageMap)
admin.site.register(Review)
