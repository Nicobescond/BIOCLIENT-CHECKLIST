import streamlit as st
import pandas as pd
import json
from datetime import datetime
import io

# Configuration de la page
st.set_page_config(
    page_title="Audit BIOCOOP - Fournisseurs Locaux",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Définition de la checklist d'audit basée sur le cahier des charges
CHECKLIST_AUDIT = {
    "1. SÉCURITÉ DES ALIMENTS": {
        "criticite": "CRITIQUE",
        "coefficient": 2.0,
        "items": [
            {
                "id": "SEC-001",
                "question": "Pertinence et vérification des points critiques (étude HACCP) si applicable",
                "details": "Vérifier l'existence et la mise à jour du plan HACCP, identification des CCP"
            },
            {
                "id": "SEC-002",
                "question": "Maîtrise du risque allergènes",
                "details": "Procédures de gestion des allergènes, étiquetage, formation du personnel"
            },
            {
                "id": "SEC-003",
                "question": "Maîtrise du risque corps étrangers",
                "details": "Procédures de prévention, détection (tamis, aimants, détecteur de métaux)"
            },
            {
                "id": "SEC-004",
                "question": "Maîtrise du risque chimique",
                "details": "Stockage et utilisation des produits chimiques, traçabilité"
            },
            {
                "id": "SEC-005",
                "question": "Définition d'un plan d'analyses et d'un plan de contrôles",
                "details": "Plan d'analyses microbiologiques, physico-chimiques, fréquence, laboratoire"
            },
            {
                "id": "SEC-006",
                "question": "Système de blocage/libération produits si concerné",
                "details": "Procédure de quarantaine et de libération des produits"
            },
            {
                "id": "SEC-007",
                "question": "Gestion des retraits rappels produits (traçabilité des lots livrés aux magasins)",
                "details": "Procédure de retrait/rappel, traçabilité amont/aval, tests de traçabilité"
            }
        ]
    },
    "2. HYGIÈNE DU PERSONNEL ET DES LOCAUX": {
        "criticite": "CRITIQUE",
        "coefficient": 2.0,
        "items": [
            {
                "id": "HYG-001",
                "question": "Définition/affichage des règles d'hygiène",
                "details": "Règles affichées, accessibles et compréhensibles par le personnel"
            },
            {
                "id": "HYG-002",
                "question": "Respect application des règles d'hygiène par le personnel",
                "details": "Port de la tenue, lavage des mains, comportement en production"
            },
            {
                "id": "HYG-003",
                "question": "Conformité infrastructure (locaux de production, sanitaires, vestiaires, équipements)",
                "details": "État des locaux, séparation des zones, équipements pour l'hygiène"
            },
            {
                "id": "HYG-004",
                "question": "Maîtrise des opérations de nettoyage",
                "details": "Plan de nettoyage, produits utilisés, fréquence, enregistrements"
            },
            {
                "id": "HYG-005",
                "question": "Maîtrise des températures (process et installation)",
                "details": "Contrôle des températures, enregistrements, actions correctives"
            },
            {
                "id": "HYG-006",
                "question": "Surveillance des nuisibles",
                "details": "Plan de lutte contre les nuisibles, prestataire, fréquence, résultats"
            }
        ]
    },
    "3. RÉGLEMENTATION": {
        "criticite": "MAJEUR",
        "coefficient": 1.5,
        "items": [
            {
                "id": "REG-001",
                "question": "Certificat bio couvrant l'ensemble des produits en cours de validité",
                "details": "Vérifier la validité du certificat bio et la couverture de tous les produits"
            },
            {
                "id": "REG-002",
                "question": "Maîtrise des contrôles quantitatifs (poids/volume)",
                "details": "Procédure de contrôle des poids/volumes, balance étalonnée"
            },
            {
                "id": "REG-003",
                "question": "Conformité globale des étiquettes produits + marquage lot/DLC",
                "details": "Étiquetage réglementaire, liste d'ingrédients, allergènes, lot, DLC/DLUO"
            },
            {
                "id": "REG-004",
                "question": "Conformité système de traçabilité produits",
                "details": "Traçabilité amont/aval, test de traçabilité réalisé"
            }
        ]
    },
    "4. EXIGENCES BIOCOOP - PRODUITS AUTORISÉS": {
        "criticite": "MAJEUR",
        "coefficient": 1.5,
        "items": [
            {
                "id": "BIO-001",
                "question": "Produits certifiés bio portant le label européen OU en conversion OU SPG autorisé",
                "details": "Vérifier Nature et Progrès ou Simples, attestation en cours de validité"
            },
            {
                "id": "BIO-002",
                "question": "Produits de la mer : ingrédient principal non certifiable + ingrédients bio",
                "details": "Si applicable, vérifier conformité avec annexe produits de la pêche"
            },
            {
                "id": "BIO-003",
                "question": "Absence de dioxyde de silicium (E551) et dioxyde de titane (E171)",
                "details": "Vérifier les recettes et étiquettes"
            }
        ]
    },
    "5. EXIGENCES BIOCOOP - INGRÉDIENTS SPÉCIFIQUES": {
        "criticite": "MAJEUR",
        "coefficient": 1.5,
        "items": [
            {
                "id": "ING-001",
                "question": "Sel : de mer, récolté manuellement, origine France",
                "details": "Pour le sel vendu en l'état (aromatisé ou non)"
            },
            {
                "id": "ING-002",
                "question": "Arômes : certifiés biologiques",
                "details": "Si goût annoncé dans le nom, tous les ingrédients aromatisants doivent être bio"
            },
            {
                "id": "ING-003",
                "question": "Absence de labels interdits sur les étiquettes",
                "details": "HVE, Zéro résidu, Produit responsable, Bleu Blanc Cœur, Bee Friendly, etc."
            }
        ]
    },
    "6. EXIGENCES BIOCOOP - COMMERCE ÉQUITABLE": {
        "criticite": "MAJEUR",
        "coefficient": 1.5,
        "items": [
            {
                "id": "CEQ-001",
                "question": "Produits bruts obligatoirement commerce équitable : Café, Sucre de canne/coco, Chocolat",
                "details": "Vérifier label présent sur l'étiquette (liste des labels autorisés disponible)"
            },
            {
                "id": "CEQ-002",
                "question": "Thé (hors Japon/Corée du Sud), Beurre de cacao certifiés commerce équitable",
                "details": "Label présent sur l'étiquette"
            },
            {
                "id": "CEQ-003",
                "question": "Fruits secs mono-ingrédient : cajou, macadamia, coco, Brésil, ananas, papaye, banane, mangue",
                "details": "Commerce équitable obligatoire (vrac et conditionné)"
            },
            {
                "id": "CEQ-004",
                "question": "Gingembre confit (Hors UE), Beurre de karité, Huile d'argan, Riz hors UE",
                "details": "Commerce équitable obligatoire"
            },
            {
                "id": "CEQ-005",
                "question": "Pâtes à tartiner : sucre de canne commerce équitable avec mention",
                "details": "Mention '*issu du commerce équitable' en fin de liste d'ingrédients"
            }
        ]
    },
    "7. EXIGENCES BIOCOOP - TRANSPORT ET PRODUCTION": {
        "criticite": "MAJEUR",
        "coefficient": 1.5,
        "items": [
            {
                "id": "TRA-001",
                "question": "Interdiction transport aérien pour produits finis",
                "details": "Vérifier les modes de transport utilisés"
            },
            {
                "id": "TRA-002",
                "question": "Pas de serres chauffées (hors production de plants)",
                "details": "Pour fruits et légumes uniquement"
            },
            {
                "id": "TRA-003",
                "question": "Interdiction déverdissage des agrumes vendus en l'état",
                "details": "Vérifier les pratiques"
            },
            {
                "id": "TRA-004",
                "question": "Tomates 'anciennes' : variétés de population non hybride",
                "details": "Si applicable, vérifier les variétés"
            },
            {
                "id": "TRA-005",
                "question": "Produits de la pêche : conformité avec annexe zones autorisées",
                "details": "Cf. Liste des produits de la pêche et zones BIOCOOP"
            }
        ]
    },
    "8. MAÎTRISE ORIGINES MATIÈRES PREMIÈRES": {
        "criticite": "STANDARD",
        "coefficient": 1.0,
        "items": [
            {
                "id": "ORI-001",
                "question": "Connaissance des origines des ingrédients",
                "details": "Cohérence avec le tableau des origines BIOCOOP (par sondage)"
            },
            {
                "id": "ORI-002",
                "question": "Respect des couples produits/origines interdits",
                "details": "Ex: Ail de Chine, Sucre de canne d'Inde, Cacao RDC, Muscade Indonésie"
            },
            {
                "id": "ORI-003",
                "question": "Respect des zones obligatoires pour produits spécifiques",
                "details": "Ex: Agrumes bassin méditerranéen, Produits animaux UE, etc."
            }
        ]
    },
    "9. MAÎTRISE OGM": {
        "criticite": "STANDARD",
        "coefficient": 1.0,
        "items": [
            {
                "id": "OGM-001",
                "question": "Maîtrise de l'absence d'OGM dans les produits",
                "details": "Seuil analytique: 0,01% produits bruts, 0,1% ingrédients élaborés"
            },
            {
                "id": "OGM-002",
                "question": "Contrôle des ingrédients à risque OGM",
                "details": "Ananas rose, betterave, maïs, colza, papaye, sirop/riz basmati, soja, sucre de canne"
            }
        ]
    }
}

# Options de notation
NOTATION_OPTIONS = {
    "A": {"label": "A - Conforme", "points": 20, "color": "#28a745"},
    "B": {"label": "B - Non-conformité mineure", "points": 10, "color": "#ffc107"},
    "C": {"label": "C - Non-conformité majeure", "points": 0, "color": "#dc3545"},
    "N/A": {"label": "N/A - Non applicable", "points": None, "color": "#6c757d"}
}

def initialize_session_state():
    """Initialise l'état de la session"""
    if 'audit_data' not in st.session_state:
        st.session_state.audit_data = {}
    if 'fournisseur_info' not in st.session_state:
        st.session_state.fournisseur_info = {}
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1

def calculer_score_global(audit_data):
    """Calcule le score global de l'audit"""
    total_points = 0
    total_possible = 0
    details_par_categorie = {}
    
    for categorie, data in CHECKLIST_AUDIT.items():
        coefficient = data["coefficient"]
        points_categorie = 0
        points_possibles_categorie = 0
        items_evalues = 0
        
        for item in data["items"]:
            item_id = item["id"]
            if item_id in audit_data and audit_data[item_id]["notation"] != "N/A":
                note = audit_data[item_id]["notation"]
                points = NOTATION_OPTIONS[note]["points"]
                points_categorie += points * coefficient
                points_possibles_categorie += 20 * coefficient
                items_evalues += 1
        
        if items_evalues > 0:
            score_categorie = (points_categorie / points_possibles_categorie) * 100
            details_par_categorie[categorie] = {
                "score": score_categorie,
                "points": points_categorie,
                "points_possibles": points_possibles_categorie,
                "items_evalues": items_evalues,
                "criticite": data["criticite"]
            }
            total_points += points_categorie
            total_possible += points_possibles_categorie
    
    score_global = (total_points / total_possible * 100) if total_possible > 0 else 0
    
    return score_global, details_par_categorie

def get_niveau_conformite(score):
    """Détermine le niveau de conformité selon le score"""
    if score >= 90:
        return "EXCELLENT", "#28a745"
    elif score >= 75:
        return "SATISFAISANT", "#5cb85c"
    elif score >= 60:
        return "ACCEPTABLE", "#ffc107"
    elif score >= 40:
        return "INSUFFISANT", "#fd7e14"
    else:
        return "NON CONFORME", "#dc3545"

def generer_rapport_excel(fournisseur_info, audit_data):
    """Génère un rapport d'audit complet en Excel avec xlsxwriter"""
    try:
        import xlsxwriter
        
        # Créer un buffer en mémoire
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        
        # Définir les formats
        header_format = workbook.add_format({
            'bold': True,
            'font_color': 'white',
            'bg_color': '#2C3E50',
            'font_size': 12,
            'align': 'center',
            'valign': 'vcenter',
            'border': 1
        })
        
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 16,
            'align': 'left'
        })
        
        bold_format = workbook.add_format({'bold': True})
        
        conforme_format = workbook.add_format({
            'bg_color': '#D5F4E6',
            'border': 1
        })
        
        mineur_format = workbook.add_format({
            'bg_color': '#FFF3CD',
            'border': 1
        })
        
        majeur_format = workbook.add_format({
            'bg_color': '#F8D7DA',
            'border': 1
        })
        
        border_format = workbook.add_format({'border': 1})
        
        # FEUILLE 1: Informations Fournisseur
        ws1 = workbook.add_worksheet("Informations Fournisseur")
        ws1.write(0, 0, "RAPPORT D'AUDIT FOURNISSEUR BIOCOOP", title_format)
        ws1.merge_range(0, 0, 0, 3, "RAPPORT D'AUDIT FOURNISSEUR BIOCOOP", title_format)
        
        row = 2
        for key, value in fournisseur_info.items():
            ws1.write(row, 0, key, bold_format)
            ws1.write(row, 1, str(value))
            row += 1
        
        ws1.set_column('A:A', 35)
        ws1.set_column('B:B', 50)
        
        # FEUILLE 2: Résultats Audit
        ws2 = workbook.add_worksheet("Résultats Audit")
        
        headers = ["ID", "Catégorie", "Question", "Notation", "Commentaire", "Criticité"]
        for col, header in enumerate(headers):
            ws2.write(0, col, header, header_format)
        
        row = 1
        for categorie, data in CHECKLIST_AUDIT.items():
            for item in data["items"]:
                item_id = item["id"]
                if item_id in audit_data:
                    notation = audit_data[item_id]["notation"]
                    commentaire = audit_data[item_id].get("commentaire", "")
                    
                    # Choisir le format selon la notation
                    if notation == "A":
                        cell_format = conforme_format
                    elif notation == "B":
                        cell_format = mineur_format
                    elif notation == "C":
                        cell_format = majeur_format
                    else:
                        cell_format = border_format
                    
                    ws2.write(row, 0, item_id, cell_format)
                    ws2.write(row, 1, categorie.split(".")[1].strip(), cell_format)
                    ws2.write(row, 2, item["question"], cell_format)
                    ws2.write(row, 3, notation, cell_format)
                    ws2.write(row, 4, commentaire, cell_format)
                    ws2.write(row, 5, data["criticite"], cell_format)
                    
                    row += 1
        
        ws2.set_column('A:A', 12)
        ws2.set_column('B:B', 30)
        ws2.set_column('C:C', 50)
        ws2.set_column('D:D', 12)
        ws2.set_column('E:E', 40)
        ws2.set_column('F:F', 15)
        
        # FEUILLE 3: Plan d'Action
        ws3 = workbook.add_worksheet("Plan d'Action")
        
        action_headers = ["ID", "Point d'audit", "Non-conformité", "Action corrective", 
                         "Responsable", "Délai", "Statut", "Date clôture", "Commentaires"]
        for col, header in enumerate(action_headers):
            ws3.write(0, col, header, header_format)
        
        row = 1
        for categorie, data in CHECKLIST_AUDIT.items():
            for item in data["items"]:
                item_id = item["id"]
                if item_id in audit_data and audit_data[item_id]["notation"] in ["B", "C"]:
                    cell_format = majeur_format if audit_data[item_id]["notation"] == "C" else mineur_format
                    
                    ws3.write(row, 0, item_id, cell_format)
                    ws3.write(row, 1, item["question"], cell_format)
                    ws3.write(row, 2, audit_data[item_id].get("commentaire", ""), cell_format)
                    ws3.write(row, 3, "[À définir]", cell_format)
                    ws3.write(row, 4, "[Responsable]", cell_format)
                    ws3.write(row, 5, "[Date limite]", cell_format)
                    ws3.write(row, 6, "En cours", cell_format)
                    ws3.write(row, 7, "", cell_format)
                    ws3.write(row, 8, "", cell_format)
                    
                    row += 1
        
        ws3.set_column('A:A', 12)
        ws3.set_column('B:B', 40)
        ws3.set_column('C:C', 35)
        ws3.set_column('D:D', 35)
        ws3.set_column('E:E', 20)
        ws3.set_column('F:F', 15)
        ws3.set_column('G:G', 12)
        ws3.set_column('H:H', 15)
        ws3.set_column('I:I', 30)
        
        # FEUILLE 4: Synthèse
        ws4 = workbook.add_worksheet("Synthèse")
        
        score_global, details = calculer_score_global(audit_data)
        niveau, couleur = get_niveau_conformite(score_global)
        
        ws4.write(0, 0, "SYNTHÈSE DE L'AUDIT", title_format)
        ws4.merge_range(0, 0, 0, 3, "SYNTHÈSE DE L'AUDIT", title_format)
        
        ws4.write(2, 0, "Score Global", bold_format)
        ws4.write(2, 1, f"{score_global:.1f}%", bold_format)
        ws4.write(3, 0, "Niveau de Conformité", bold_format)
        ws4.write(3, 1, niveau, bold_format)
        
        ws4.write(5, 0, "Scores par catégorie", bold_format)
        
        headers_synth = ["Catégorie", "Score (%)", "Criticité", "Items évalués"]
        for col, header in enumerate(headers_synth):
            ws4.write(6, col, header, header_format)
        
        row = 7
        for categorie, info in details.items():
            ws4.write(row, 0, categorie.split(".")[1].strip())
            ws4.write(row, 1, f"{info['score']:.1f}%")
            ws4.write(row, 2, info['criticite'])
            ws4.write(row, 3, info['items_evalues'])
            row += 1
        
        ws4.set_column('A:A', 40)
        ws4.set_column('B:B', 15)
        ws4.set_column('C:C', 15)
        ws4.set_column('D:D', 15)
        
        # Fermer le workbook
        workbook.close()
        
        # Récupérer le buffer
        output.seek(0)
        return output
        
    except Exception as e:
        st.error(f"❌ Erreur lors de la génération du rapport Excel : {e}")
        return None

