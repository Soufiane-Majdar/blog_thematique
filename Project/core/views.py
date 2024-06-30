from django.shortcuts import render, redirect
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator

def home(request):
    query = request.GET.get('q')
    categorie = request.GET.get('categorie')
    page_number = request.GET.get('page', 1)

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

    paginator = Paginator(publications, 10)  # Show 10 publications per page
    page_obj = paginator.get_page(page_number)

    context = {
        'publications': page_obj,
        'thematiques': thematiques
    }
    return render(request, 'home.html', context)

def about(request, id):
    publication = Publication.objects.get(id=id)
    thematiques = Thematique.objects.all()

    if request.method == "POST":
        contenu = request.POST.get('contenu')
        utilisateur_id = request.POST.get('utilisateur_id')  # Assuming you are getting the user ID from the form

        if contenu and utilisateur_id:
            utilisateur = Utilisateur.objects.get(id=utilisateur_id)
            Commentaire.objects.create(contenu=contenu, publication=publication, utilisateur=utilisateur)

            return redirect('about', id=id)

    commentaires = Commentaire.objects.filter(publication=publication)

    context = {
        'publication': publication,
        'thematiques': thematiques,
        'commentaires': commentaires
    }
    return render(request, 'about.html', context)
