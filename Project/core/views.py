from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages

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

    paginator = Paginator(publications, 4)  # Show 10 publications per page
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


def logout(request):
    if request.session['utilisateur_id']:
        del request.session['utilisateur_id']
        return redirect('login')
    else:
        return redirect('login')



def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            utilisateur = Utilisateur.objects.get(email=email, mot_de_passe=password)
            request.session['utilisateur_id'] = utilisateur.id
            return redirect('profile')
        except Utilisateur.DoesNotExist:
            messages.error(request, 'Invalid email or password')
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        email = request.POST['email']
        password = request.POST['password']
        nationalite = request.POST['nationalite']
        type = 'chercheur'
        utilisateur = Utilisateur(nom=nom, prenom=prenom, email=email, mot_de_passe=password, nationalite=nationalite, type=type)
        utilisateur.save()
        return redirect('login')
    return render(request, 'signup.html')

def profile_view(request):
    utilisateur_id = request.session.get('utilisateur_id')
    if utilisateur_id:
        utilisateur = Utilisateur.objects.get(id=utilisateur_id)
        publications = Publication.objects.filter(auteur=utilisateur)
        return render(request, 'profile.html', {'user': utilisateur, 'publications': publications})
    return redirect('login')


def update_profile(request):
    if request.method == 'POST':
        utilisateur_id = request.session.get('utilisateur_id')
        if utilisateur_id:
            user = get_object_or_404(Utilisateur, id=utilisateur_id)
            user.nom = request.POST['nom']
            user.prenom = request.POST['prenom']
            user.email = request.POST['email']
            user.nationalite = request.POST['nationalite']
            if request.FILES.get('image'):
                user.image = request.FILES['image']
            if request.POST.get('password'):
                user.mot_de_passe = request.POST['password']  # Ensure to hash the password
            user.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    return redirect('profile')



def add_publication(request):
    if request.method == 'POST':
        titre = request.POST['titre']
        resume = request.POST['resume']
        fichier_pdf = request.FILES.get('fichier_pdf')
        image = request.FILES.get('image')
        thematiques_ids = request.POST.getlist('thematiques')
        utilisateur_id = request.session.get('utilisateur_id')
        auteur = Utilisateur.objects.get(id=utilisateur_id)

        publication = Publication(
            titre=titre,
            resume=resume,
            fichier_pdf=fichier_pdf,
            image=image,
            auteur=auteur
        )
        publication.save()
        publication.thematiques.set(thematiques_ids)
        publication.save()
        
        messages.success(request, 'Publication added successfully.')
        return redirect('profile')
    
    thematiques = Thematique.objects.all()
    return render(request, 'add_publication.html', {'thematiques': thematiques})

def update_publication(request, publication_id):
    publication = get_object_or_404(Publication, id=publication_id)
    
    if request.method == 'POST':
        # Update publication details
        publication.titre = request.POST['titre']
        publication.resume = request.POST['resume']
        # Update other fields as needed
        publication.save()
        messages.success(request, 'Publication updated successfully.')
        return redirect('profile')
    thematiques = Thematique.objects.all()
    return render(request, 'update_publication.html', {'publication': publication,'thematiques':thematiques})

def delete_publication(request, publication_id):
    publication = get_object_or_404(Publication, id=publication_id)
    
    if request.method == 'POST':
        # Delete publication
        publication.delete()
        messages.success(request, 'Publication deleted successfully.')
        return redirect('profile')
    
    return render(request, 'delete_publication.html', {'publication': publication})