# Interface principale
def main():
    initialize_session_state()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🏪 BIOCOOP")
        st.markdown("*Audit Fournisseurs Locaux*")
        st.divider()
        
        st.title("Navigation")
        
        step = st.radio(
            "Étapes de l'audit",
            ["1️⃣ Informations Fournisseur", "2️⃣ Checklist d'Audit", "3️⃣ Rapport Final"],
            index=st.session_state.current_step - 1
        )
        
        if "1️⃣" in step:
            st.session_state.current_step = 1
        elif "2️⃣" in step:
            st.session_state.current_step = 2
        else:
            st.session_state.current_step = 3
        
        st.divider()
        st.markdown("### 📊 Système de notation")
        st.markdown("**A** (20 pts) = Conforme ✅")
        st.markdown("**B** (10 pts) = NC mineure ⚠️")
        st.markdown("**C** (0 pts) = NC majeure ❌")
        st.markdown("**N/A** = Non applicable ⊘")
        
        st.divider()
        st.caption("Version 1.1 - Octobre 2025")
    
    # Contenu principal
    if st.session_state.current_step == 1:
        afficher_etape_informations()
    elif st.session_state.current_step == 2:
        afficher_etape_checklist()
    else:
        afficher_etape_rapport()

def afficher_etape_informations():
    st.title("📋 Informations sur le Fournisseur")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Identification")
        nom_fournisseur = st.text_input("Nom du fournisseur*", 
                                         value=st.session_state.fournisseur_info.get("Nom du fournisseur", ""))
        adresse = st.text_area("Adresse de l'activité de production/fabrication*",
                               value=st.session_state.fournisseur_info.get("Adresse", ""))
        
        interlocuteurs = st.text_area("Interlocuteurs rencontrés + fonction/coordonnées*",
                                      value=st.session_state.fournisseur_info.get("Interlocuteurs", ""))
        
        effectif = st.text_input("Effectif total",
                                 value=st.session_state.fournisseur_info.get("Effectif", ""))
        
        qualite = st.text_input("Nombre de personnes au service qualité",
                                value=st.session_state.fournisseur_info.get("Service qualité", ""))
    
    with col2:
        st.subheader("Contact et Certifications")
        contact_crise = st.text_input("Contact en cas de crise sanitaire (retrait/rappel)*",
                                      value=st.session_state.fournisseur_info.get("Contact crise", ""))
        
        gamme_produits = st.text_area("Description de l'entreprise / gamme de produits livrés chez BIOCOOP*",
                                      value=st.session_state.fournisseur_info.get("Gamme produits", ""))
        
        annee_partenariat = st.text_input("Année de démarrage du partenariat avec Biocoop",
                                          value=st.session_state.fournisseur_info.get("Année partenariat", ""))
        
        certifications = st.text_area("Certifications qualité et produits (dont BIO et BIO COHÉRENCE) + dates de validité*",
                                      value=st.session_state.fournisseur_info.get("Certifications", ""))
        
        site_mixte = st.radio("Type de site", ["100% BIO", "Site mixte (BIO + conventionnel)"],
                             index=0 if st.session_state.fournisseur_info.get("Type site", "100% BIO") == "100% BIO" else 1)
    
    st.subheader("Informations complémentaires")
    col3, col4 = st.columns(2)
    
    with col3:
        date_visite = st.date_input("Date de l'audit*",
                                    value=datetime.now())
        auditeur = st.text_input("Nom de l'auditeur*",
                                 value=st.session_state.fournisseur_info.get("Auditeur", ""))
    
    with col4:
        magasin_referent = st.text_input("Magasin référent BIOCOOP",
                                         value=st.session_state.fournisseur_info.get("Magasin référent", ""))
        
        date_derniere_visite = st.text_input("Date de la dernière fiche de visite BIOCOOP",
                                            value=st.session_state.fournisseur_info.get("Dernière visite", ""))
    
    st.markdown("---")
    
    if st.button("➡️ Passer à la checklist d'audit", type="primary", use_container_width=True):
        # Sauvegarder les informations
        st.session_state.fournisseur_info = {
            "Nom du fournisseur": nom_fournisseur,
            "Adresse": adresse,
            "Interlocuteurs": interlocuteurs,
            "Effectif": effectif,
            "Service qualité": qualite,
            "Contact crise": contact_crise,
            "Gamme produits": gamme_produits,
            "Année partenariat": annee_partenariat,
            "Certifications": certifications,
            "Type site": site_mixte,
            "Date audit": date_visite.strftime("%d/%m/%Y"),
            "Auditeur": auditeur,
            "Magasin référent": magasin_referent,
            "Dernière visite": date_derniere_visite
        }
        st.session_state.current_step = 2
        st.rerun()

