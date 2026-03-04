from django.core.management.base import BaseCommand
from users.models import Member
from catalog.models import Author, Publisher, Category, Book, BookImage
import random

class Command(BaseCommand):
    help = 'Seeds initial data for the bookstore'

    def handle(self, *args, **kwargs):
        # Create superuser
        if not Member.objects.filter(username='admin').exists():
            Member.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write(self.style.SUCCESS('Created superuser: admin/admin'))

        # Create test customer
        if not Member.objects.filter(username='member').exists():
            Member.objects.create_user('member', 'member@example.com', 'member', role='customer')
            self.stdout.write(self.style.SUCCESS('Created test member: member/member'))

        # Seed Catalog
        authors = ['J.K. Rowling', 'J.R.R. Tolkien', 'George R.R. Martin', 'Isaac Asimov']
        pubs = ['Bloomsbury', 'HarperCollins', 'Bantam Spectra', 'Gnome Press']
        cats = ['Fantasy', 'Sci-Fi', 'Mystery', 'History']

        author_objs = [Author.objects.get_or_create(name=name)[0] for name in authors]
        pub_objs = [Publisher.objects.get_or_create(name=name)[0] for name in pubs]
        cat_objs = [Category.objects.get_or_create(type=name)[0] for name in cats]

        books_data = [
            ('Harry Potter and the Philosopher\'s Stone', 29.99),
            ('The Hobbit', 24.50),
            ('A Game of Thrones', 35.00),
            ('Foundation', 19.99),
            ('Harry Potter and the Chamber of Secrets', 29.99),
            ('The Silmarillion', 30.00),
            ('Dune', 22.00),
            ('I, Robot', 15.00),
        ]

        for title, price in books_data:
            book, created = Book.objects.get_or_create(
                title=title,
                defaults={
                    'price': price,
                    'stock': random.randint(10, 100),
                    'publisher': random.choice(pub_objs)
                }
            )
            if created:
                book.authors.add(random.choice(author_objs))
                book.categories.add(random.choice(cat_objs))
                # Add a placeholder image
                BookImage.objects.create(book=book, img_url=f"https://picsum.photos/seed/{book.id}/300/450")
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded catalog data'))
