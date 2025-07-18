# home/urls.py

from django.urls import path
from .views import (homepage, 
                    book_entries, 
                    edit_entry, 
                    delete_entry,
                    export_to_csv,
                    export_master_csv,
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
        'entries/export/',
        export_to_csv,
        name='export_to_csv'
    ),
    path(
        'entries/master',
        export_master_csv,
        name='export_master_csv'
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
