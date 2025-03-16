import streamlit as st
import main

# Configuration de la page
st.set_page_config(
    page_title="Simulation de Numérisation",
    page_icon="🔢",
    layout="wide"
)

st.title("Simulation de Numérisation avec Redondance et Entrelacement")

st.markdown("""
Cette application simule le traitement d'une trame binaire avec:
1. Redondance 
2. Entrelacement
3. Simulation d'un canal bruité (inversion des 2ème et 3ème bits)
4. Désentrelacement
5. Suppression de redondance
""")

# Entrée utilisateur
col1, col2 = st.columns(2)

with col1:
    trame_initiale = st.text_input("Trame binaire initiale", "0110")
    
    # Vérification que la trame ne contient que des 0 et des 1
    if not all(bit in '01' for bit in trame_initiale):
        st.error("La trame doit contenir uniquement des 0 et des 1.")
    
    ordre_redondance = st.number_input("Ordre de redondance (n)", min_value=1, value=3, step=1)

with col2:
    longueur_mot = st.number_input("Longueur des mots (m)", min_value=1, value=3, step=1)
    profondeur = st.number_input("Profondeur (t)", min_value=1, value=2, step=1)

# Bouton pour lancer la simulation
if st.button("Lancer la simulation"):
    # Créer des zones pour l'affichage des résultats
    st.subheader("Résultats de la simulation")
    
    # 1. Appliquer la redondance
    trame_redondante = main.redondance_n(trame_initiale, ordre_redondance)
    st.markdown(f"**B: Trame après redondance:**")
    st.code(trame_redondante)
    
    # 2. Préparation pour l'entrelacement
    taille_groupe = longueur_mot * profondeur  # Taille totale d'un groupe (m*t)
    
    # Compléter la trame si nécessaire pour avoir des groupes complets
    trame_complete = trame_redondante
    while len(trame_complete) % taille_groupe != 0:
        trame_complete += '0'  # Ajouter des 0 de padding
    
    if trame_complete != trame_redondante:
        st.markdown(f"**Trame complétée avec padding:**")
        st.code(trame_complete)
    
    # Diviser la trame en groupes de taille m*t
    groupes = []
    for i in range(0, len(trame_complete), taille_groupe):
        groupes.append(trame_complete[i:i+taille_groupe])
    
    st.markdown(f"**Trame divisée en groupes de taille {taille_groupe}:**")
    st.code(str(groupes))
    
    # 3. Entrelacement par groupe
    trame_entrelacee = []
    sous_groupes_par_groupe = []
    
    for groupe in groupes:
        # Diviser le groupe en t sous-groupes de taille m
        sous_groupes = []
        for i in range(0, len(groupe), longueur_mot):
            sous_groupes.append(groupe[i:i+longueur_mot])
        
        sous_groupes_par_groupe.append(sous_groupes)
        
        # Entrelacer ce groupe
        entrelace = main.entrelacer_bin(sous_groupes)
        entrelace_joint = ''.join(entrelace)
        trame_entrelacee.append(entrelace_joint)
    
    st.markdown("**Groupes divisés en sous-groupes:**")
    for i, sg in enumerate(sous_groupes_par_groupe):
        st.code(f"Groupe {i+1}: {sg}")
    
    st.markdown(f"**C: Trame après entrelacement:**")
    st.code(str(trame_entrelacee))
    
    # 4. Simulation du canal (inversion des 2ème et 3ème bits)
    trame_canal = main.simuler_canal(trame_entrelacee)
    
    st.markdown(f"**D: Trame après passage dans le canal (inversion des 2ème et 3ème bits):**")
    st.code(str(trame_canal))
    
    # Afficher les différences
    st.markdown("**Bits modifiés par le canal:**")
    for i, (avant, apres) in enumerate(zip(trame_entrelacee, trame_canal)):
        if avant != apres:
            diff = []
            for j, (bit_avant, bit_apres) in enumerate(zip(avant, apres)):
                if bit_avant != bit_apres:
                    diff.append(f"Position {j+1}: {bit_avant} → {bit_apres}")
            
            st.code(f"Groupe {i+1}: {', '.join(diff)}")
    
    # 5. Désentrelacement par groupe
    trame_desentrelacee = []
    for groupe_entrelace in trame_canal:
        # Préparer le groupe entrelacé pour le désentrelacement
        groupe_entrelace_liste = []
        for i in range(0, len(groupe_entrelace), profondeur):
            groupe_entrelace_liste.append(groupe_entrelace[i:i+profondeur])
        
        # Désentrelacer ce groupe
        groupe_desentrelace = main.desentrelacer_bin(groupe_entrelace_liste)
        groupe_desentrelace_joint = ''.join(groupe_desentrelace)
        trame_desentrelacee.append(groupe_desentrelace_joint)
    
    st.markdown(f"**E: Trame après désentrelacement:**")
    st.code(str(trame_desentrelacee))
    
    # 6. Reconstituer la trame
    trame_reconstituee = ''.join(trame_desentrelacee)
    st.markdown(f"**Trame reconstituée:**")
    st.code(trame_reconstituee)
    
    # 7. Supprimer la redondance
    trame_finale = main.supprimer_redondance(trame_reconstituee, ordre_redondance)
    
    # Supprimer les bits de padding éventuels
    trame_finale = trame_finale[:len(trame_initiale)]
    
    st.markdown(f"**F: Trame finale après suppression de la redondance:**")
    st.code(trame_finale)
    
    # 8. Afficher le résultat
    if trame_finale == trame_initiale:
        st.success(f"Succès! La trame finale ({trame_finale}) est identique à la trame initiale ({trame_initiale}).")
    else:
        st.error(f"Échec. La trame finale ({trame_finale}) diffère de la trame initiale ({trame_initiale}).")
    
    # Afficher le résumé
    st.subheader("Résumé du traitement")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.markdown("**A (Initial)**")
        st.code(trame_initiale)
    
    with col2:
        st.markdown("**B (Redondance)**")
        st.code(trame_redondante)
    
    with col3:
        st.markdown("**C (Entrelacement)**")
        st.code(str(trame_entrelacee))
    
    with col4:
        st.markdown("**D (Canal)**")
        st.code(str(trame_canal))
    
    with col5:
        st.markdown("**E (Désentrelacement)**")
        st.code(str(trame_desentrelacee))
    
    with col6:
        st.markdown("**F (Final)**")
        st.code(trame_finale)

# Ajout d'informations explicatives en bas de page
st.markdown("---")
st.subheader("Comment ça marche?")
st.markdown("""
1. **Redondance**: Chaque bit est répété n fois (ex: '0' → '000' si n=3)
2. **Entrelacement**: Les bits sont réorganisés pour disperser les erreurs potentielles
3. **Canal bruité**: Simule les erreurs de transmission en inversant certains bits
4. **Désentrelacement**: Reconstitue l'ordre original des bits
5. **Suppression de redondance**: Utilise la redondance pour corriger les erreurs par vote majoritaire
""")

st.info("Cette application démontre comment la combinaison de redondance et d'entrelacement permet de corriger des erreurs lors de la transmission numérique.") 