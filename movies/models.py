from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Movie(models.Model):
    STATUS_CHOICES = [
        ('to_watch', 'Хочу посмотреть'),
        ('watching', 'Смотрю'),
        ('watched', 'Посмотрел'),
    ]
    
    GENRE_CHOICES = [
        ('Action', 'Экшн'),
        ('Comedy', 'Комедия'),
        ('Drama', 'Драма'),
        ('Horror', 'Ужасы'),
        ('Sci-Fi', 'Научная фантастика'),
    ]

    title = models.CharField("Название", max_length=200)
    genre = models.CharField("Жанр", max_length=50, choices=GENRE_CHOICES)
    year = models.PositiveIntegerField("Год выпуска")
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='to_watch')
    rating = models.PositiveIntegerField("Оценка (1-10)", 
                                        validators=[MinValueValidator(1), MaxValueValidator(10)], 
                                        null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movies')

    def __str__(self):
        return self.title