def afficher_etape_checklist():
    st.title("✅ Checklist d'Audit BIOCOOP")
    st.markdown("---")
    
    # Barre de progression
    total_items = sum(len(data["items"]) for data in CHECKLIST_AUDIT.values())
    items_completes = len([k for k in st.session_state.audit_data if st.session_state.audit_data[k].get("notation")])
    progress = items_completes / total_items if total_items > 0 else 0
    
    st.progress(progress, text=f"Progression : {items_completes}/{total_items} items complétés ({progress*100:.0f}%)")
    
    # Filtres
    col1, col2 = st.columns([3, 1])
    with col1:
        categorie_selectionnee = st.selectbox(
            "Sélectionner une catégorie",
            ["Toutes les catégories"] + list(CHECKLIST_AUDIT.keys())
        )
    
    with col2:
        filtre_notation = st.multiselect(
            "Filtrer par notation",
            ["A", "B", "C", "N/A"],
            default=[]
        )
    
    st.markdown("---")
    
    # Affichage des items
    categories_a_afficher = CHECKLIST_AUDIT.keys() if categorie_selectionnee == "Toutes les catégories" else [categorie_selectionnee]
    
    for categorie in categories_a_afficher:
        data = CHECKLIST_AUDIT[categorie]
        
        with st.expander(f"**{categorie}**", expanded=(categorie_selectionnee != "Toutes les catégories")):
            st.markdown(f"**Criticité**: {data['criticite']} | **Coefficient**: {data['coefficient']}x")
            st.markdown("---")
            
            for item in data["items"]:
                item_id = item["id"]
                
                # Initialiser les données si nécessaire
                if item_id not in st.session_state.audit_data:
                    st.session_state.audit_data[item_id] = {"notation": None, "commentaire": ""}
                
                # Appliquer le filtre
                if filtre_notation and st.session_state.audit_data[item_id]["notation"] not in filtre_notation:
                    continue
                
                # Conteneur pour chaque item
                with st.container():
                    st.markdown(f"**{item_id}** - {item['question']}")
                    st.caption(item['details'])
                    
                    col_note, col_comment = st.columns([1, 3])
                    
                    with col_note:
                        notation = st.selectbox(
                            "Notation",
                            options=list(NOTATION_OPTIONS.keys()),
                            format_func=lambda x: NOTATION_OPTIONS[x]["label"],
                            key=f"notation_{item_id}",
                            index=list(NOTATION_OPTIONS.keys()).index(st.session_state.audit_data[item_id]["notation"]) 
                                  if st.session_state.audit_data[item_id]["notation"] else 0,
                            label_visibility="collapsed"
                        )
                        st.session_state.audit_data[item_id]["notation"] = notation
                    
                    with col_comment:
                        commentaire = st.text_area(
                            "Commentaire / Constat",
                            value=st.session_state.audit_data[item_id]["commentaire"],
                            key=f"comment_{item_id}",
                            height=80,
                            placeholder="Détaillez vos observations, preuves, constats..."
                        )
                        st.session_state.audit_data[item_id]["commentaire"] = commentaire
                    
                    st.markdown("---")
    
    # Boutons de navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Retour aux informations", use_container_width=True):
            st.session_state.current_step = 1
            st.rerun()
    
    with col2:
        if st.button("➡️ Générer le rapport", type="primary", use_container_width=True):
            st.session_state.current_step = 3
            st.rerun()

