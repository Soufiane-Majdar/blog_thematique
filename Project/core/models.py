from django.db import models


class Utilisateur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    nationalite = models.CharField(max_length=100,blank=True)
    mot_de_passe = models.CharField(max_length=100)
    date_de_creation = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='Utilisateur/', blank=True)
    TYPE_CHOICES = [
        ('chercheur', 'Chercheur'),
        ('admin', 'Admin'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.nom} {self.prenom}"


class Thematique(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Publication(models.Model):
    titre = models.CharField(max_length=200)
    auteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    resume = models.TextField()
    fichier_pdf = models.FileField(upload_to='publications/')
    image = models.ImageField(upload_to='publications_imgs/', blank=True)
    date_de_publication = models.DateTimeField(auto_now_add=True)
    thematiques = models.ManyToManyField(Thematique)

    def __str__(self):
        return self.titre


class Commentaire(models.Model):
    contenu = models.TextField()
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.utilisateur} on {self.publication}"


class Statistique(models.Model):
    TYPE_CHOICES = [
        ('vue', 'Vue'),
        ('like', 'Like'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    valeur = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.type} - {self.valeur} by {self.utilisateur}"



class Chercheur(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    def __str__(self):
        return f"Chercheur: {self.utilisateur}"


class Admin(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)

    def __str__(self):
        return f"Admin: {self.utilisateur}"
