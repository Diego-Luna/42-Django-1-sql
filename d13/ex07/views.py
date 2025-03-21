from django.shortcuts import render
from django.shortcuts import HttpResponse
from .addTable import TableValue, ErrorInDatabase
from .models import Movies

# Create your views here.
def populate(request):
    data = [
        TableValue(
            episode_nb= 1,
            title= "The Phantom Menace",
            director= "George Lucas",
            producer= "Rick McCallum",
            release_date= "1999-05-19",
        ),
        TableValue(
            episode_nb= 2,
            title= "Attack of the Clones",
            director= "George Lucas",
            producer= "Rick McCallum",
            release_date= "2002-05-16",
        ),
        TableValue(
            episode_nb= 3,
            title= "Revenge of the Sith",
            director= "George Lucas",
            producer= "Rick McCallum",
            release_date= "2005-05-19",
        ),
        TableValue(
            episode_nb= 4,
            title= "A New Hope",
            director= "George Lucas",
            producer= "Gary Kurtz, Rick McCallum",
            release_date= "1977-05-25",
        ),
        TableValue(
            episode_nb= 5,
            title= "The Empire Strikes Back",
            director= "Irvin Kershner",
            producer= "Gary Kutz, Rick McCallum",
            release_date= "1980-05-17",
        ),
        TableValue(
        
            episode_nb= 6,
            title= "Return of the Jedi",
            director= "Richard Marquand",
            producer= "Howard G. Kazanjian, George Lucas, Rick McCallum",
            release_date= "1983-05-25",
        ),
        TableValue(
            episode_nb= 7,
            title= "The Force Awakens",
            director= "J.J. Abrams",
            producer= "Kathleen Kennedy, J.J. Abrams, Bryan Burk",
            release_date= "2015-12-11",
        )
    ]
    returnValue = ""
    for value in data:
        try:
            value.save()
            returnValue += "<br>OK"
        except ErrorInDatabase as e:
            returnValue += "<br> Error: {}".format(e)


    return HttpResponse(returnValue)


def display(request):
    try:
        test = Movies.objects.all()
        print("test: ")
        print(len(test))
        if len(test) == 0:
            return HttpResponse("No data available")
        result = "<table border='1' colspan='6'>"
        result += """<tr>
    <td>Title</td>
    <td>episode_nb</td>
    <td>opening_crawl</td>
    <td>director</td>
    <td>producer</td>
    <td>release_date</td>
    <td>created</td>
    <td>updated</td>
  </tr>"""
        for row in test:
            result += "<tr>"
            result += "<td>{}</td>".format(row.title)
            result += "<td>{}</td>".format(row.episode_nb)
            result += "<td>{}</td>".format(row.opening_crawl)
            result += "<td>{}</td>".format(row.director)
            result += "<td>{}</td>".format(row.producer)
            result += "<td>{}</td>".format(row.release_date)
            result += "<td>{}</td>".format(row.created)
            result += "<td>{}</td>".format(row.updated)
            result += "</tr>"
        result += "</table>"

        return HttpResponse(result)
    except Exception as e:
        return HttpResponse("No data available")


def update(request):
    try:
        # * Si se envió el formulario
        if request.method == 'POST' and 'update' in request.POST:
            title = request.POST.get('title')
            opening_crawl = request.POST.get('opening_crawl')
            if title:
                movie = Movies.objects.get(title=title)
                movie.opening_crawl = opening_crawl
                movie.save()
        
        # ! Obtener todas las películas para el menú desplegable
        movies = Movies.objects.all().order_by('episode_nb')
        
        if not movies:
            return HttpResponse("No data available")
        
        return render(request, 'ex07_update.html', {'movies': movies})
    except Exception as e:
        return HttpResponse("No data available")