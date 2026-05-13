from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Movie
from .forms import MovieForm

class MovieListView(LoginRequiredMixin, ListView):
    model = Movie
    template_name = 'movies/movie_list.html'
    context_object_name = 'movies'

    def get_queryset(self):
        queryset = Movie.objects.filter(owner=self.request.user).order_by('-created_at')
        status = self.request.GET.get('status')
        genre = self.request.GET.get('genre')
        if status:
            queryset = queryset.filter(status=status)
        if genre:
            queryset = queryset.filter(genre=genre)
        return queryset

class MovieCreateView(LoginRequiredMixin, CreateView):
    model = Movie
    form_class = MovieForm
    template_name = 'movies/movie_form.html'
    success_url = reverse_lazy('movie-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class MovieUpdateView(LoginRequiredMixin, UpdateView):
    model = Movie
    form_class = MovieForm
    template_name = 'movies/movie_form.html'
    success_url = reverse_lazy('movie-list')

    def get_queryset(self):
        return Movie.objects.filter(owner=self.request.user)

class MovieDeleteView(LoginRequiredMixin, DeleteView):
    model = Movie
    template_name = 'movies/movie_confirm_delete.html'
    success_url = reverse_lazy('movie-list')

    def get_queryset(self):
        return Movie.objects.filter(owner=self.request.user)

class SignupView(FormView):
    template_name = 'registration/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('movie-list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
