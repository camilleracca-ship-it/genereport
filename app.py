import pandas as pd
import streamlit as st

st.title("GeneReport")
st.subheader("Outil de génération automatisée de rapports d'analyse génétique à partir de fichier CSV.")
st.markdown("""
Cette application permet la génération automatisée de comptes rendus textuels d'analyse génétique à partir d'annotations issues de MobiDetails.

Mode emploi
1. Télécharger le tableur modèle : """)
with open("modele_variants.xlsx", "rb") as file:
    st.download_button(
        label="Tableur modèle (Excel)",
        data=file,
        file_name="modele_variants.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
st.markdown("""
2. Renseigner les données dans le tableur en respectant strictement la structure et les colonnes  
3. Exporter le tableur complété au format CSV depuis votre ordinateur  
4. Importer le fichier CSV dans l'application : 
""")
uploaded_file = st.file_uploader("Votre fichier (CSV)", type=["csv"])

if uploaded_file is None:
    st.stop()

df = pd.read_csv(uploaded_file)

df["ID_PATIENT"] = df["ID_PATIENT"].astype(str).str.strip()

for id_patient, df_patient in df.groupby("ID_PATIENT"):
    serie = str(df_patient.iloc[0]["SERIE_ANALYSE"]).strip()

    en_tete = f"""
__________________
Rapport d'analyse génétique pour le patient {id_patient} (Série d'analyse : {serie})
"""
    st.text(en_tete)

    for i, (_, row) in enumerate(df_patient.iterrows(), start=1):
        type_de_variant = str(row["TYPE_VARIANT"]).strip().lower()
        variant_hgvs = str(row["VARIANT_HGVS"]).strip()
        zygosite = str(row["ZYGOSITE"]).strip().lower()
        gene = str(row["GENE"]).strip()
        transcript = str(row["TRANSCRIPT"]).strip()
        conservation = str(row["CONSERVATION"]).strip().lower()
        localisation_du_domaine = str(row["LOCALISATION_DOMAINE"]).strip()
        position = str(row["POSITION"]).strip()
        in_silico_prediction = str(row["IN_SILICO_PREDICTION"]).strip()
        splicing_effect = str(row["SPLICING_EFFECT"]).strip().lower()
        splicing_prediction = str(row["SPLICING_PREDICTION"]).strip()
        population_data = str(row["POPULATION_DATA"]).strip()
        allele_frequency = str(row["ALLELE_FREQUENCY"]).strip()
        literature_data = str(row["LITERATURE_DATA"]).strip().lower()
        literature_detail = str(row["LITERATURE_DETAIL"]).strip()
        PMID = str(row["PMID"]).strip()
        functional_data = str(row["FUNCTIONAL_DATA"]).strip().lower()
        pmid_functional = str(row["PMID_FUNCTIONAL"]).strip()
        class_acmg = str(row["CLASS_ACMG"]).strip()

        if splicing_effect == "probable anomalie de l'épissage":
            splicing_sentence = f"Les outils de prédiction in silico suggèrent un effet sur l'épissage : {splicing_prediction}."
        elif splicing_effect == "pas d'anomalie de l'épissage":
            splicing_sentence = "Les outils de prédiction in silico ne mettent pas en évidence d’anomalie de l’épissage."
        else:
            splicing_sentence = "Aucune prédiction in silico n’est disponible concernant l’impact sur l’épissage."

        if literature_data == "oui":
            literature_sentence = f"ce variant a été rapporté dans la litterature scientifique : {literature_detail} (PMID : {PMID})."
        else:
            literature_sentence = "ce variant n'a pas été rapporté dans la litterature scientifique."

        if functional_data == "analyse fonctionnelle : perte de fonction":
            functional_sentence = f"Les analyses fonctionnelles disponibles sont en faveur d'une perte de fonction de la protéine associée à ce variant (PMID : {pmid_functional})."
        elif functional_data == "analyse fonctionnelle : gain de fonction":
            functional_sentence = f"Les analyses fonctionnelles disponibles sont en faveur d'un gain de fonction de la protéine associée à ce variant (PMID : {pmid_functional})."
        elif functional_data == "analyse fonctionnelle : absence d'altération":
            functional_sentence = f"Les analyses fonctionnelles disponibles sont en faveur d'une absence d'altération de la protéine associée à ce variant (PMID : {pmid_functional})."
        else:
            functional_sentence = "Aucune analyse fonctionnelle n'est disponible pour ce variant."

        if class_acmg == "1.0":
            class_sentence = "bénin"
            class_affichage = 1
        elif class_acmg == "2.0":
            class_sentence = "probablement bénin"
            class_affichage = 2
        elif class_acmg == "3.0":
            class_sentence = "de signification indéterminée"
            class_affichage = 3
        elif class_acmg == "4.0":
            class_sentence = "probablement pathogène"
            class_affichage = 4
        elif class_acmg == "5.0":
            class_sentence = "pathogène"
            class_affichage = 5
        else:
            class_sentence = "classement non précisé"
            class_affichage = "non indiqué"

        rapport = f"""
Variant {i} :
Mise en évidence du variant {type_de_variant} {variant_hgvs} à l’état {zygosite} sur le gène {gene} ({transcript}).

Ce variant concerne un acide aminé {conservation} conservé dans les comparaisons inter-espèces. Il est localisé {localisation_du_domaine} de la protéine (position {position}).

Les algorithmes in silico de prédiction de pathogénicité sont {in_silico_prediction}. {splicing_sentence}

Il est {population_data} dans les bases de données de populations contrôles (gnomAD v4.1.0 : {allele_frequency}).

À ce jour, {literature_sentence}
{functional_sentence}

Au vu de l'ensemble de ces éléments, ce variant est classé {class_affichage}, c’est-à-dire {class_sentence}, selon les recommandations ACMG/AMP.
___________________________________
"""
        st.text(rapport)
