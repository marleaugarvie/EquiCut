import streamlit as st
import pandas as pd
import math
from io import StringIO

# ==============================================================================
# 1. FONCTIONS DE CALCUL (Logique principale de votre programme)
# Ces fonctions sont presque identiques à votre code original.
# La seule modification majeure est que la fonction principale "analyze_data"
# RETOURNE les résultats au lieu de les IMPRIMER.
# ==============================================================================

def calculate_shannon_entropy_and_equitability(counts):
    """
    Calcule l'entropie de Shannon (H) et l'équitabilité (E) pour une liste de comptages.
    """
    total_count = sum(counts)
    if total_count == 0:
        return 0, 0

    num_categories = len(counts)
    shannon_h = 0

    for count in counts:
        if count > 0:
            proportion = count / total_count
            shannon_h -= proportion * math.log(proportion)

    if num_categories <= 1:
        equitability_e = 0
    else:
        equitability_e = shannon_h / math.log(num_categories)

    return shannon_h, equitability_e

def analyze_data(data_counts):
    """
    Analyse les données pour trouver le point de coupure optimal.
    RETOURNE les résultats pour affichage dans l'interface Streamlit.
    """
    if not data_counts or len(data_counts) < 2:
        st.error("Erreur : Les données doivent contenir au moins deux catégories pour l'analyse.")
        return None

    num_original_categories = len(data_counts)

    # Calcul de l'entropie et de l'équitabilité globales
    h_global, e_global = calculate_shannon_entropy_and_equitability(data_counts)

    results = []
    # Itération à travers tous les points de coupure possibles
    for cutoff_value in range(num_original_categories - 1):
        count_low = sum(data_counts[i] for i in range(cutoff_value + 1))
        count_high = sum(data_counts[i] for i in range(cutoff_value + 1, num_original_categories))

        dichotomized_counts = [count_low, count_high]

        if count_low == 0 or count_high == 0:
            h_cutoff, e_cutoff = 0, 0
        else:
            h_cutoff, e_cutoff = calculate_shannon_entropy_and_equitability(dichotomized_counts)

        absolute_difference = abs(e_global - e_cutoff)

        results.append({
            "Point de coupure": f"{cutoff_value}/{cutoff_value + 1}",
            "H (Coupure)": h_cutoff,
            "E (Coupure)": e_cutoff,
            "Différence Absolue (E)": absolute_difference
        })

    # Trouver le point de coupure optimal
    optimal_result = min(results, key=lambda x: x["Différence Absolue (E)"])

    # Renvoyer un dictionnaire contenant tous les résultats
    return {
        "num_categories": num_original_categories,
        "h_global": h_global,
        "e_global": e_global,
        "detailed_results": results,
        "optimal_result": optimal_result
    }

# ==============================================================================
# 2. INTERFACE UTILISATEUR STREAMLIT
# C'est la partie qui crée la page web interactive.
# ==============================================================================

st.set_page_config(layout="wide", page_title="Analyse d'Entropie")

st.title("Outil d'Analyse pour le Point de Coupure Optimal par l'Entropie")
st.markdown("""
Cette application web implémente la méthode décrite dans l'article *"[Votre Titre d'Article Ici]"*.
Elle permet de déterminer le point de coupure optimal pour une variable ordinale en se basant sur la théorie de l'information.
""")

st.sidebar.header("Instructions")
st.sidebar.info(
    """
    1. **Préparez votre fichier de données** : Il doit être un fichier texte (`.txt`) contenant une seule colonne de nombres. Chaque ligne représente le nombre de cas (fréquence) pour une catégorie, en partant de la catégorie 0.
    2. **Téléversez le fichier** en utilisant le bouton ci-dessous.
    3. **Cliquez sur "Lancer l'Analyse"**.
    4. **Consultez les résultats** qui s'afficheront sur la page.
    5. **Téléchargez les résultats** si vous le souhaitez en utilisant le bouton qui apparaîtra en bas.
    """
)

