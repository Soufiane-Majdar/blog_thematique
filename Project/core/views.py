from django.shortcuts import render
from .models import *
from django.db.models import Q


def home(request):
    query = request.GET.get('q')
    categorie = request.GET.get('categorie')

    publications = Publication.objects.all()
    thematiques = Thematique.objects.all()

    if query:
        publications = publications.filter(
            Q(titre__icontains=query) |
            Q(auteur__nom__icontains=query) |
            Q(auteur__prenom__icontains=query) |
            Q(resume__icontains=query)
        ).distinct()

    if categorie:
        publications = publications.filter(thematiques__nom__exact=categorie)

    context = {
        'publications': publications,
        'thematiques':thematiques

    }
    return render(request, 'home.html', context)


def about(request,id):
    publication = Publication.objects.get(id=id)
    thematiques = Thematique.objects.all()

    context = {
        'publication': publication,
        'thematiques':thematiques
    }
    return render(request, 'about.html',context)