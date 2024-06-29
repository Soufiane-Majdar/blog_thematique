from django.contrib import admin
from .models import Utilisateur, Thematique, Publication, Commentaire, Statistique, Chercheur, Admin

@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'nationalite', 'type', 'date_de_creation')
    search_fields = ('nom', 'prenom', 'email', 'nationalite')
    list_filter = ('type', 'date_de_creation')
    ordering = ('-date_de_creation',)

@admin.register(Thematique)
class ThematiqueAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)
    ordering = ('nom',)

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'date_de_publication')
    search_fields = ('titre', 'auteur__nom', 'auteur__prenom')
    list_filter = ('date_de_publication', 'thematiques')
    ordering = ('-date_de_publication',)
    filter_horizontal = ('thematiques',)

@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('publication', 'utilisateur', 'date')
    search_fields = ('publication__titre', 'utilisateur__nom', 'utilisateur__prenom')
    list_filter = ('date',)
    ordering = ('-date',)

@admin.register(Statistique)
class StatistiqueAdmin(admin.ModelAdmin):
    list_display = ('type', 'valeur', 'date', 'utilisateur')
    search_fields = ('type', 'utilisateur__nom', 'utilisateur__prenom')
    list_filter = ('type', 'date')
    ordering = ('-date',)

@admin.register(Chercheur)
class ChercheurAdmin(admin.ModelAdmin):
    list_display = ('utilisateur',)
    search_fields = ('utilisateur__nom', 'utilisateur__prenom')
    ordering = ('utilisateur__nom',)

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('utilisateur',)
    search_fields = ('utilisateur__nom', 'utilisateur__prenom')
    ordering = ('utilisateur__nom',)