# --- Étape A : Téléversement du fichier ---
uploaded_file = st.file_uploader("1. Choisissez votre fichier de données (.txt)", type="txt")

if uploaded_file is not None:
    try:
        # Lecture et validation des données
        string_data = uploaded_file.getvalue().decode("utf-8")
        lines = string_data.strip().split('\n')
        counts = [int(line.strip()) for line in lines if line.strip()]

        st.success(f"Fichier téléversé avec succès. {len(counts)} catégories détectées.")
        
        # Afficher un aperçu des données
        with st.expander("Afficher les données brutes téléversées"):
            st.text(string_data)

        # --- Étape B : Bouton pour lancer l'analyse ---
        if st.button("2. Lancer l'Analyse", type="primary"):
            
            # --- Étape C : Appel de la fonction d'analyse et affichage des résultats ---
            analysis_results = analyze_data(counts)

            if analysis_results:
                st.header("Résultats de l'Analyse")

                # Afficher les résultats globaux
                st.subheader("Résultats Globaux")
                col1, col2, col3 = st.columns(3)
                col1.metric("Nombre de catégories", f"{analysis_results['num_categories']}")
                col2.metric("Entropie Globale (H)", f"{analysis_results['h_global']:.4f}")
                col3.metric("Équitabilité Globale (E)", f"{analysis_results['e_global']:.4f}")

                # Afficher le résultat optimal de manière visible
                st.subheader("Point de Coupure Optimal")
                optimal = analysis_results['optimal_result']
                st.success(f"**Le point de coupure optimal est : {optimal['Point de coupure']}**")
                
                col_opt1, col_opt2 = st.columns(2)
                col_opt1.metric("Équitabilité pour ce point de coupure", f"{optimal['E (Coupure)']:.4f}")
                col_opt2.metric("Différence absolue minimale avec l'équitabilité globale", f"{optimal['Différence Absolue (E)']:.4f}")

                # Afficher le tableau détaillé
                st.subheader("Détails pour chaque point de coupure")
                results_df = pd.DataFrame(analysis_results['detailed_results'])
                st.dataframe(results_df.style.highlight_min(subset=['Différence Absolue (E)'], color='lightgreen'))

                # --- Étape D : Option de téléchargement ---
                st.header("Télécharger les Résultats")
                
                # Préparer le contenu du fichier texte à télécharger
                output_string = StringIO()
                output_string.write("ANALYSE D'ENTROPIE POUR LE POINT DE COUPURE OPTIMAL\n")
                output_string.write("="*50 + "\n\n")
                output_string.write("RÉSULTATS GLOBAUX\n")
                output_string.write(f"Nombre de catégories originales: {analysis_results['num_categories']}\n")
                output_string.write(f"Entropie Globale (H): {analysis_results['h_global']:.4f}\n")
                output_string.write(f"Équitabilité Globale (E): {analysis_results['e_global']:.4f}\n\n")
                output_string.write("POINT DE COUPURE OPTIMAL\n")
                output_string.write(f"Point de coupure: {optimal['Point de coupure']}\n")
                output_string.write(f"Équitabilité pour ce point: {optimal['E (Coupure)']:.4f}\n")
                output_string.write(f"Différence absolue minimale: {optimal['Différence Absolue (E)']:.4f}\n\n")
                output_string.write("DÉTAILS COMPLETS\n")
                results_df.to_csv(output_string, index=False, sep='\t')
                
                st.download_button(
                    label="📥 Télécharger le fichier de résultats (.txt)",
                    data=output_string.getvalue().encode('utf-8'),
                    file_name="resultats_analyse_entropie.txt",
                    mime="text/plain"
                )

    except Exception as e:
        st.error(f"Erreur lors de la lecture ou du traitement du fichier. Veuillez vérifier le format de votre fichier. Détails de l'erreur : {e}")
