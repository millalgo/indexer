from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)  # e.g. “SANS Course Book 1”
    color = models.CharField(                  # Hex code for color‐coding
        max_length=7,
        help_text="Hex color code, e.g. #FF0000"
    )

    def __str__(self):
        return self.title

class IndexEntry(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="entries"
    )
    page = models.PositiveIntegerField()       # Page number
    term = models.CharField(max_length=200)    # Indexed keyword
    description = models.TextField()           # Notes or definition
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["book", "page", "term"]    # Sort by book→page→term

    def __str__(self):
        return f"{self.term} (p.{self.page})"