from django.contrib import admin
from .models import User, Author, Genre, Book, BorrowRequest, BookReview


admin.site.site_header = "Library Management Admin"
admin.site.site_title = "Library Management Admin Portal"
admin.site.index_title = "Welcome to the Library Management Admin Portal"

admin.site.register(User)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Book)   
admin.site.register(BorrowRequest)
admin.site.register(BookReview)

