#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import matplotlib.pyplot as plt
import networkx as nx

#Question 6.1
def enlever_elem(nom):
    """Fonction enlevant les éléments indésirable dans les noms des acteurs
    
    Parametres:
        nom: nom de l'acteur
    """
    elem = "[']"
    for x in range(len(elem)):
        nom = nom.replace(elem[x],"")
    v = nom.split("|")
    nom = v[-1]
    return nom


def convertisseur(fichier):
    """Fonction renvoyant le Graph à partir d'un fichier texte

    Parametres:
        fichier : un fichier .txt
    """
    G = nx.Graph() # Création du graph
    fic = open(fichier,'r',encoding = "utf-8") # Lecture du fichier text
    for lignes in fic: # Parcour du fichier par ligne
        dico = json.loads(lignes) # Initialisation automatique du dictionnaire à partir des données du fichier pour chaque film
        for i in range (len(dico["cast"])): # Parcours du dictionnaire des acteurs 
            dico["cast"][i] = enlever_elem(dico["cast"][i]) # Remplace le nom des acteurs et les remets au propre
            if dico["cast"][i] not in G: # S'il n'est pas déjà dans le Graph, le mettre
                G.add_node(dico["cast"][i],label='A')
        
        for acteur1 in dico["cast"]: # Pour chaque acteur former un lien entre eux dans le Graph pour signifier qu'ils ont travaillé ensemble 
            for acteur2 in dico["cast"]:
                if (acteur1,acteur2) not in G and acteur1 != acteur2:
                    G.add_edge(acteur1,acteur2)
    
    nx.draw(G,with_labels = True) # Dessiner puis afficher graph
    plt.show()
    return G 

print(convertisseur("données/data_100.txt"))

#Question 6.2
def collab_commun(acteur1, acteur2,fichier):
    """Fonction renvoyant l'ensemble des acteurs ayant collaboré avec ces 2 acteurs placé en parametre'

    Parametres:
        acteur1 : un acteur
        acteur2 : un acteur
        fichier : un fichier .txt
    """
    # Initialisation de l'ensemble des collaborateurs
    collab = set()
    # Appel de la fonction convertisseur pour reprendre le Graph
    G = convertisseur(fichier)

    # Pour chaque acteur du graph s'il n'est pas égal aux 2 acteurs et qu'il a déjà travaillé avec ces 2 acteurs, on l'ajouterai à l'ensemble
    for acteur in G.nodes:
        if acteur != acteur1 and acteur != acteur2:
            if (acteur1,acteur) in G.edges and (acteur2,acteur) in G.edges:
                collab.add(acteur)
    return collab

#Question 6.3
# Fonction donnée
def collaborateurs_proches(G,u,k):
    """Fonction renvoyant l'ensemble des acteurs à distance au plus k de l'acteur u dans le graphe G. La fonction renvoie None si u est absent du graphe.
    
    Parametres:
        G: le graphe
        u: le sommet de départ
        k: la distance depuis u
    """
    if u not in G.nodes:
        print(u,"est un illustre inconnu")
        return None
    collaborateurs = set()
    collaborateurs.add(u)
    print(collaborateurs)
    for i in range(k):
        collaborateurs_directs = set()
        for c in collaborateurs:
            for voisin in G.adj[c]:
                if voisin not in collaborateurs:
                    collaborateurs_directs.add(voisin)
        collaborateurs = collaborateurs.union(collaborateurs_directs)
    return collaborateurs

def collaborateurs_proches(acteur_dep,acteur_fin,fichier):
    """Fonction renvoyant la distance entre 2 acteurs.
    
    Parametres:
        acteur_dep : le sommet de départ
        acteur_fin : le somemt de fin
        fichier : un fichier .txt
    """
    # Appel de la fonction convertisseur pour reprendre le Graph
    G = convertisseur(fichier)

    #si l'acteur placé en parametre n'est pas dans le graph return None
    if acteur_dep not in G.nodes:
        print(acteur_dep,"est un illustre inconnu")
        return None
    
    # Initialisation de l'ensemble des collaborateurs 
    collaborateurs = set()
    # On ajoute dans l'ensemble l'acteur de départ
    collaborateurs.add(acteur_dep)
    # Inialisation d'un compteur pour calculer la distance entre ces 2 acteurs
    count = 0

    # Tant que l'acteur de fin n'est pas dans l'ensemble des collaborateurs, parcourir en largeur le graph
    while acteur_fin not in collaborateurs:
        # Initialisation d'un testeur d'action pour vérifier que nous ne sommes pas dans une boucle infini
        test = False 
        
        # Inialisationd d'un nouvel ensemble des collaborateurs direct pour chaque tour de boucle
        collaborateurs_directs = set()

        # Parcours de chaque collaborateurs
        for c in collaborateurs:
            # Parcours de tout les voisins des collaborateurs 
            for voisin in G.adj[c]:
        # On ajoute ces voisins à l'ensemble des collaborateurs s'ils ne sont pas déjà dedans et on ajoute 1 au compteur 
                if voisin not in collaborateurs:
                    collaborateurs_directs.add(voisin)
                    test = True
        count +=1
        collaborateurs = collaborateurs.union(collaborateurs_directs)
        if test == False :
            print (acteur_dep, " et ", acteur_fin," n'ont aucune connexions.")
            return None

    return count

#Question 6.4
def central(acteur,fichier):
    """Fonction renvoyant la valeur de centralité d'un acteur

    Parametres:
        acteur : nom de l'acteur dont on veut la centralité
        fichier : un fichier .txt
    """
    # Appel de la fonction convertisseur pour reprendre le Graph
    G = convertisseur(fichier)

    # Initialisation d'un dictionnaire de la centralisation de chaque acteur
    dico = nx.centrality.betweenness.betweenness_centrality(G)


    for nom, value in dico.items():
        if acteur == nom:
            return value
    return 0



def pluscentral(fichier):
    """Fonction renvoyant l'acteur a la plus haute centralité

    Parametres:
        fichier : un fichier .txt
    """
    # Appel de la fonction convertisseur pour reprendre le Graph
    G = convertisseur(fichier)
    # l'acteur avec la valeur max de centralité
    valmax=0
    actmax=""

    # Boucle for cherchant la valeur max de centralité et renvoyant l'acteur avec la plus haute valeur de centralité
    for acteur in G.nodes:
        if central(acteur,fichier) > valmax:
            valmax=central(acteur,fichier)
            actmax=acteur
    return actmax

#Question 6.5
def pluseloigne(fichier):
    """Fonction renvoyant le couple d'acteur/actrice le plus éloigné
    Parametres:
        fichier : un fichier .txt
    """
    # Appel de la fonction convertisseur pour reprendre le Graph
    G = convertisseur(fichier)
    # la distance qui sera la plus éloigné et leurs acteurs
    distmax = 0
    actmax=("","")

    # Parcours de toutes les arrètes du Graph
    for (acteur1,acteur2) in G.edges:
        if collaborateurs_proches(acteur1,acteur2,fichier)>distmax:
            distmax=collaborateurs_proches(acteur1,acteur2,fichier)
            actmax=(acteur1,acteur2)
    return actmax

