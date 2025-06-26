# home/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from .models import Book, IndexEntry
import csv

def homepage(request):
    """
    Handle adding Books and IndexEntries; persist selected book in session.
    """
    # Persist selected book from GET
    book_id = request.GET.get('book_id')
    if book_id:
        request.session['selected_book_id'] = book_id

    if request.method == 'POST':
        # New‐book form submitted
        if 'title' in request.POST:
            title = request.POST.get('title', '').strip()
            if title:
                Book.objects.create(title=title)

        # New‐entry form submitted (comma-split terms)
        elif 'page' in request.POST:
            # Fix typo: use correct session key
            book_id = request.session.get('selected_book_id')
            page_str = request.POST.get('page', '')
            term_str = request.POST.get('terms', '').strip()
            description = request.POST.get('description', '').strip()

            # Only proceed if valid data
            if book_id and page_str.isdigit() and term_str:
                try:
                    book = Book.objects.get(pk=book_id)
                    page = int(page_str)
                    # Split comma-separated terms
                    terms = [t.strip() for t in term_str.split(',') if t.strip()]
                    # Create one entry per term
                    for term in terms:
                        IndexEntry.objects.create(
                            book=book,
                            page=page,
                            term=term,
                            description=description
                        )
                    request.session['last_terms_str'] = term_str
                except Book.DoesNotExist:
                    pass

        # Redirect to clear POST data (session keeps selected_book_id)
        return redirect('home:homepage')

    # GET: build context
    books = Book.objects.all()
    context = {'books': books}

    last = request.session.pop('last_terms_str', None)
    if last:
        context['last_terms_str'] = last

    selected_id = request.session.get('selected_book_id')
    if selected_id:
        try:
            context['selected_book'] = Book.objects.get(pk=selected_id)
        except Book.DoesNotExist:
            context['selected_book'] = None

    # Add the 5 most recent entries
    context['recent_entries'] = (
        IndexEntry.objects
                  .select_related('book')
                  .order_by('-created_at')[:5]
    )

    return render(request, 'home/index.html', context)

def book_entries(request):
    """
    Display all index entries for a selected book, newest first.
    """
    books = Book.objects.all()
    book_id = request.GET.get('book_id')
    selected_book = None
    entries = []

    if book_id:
        try:
            selected_book = Book.objects.get(pk=book_id)
            # Newest entries first
            entries = (
                IndexEntry.objects
                          .filter(book=selected_book)
                          .order_by('-created_at')
            )
        except Book.DoesNotExist:
            selected_book = None

    return render(request, 'home/book_entries.html', {
        'books': books,
        'selected_book': selected_book,
        'entries': entries,
    })

def edit_entry(request, entry_id):
    """
    Edit a single IndexEntry; on POST saves and redirects back to its book.
    """
    entry = get_object_or_404(IndexEntry, pk=entry_id)

    if request.method == 'POST':
        page = request.POST.get('page')
        term = request.POST.get('term', '').strip()
        desc = request.POST.get('description', '').strip()

        if page and page.isdigit() and term and desc:
            entry.page = int(page)
            entry.term = term
            entry.description = desc
            entry.save()
            # build URL with query string, then redirect
            url = reverse('home:book_entries') + f'?book_id={entry.book.id}'
            return redirect(url)

    # GET → show edit form
    return render(request, 'home/edit_entry.html', {'entry': entry})

def delete_entry(request, entry_id):
    """
    Delete an IndexEntry (on POST) and always redirect back to its book page.
    """
    entry = get_object_or_404(IndexEntry, pk=entry_id)
    book_id = entry.book.id

    if request.method == 'POST':
        entry.delete()

    # Build URL: /entries/?book_id=<id>
    url = f"{reverse('home:book_entries')}?book_id={book_id}"
    return redirect(url)

def export_to_csv(request):
    book_id = request.GET.get('book_id')
    if request.GET.get("export") == "csv" and book_id:
        try:
            selected_book = Book.objects.get(pk=book_id)
            entries = IndexEntry.objects.filter(book=selected_book).order_by('-created_at')
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename=\"{selected_book.title}.csv"'
            writer = csv.writer(response)
            writer.writerow(['Page', 'Term', 'Description'])
            for e in entries:
                writer.writerow([e.page, e.term, e.description])
            return response
        
        except Book.DoesNotExist:
            pass
    
    return redirect(f"{reverse('home:book_entries')}?book_id={book_id}")

def symbols(request):
    return render(request, 'home/symbols.html')