def afficher_etape_rapport():
    st.title("📊 Rapport d'Audit Final")
    st.markdown("---")
    
    # Calculer les scores
    score_global, details_categories = calculer_score_global(st.session_state.audit_data)
    niveau, couleur = get_niveau_conformite(score_global)
    
    # Affichage du score global
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Score Global", f"{score_global:.1f}%")
    
    with col2:
        st.metric("Niveau de Conformité", niveau)
    
    with col3:
        total_nc = sum(1 for v in st.session_state.audit_data.values() 
                      if v.get("notation") in ["B", "C"])
        st.metric("Non-conformités", total_nc)
    
    st.markdown("---")
    
    # Détails par catégorie
    st.subheader("📈 Scores par catégorie")
    
    df_scores = pd.DataFrame([
        {
            "Catégorie": cat.split(".")[1].strip(),
            "Score (%)": f"{info['score']:.1f}",
            "Criticité": info['criticite'],
            "Items évalués": info['items_evalues']
        }
        for cat, info in details_categories.items()
    ])
    
    st.dataframe(df_scores, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Plan d'action (non-conformités)
    st.subheader("⚠️ Non-conformités identifiées")
    
    nc_list = []
    for categorie, data in CHECKLIST_AUDIT.items():
        for item in data["items"]:
            item_id = item["id"]
            if item_id in st.session_state.audit_data:
                notation = st.session_state.audit_data[item_id]["notation"]
                if notation in ["B", "C"]:
                    nc_list.append({
                        "ID": item_id,
                        "Catégorie": categorie.split(".")[1].strip(),
                        "Question": item["question"],
                        "Gravité": "Majeure" if notation == "C" else "Mineure",
                        "Commentaire": st.session_state.audit_data[item_id].get("commentaire", "")
                    })
    
    if nc_list:
        df_nc = pd.DataFrame(nc_list)
        st.dataframe(df_nc, use_container_width=True, hide_index=True)
    else:
        st.success("✅ Aucune non-conformité identifiée !")
    
    st.markdown("---")
    
    # Génération du rapport Excel
    st.subheader("📥 Télécharger le rapport complet")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Régénérer le rapport", use_container_width=True):
            st.rerun()
    
    with col2:
        buffer = generer_rapport_excel(st.session_state.fournisseur_info, st.session_state.audit_data)
        
        if buffer:
            nom_fichier = f"Audit_BIOCOOP_{st.session_state.fournisseur_info.get('Nom du fournisseur', 'Fournisseur').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.xlsx"
            
            st.download_button(
                label="📥 Télécharger le rapport Excel",
                data=buffer,
                file_name=nom_fichier,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="primary",
                use_container_width=True
            )
        else:
            st.error("❌ Impossible de générer le rapport Excel")
    
    st.markdown("---")
    
    # Bouton retour
    if st.button("⬅️ Retour à la checklist", use_container_width=True):
        st.session_state.current_step = 2
        st.rerun()

if __name__ == "__main__":
    main()
