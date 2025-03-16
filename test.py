def redondance_n(bin_str, n):
    """
    Applique une redondance d'ordre n à une chaîne binaire.
    
    bin_str : chaîne binaire d'entrée (ex: '0110')
    n       : ordre de redondance (ex: 3)
    
    Retourne la chaîne binaire redondée.
    """
    return ''.join([bit * n for bit in bin_str])

 

def entrelacer_bin(tableaux):
    """
    Entrelace des chaînes binaires ['1001', '1111', '0101']
    et retourne une liste de chaînes binaires ['110', '001', '011', '151']
    """
    # zip(*tableaux) => regroupe caractère par caractère (colonne par colonne)
    return [''.join(group) for group in zip(*tableaux)]

 
def desentrelacer_bin(entrelaces):
    """
    Désentrelace des chaînes binaires ['110', '001', '011', '151']
    et retourne une liste de chaînes binaires ['1001', '1111', '0101']
    """
    # zip(*entrelaces) => regroupe colonne par colonne (reconstitue chaque ligne d'origine)
    lignes = zip(*entrelaces)
    return [''.join(group) for group in lignes]


def supprimer_redondance(bin_str, n):
    """
    Supprime la redondance d'ordre n d'une chaîne binaire.
    
    bin_str : chaîne binaire redondée (ex: '001111110000')
    n       : ordre de redondance (ex: 3)
    
    Retourne la chaîne binaire sans redondance.
    """
    resultat = ""
    for i in range(0, len(bin_str), n):
        # Prendre le groupe de n bits
        groupe = bin_str[i:i+n]
        if groupe:
            # Voter pour le bit majoritaire
            compte_1 = groupe.count('1')
            compte_0 = groupe.count('0')
            bit_majoritaire = '1' if compte_1 > compte_0 else '0'
            resultat += bit_majoritaire
    
    return resultat


def simuler_canal(trame_entrelacee):
    """
    Simule un canal qui transforme le 2ème et 3ème bit en leurs opposés.
    
    trame_entrelacee : liste de chaînes binaires après entrelacement
    
    Retourne la trame modifiée par le canal.
    """
    resultat = []
    
    for groupe in trame_entrelacee:
        groupe_modifie = list(groupe)
        
        # Inverser le 2ème bit (indice 1) s'il existe
        if len(groupe_modifie) > 1:
            groupe_modifie[1] = '1' if groupe_modifie[1] == '0' else '0'
        
        # Inverser le 3ème bit (indice 2) s'il existe
        if len(groupe_modifie) > 2:
            groupe_modifie[2] = '1' if groupe_modifie[2] == '0' else '0'
        
        resultat.append(''.join(groupe_modifie))
    
    return resultat


def process_trame():
    """
    Fonction principale qui traite une trame binaire en appliquant:
    1. Redondance
    2. Entrelacement
    3. Simulation du canal (inversion des 2ème et 3ème bits)
    4. Désentrelacement
    5. Suppression de redondance
    
    Puis vérifie que la trame finale est identique à la trame initiale.
    """
    # Demander les entrées à l'utilisateur
    trame_initiale = input("Entrez la trame binaire (ex: 0110): ")
    
    # Vérifier que la trame ne contient que des 0 et des 1
    if not all(bit in '01' for bit in trame_initiale):
        return "Erreur: La trame doit contenir uniquement des 0 et des 1."
    
    ordre_redondance = int(input("Entrez l'ordre de redondance (ex: 3): "))
    
    # Paramètres d'entrelacement
    longueur_mot = int(input("Entrez la longueur des mots (m) pour l'entrelacement: "))
    profondeur = int(input("Entrez la profondeur (t) pour l'entrelacement (nombre de sous-groupes dans chaque groupe): "))
    
    # 1. Appliquer la redondance
    trame_redondante = redondance_n(trame_initiale, ordre_redondance)
    print(f"Trame après redondance (B): {trame_redondante}")
    
    # 2. Préparation pour l'entrelacement
    taille_groupe = longueur_mot * profondeur  # Taille totale d'un groupe (m*t)
    
    # Compléter la trame si nécessaire pour avoir des groupes complets
    while len(trame_redondante) % taille_groupe != 0:
        trame_redondante += '0'  # Ajouter des 0 de padding
    
    # Diviser la trame en groupes de taille m*t
    groupes = []
    for i in range(0, len(trame_redondante), taille_groupe):
        groupes.append(trame_redondante[i:i+taille_groupe])
    
    print(f"Trame divisée en groupes de taille {taille_groupe}: {groupes}")
    
    # 3. Entrelacement par groupe
    trame_entrelacee = []
    for groupe in groupes:
        # Diviser le groupe en t sous-groupes de taille m
        sous_groupes = []
        for i in range(0, len(groupe), longueur_mot):
            sous_groupes.append(groupe[i:i+longueur_mot])
        
        print(f"Groupe divisé en sous-groupes: {sous_groupes}")
        
        # Entrelacer ce groupe
        entrelace = entrelacer_bin(sous_groupes)
        entrelace_joint = ''.join(entrelace)
        trame_entrelacee.append(entrelace_joint)
    
    print(f"Trame après entrelacement (C): {trame_entrelacee}")
    
    # 4. Simulation du canal (inversion des 2ème et 3ème bits)
    trame_canal = simuler_canal(trame_entrelacee)
    print(f"Trame après passage dans le canal (D): {trame_canal}")
    
    # 5. Désentrelacement par groupe
    trame_desentrelacee = []
    for groupe_entrelace in trame_canal:  # Utiliser la trame modifiée par le canal
        # Préparer le groupe entrelacé pour le désentrelacement
        groupe_entrelace_liste = []
        for i in range(0, len(groupe_entrelace), profondeur):
            groupe_entrelace_liste.append(groupe_entrelace[i:i+profondeur])
        
        # Désentrelacer ce groupe
        groupe_desentrelace = desentrelacer_bin(groupe_entrelace_liste)
        groupe_desentrelace_joint = ''.join(groupe_desentrelace)
        trame_desentrelacee.append(groupe_desentrelace_joint)
    
    print(f"Trame après désentrelacement (E): {trame_desentrelacee}")
    
    # 6. Reconstituer la trame (joindre les groupes)
    trame_reconstituee = ''.join(trame_desentrelacee)
    print(f"Trame reconstituée: {trame_reconstituee}")
    
    # 7. Supprimer la redondance
    trame_finale = supprimer_redondance(trame_reconstituee, ordre_redondance)
    
    # Supprimer les bits de padding éventuels
    trame_finale = trame_finale[:len(trame_initiale)]
    
    print(f"Trame finale après suppression de la redondance (F): {trame_finale}")
    
    # 8. Vérifier si la trame finale est identique à la trame initiale
    if trame_finale == trame_initiale:
        return f"Succès! La trame finale ({trame_finale}) est identique à la trame initiale ({trame_initiale})."
    else:
        return f"Échec. La trame finale ({trame_finale}) diffère de la trame initiale ({trame_initiale})."

 

# Exécuter la fonction principale si ce script est exécuté directement
if __name__ == "__main__":
    print("\n=== TRAITEMENT DE TRAME BINAIRE ===")
    resultat = process_trame()
    print(resultat)
