# home/urls.py

from django.urls import path
from .views import (homepage, 
                    book_entries, 
                    edit_entry, 
                    delete_entry,
                    export_book,
                    master_index,
                    export_master,
                    symbols,
                    planner)

app_name = 'home'
urlpatterns = [
    path('', homepage, name='homepage'),
    path('entries/', book_entries, name='book_entries'),
    path(
        'entries/<int:entry_id>/edit/',
        edit_entry,
        name='edit_entry'
    ),
    path(
        'entries/<int:entry_id>/delete/',
        delete_entry,
        name='delete_entry'
    ),
    path(
        'entries/book/',
        export_book,
        name='export_book'
    ),
    path(
        'entries/master',
        master_index,
        name='master_index'
    ),
    path(
        'entries/export_master',
        export_master,
        name='export_master'
    ),
    path(
        'symbols/',
        symbols,
        name='symbols'
    ),
    path(
        'planner/',
        planner,
        name='planner'
    )
]
