from django.shortcuts import render
from django.http import HttpResponse
from .models import Planets, People, Movies
from django.db.models import Q
import datetime

def index(request):
    # Get unique gender values for dropdown
    genders = People.objects.values_list('gender', flat=True).distinct().order_by('gender')
    genders = [g for g in genders if g is not None]
    
    if request.method == 'POST':
        # Get form data
        min_date = request.POST.get('min_date')
        max_date = request.POST.get('max_date')
        min_diameter = request.POST.get('min_diameter')
        gender = request.POST.get('gender')
        
        # Validate date formats
        try:
            min_date = datetime.datetime.strptime(min_date, '%Y-%m-%d').date()
            max_date = datetime.datetime.strptime(max_date, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return render(request, 'ex10_form.html', {
                'genders': genders,
                'error': 'Invalid date format. Please use YYYY-MM-DD.'
            })
        
        # Validate diameter
        try:
            min_diameter = int(min_diameter) if min_diameter else 0
        except ValueError:
            return render(request, 'ex10_form.html', {
                'genders': genders,
                'error': 'Invalid diameter. Please enter a number.'
            })
        
        # Query characters with the specified criteria
        results = []
        
        # Find people with the specified gender
        people = People.objects.filter(gender=gender, homeworld__diameter__gte=min_diameter)
        
        # Find movies released between the specified dates
        movies = Movies.objects.filter(release_date__gte=min_date, release_date__lte=max_date)
        
        # For each person, find their movies and add to results
        for person in people:
            person_movies = person.movies.filter(release_date__gte=min_date, release_date__lte=max_date)
            
            for movie in person_movies:
                results.append({
                    'movie_title': movie.title,
                    'character_name': person.name,
                    'gender': person.gender,
                    'homeworld_name': person.homeworld.name if person.homeworld else 'Unknown',
                    'homeworld_diameter': person.homeworld.diameter if person.homeworld else 'Unknown',
                })
        
        # Sort results by movie title and character name
        results.sort(key=lambda x: (x['movie_title'], x['character_name']))
        
        return render(request, 'ex10_results.html', {
            'results': results,
            'genders': genders,
            'min_date': min_date,
            'max_date': max_date,
            'min_diameter': min_diameter,
            'gender': gender,
        })
    
    # Default values for the form
    min_date = '1900-01-01'
    max_date = datetime.date.today().strftime('%Y-%m-%d')
    min_diameter = 0
    
    return render(request, 'ex10_form.html', {
        'genders': genders,
        'min_date': min_date,
        'max_date': max_date,
        'min_diameter': min_diameter,
    })