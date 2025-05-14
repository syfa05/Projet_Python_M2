"""
Partie 1: Programmation Orienté Objet
"""


class article():
    def __init__(self,nom,prix,quantite):
        self.nom = nom
        self.prix = prix
        self.quantite = quantite
        quantite_stock = quantite


    def vendre_article(self,quantite_Commande):
        self.quantite_Commande = quantite_Commande
        if self.quantite < self.quantite_Commande:
            print("Le stock axctuel de l'article {self.nom} ne nous permet pas d'excecuter votre commande")
            print(f"Approvisionnement de l'article {self.nom} necessaire")
        else:
            self.quantite-=self.quantite_Commande
            print(f"Nous avons vendu: {self.quantite_Commande} {self.nom}")
            return self.quantite_Commande * self.prix

    def appro(self,quantite_Appro):
        self.quantite_Appro = quantite_Appro
        self.quantite+=self.quantite_Appro
        print(f"La quantité d'approvisionnement est de: {self.quantite_Appro}")

    def inventaire(self):
        print(f""" inventaire de l'article {self.nom}:
    Quantité en stock: {self.quantite}"
            """)

    def changer_prix(self,nouveau_prix):
        self.nouveau_prix = nouveau_prix
        self.prix = self.nouveau_prix
        print(f"Le nouveau prix de l'article {self.nom} est {self.nouveau_prix}$")



orange = article("Orange", 2, 100)
orange.vendre_article(10)
orange.vendre_article(4)
orange.vendre_article(60)
orange.vendre_article(18)
orange.appro(45)
orange.changer_prix(5)
orange.inventaire()

"""
Partie 2 : Le magasin
"""
class magasin():
    def __init__(self):
        self.articles =[]

    def ajoutee_article(self,article):
        self.articles.append(article)

    def afficher_stock(self):
        print("stock des articles dans le magasin:")
        for article in self.articles:
            print(f"{article.nom}: {article.quantite} unités, {article.prix}$ par unité ")

    def valeur_stock(self):
        print(f"La valeur  du stock est de: {sum(article.prix*article.quantite for article in self.articles)}$")

    def rechercher_articles(self,q): # q est une quantité seuil d'un article en stock
        print(f"Voici les article donc la quantité en stock est inferieeur au seuil {q}")
        for article in self.articles:
            if article.quantite<q:
                print(f"{article.nom}")



magasin_fruits = magasin()
magasin_fruits.ajoutee_article(article("tomate",4,20))
magasin_fruits.ajoutee_article(article("banane",1,30))
magasin_fruits.ajoutee_article(article("Pomme",2.45,100))
magasin_fruits.ajoutee_article(article("Pasteque",6.75,50))
magasin_fruits.afficher_stock()
magasin_fruits.valeur_stock()
magasin_fruits.rechercher_articles(40)