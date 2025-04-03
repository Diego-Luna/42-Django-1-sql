from django.shortcuts import render, HttpResponse
from django.utils import timezone
from .models import Planets, People
import json
import os

def display(request):
    try:
        # Primero verificar todos los datos cargados
        all_planets = Planets.objects.all()
        all_people = People.objects.all()
        
        # Verificar específicamente planetas con clima windy
        windy_planets = Planets.objects.filter(climate__icontains='windy')
        
        # Verificar personas asignadas a planetas windy
        people_on_windy_planets = People.objects.filter(homeworld__in=windy_planets)
        
        # Para debuggear
        debug_info = f"""
        <h3>Información de depuración:</h3>
        <p>Total de planetas: {all_planets.count()}</p>
        <p>Total de personas: {all_people.count()}</p>
        <p>Planetas con clima 'windy': {windy_planets.count()}</p>
        <p>Personas en planetas 'windy': {people_on_windy_planets.count()}</p>
        """
        
        # La consulta original
        people = People.objects.filter(
            homeworld__climate__icontains='windy'
        ).order_by('name')
        
        # Si no hay personas en planetas windy pero hay otros datos
        if not people and all_people.exists():
            # Mostrar todos los datos disponibles como alternativa
            result = debug_info
            result += "<h3>No hay personas en planetas con clima 'windy'. Mostrando todos los datos:</h3>"
            
            result += "<table border='1'>"
            result += """<tr>
                <th>Name</th>
                <th>Homeworld</th>
                <th>Climate</th>
            </tr>"""
            
            for person in all_people:
                result += "<tr>"
                result += f"<td>{person.name}</td>"
                homeworld_name = person.homeworld.name if person.homeworld else "N/A"
                result += f"<td>{homeworld_name}</td>"
                climate = person.homeworld.climate if person.homeworld else "N/A"
                result += f"<td>{climate}</td>"
                result += "</tr>"
            
            result += "</table>"
            
            return HttpResponse(result)
        
        # Si no hay datos, mostrar instrucciones
        if not people:
            return HttpResponse("No data available")
        
        # Si hay personas en planetas windy, mostrar como se requiere
        result = "<table border='1'>"
        result += """<tr>
            <th>Name</th>
            <th>Homeworld</th>
            <th>Climate</th>
        </tr>"""
        
        for person in people:
            result += "<tr>"
            result += f"<td>{person.name}</td>"
            result += f"<td>{person.homeworld.name}</td>"
            result += f"<td>{person.homeworld.climate}</td>"
            result += "</tr>"
        
        result += "</table>"
        
        return HttpResponse(result)
    except Exception as e:
        # return HttpResponse(f"Error: {str(e)}")
        return HttpResponse("No data available")


