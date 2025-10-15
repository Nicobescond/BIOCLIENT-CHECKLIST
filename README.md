# 🏪 Application d'Audit BIOCOOP - Guide d'Utilisation

## 📋 Vue d'ensemble

Application web développée pour les organismes de certification effectuant des audits de fournisseurs locaux et divers pour BIOCOOP. L'outil permet de :
- ✅ Saisir les informations du fournisseur
- ✅ Réaliser un audit complet selon le cahier des charges BIOCOOP
- ✅ Générer automatiquement un rapport Excel avec plan d'action
- ✅ Calculer un score de conformité global

## 🚀 Installation et Démarrage

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation locale

1. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

2. **Lancer l'application**
```bash
streamlit run app.py
```

3. **Accéder à l'application**
L'application s'ouvre automatiquement dans votre navigateur à l'adresse : `http://localhost:8501`

## 📊 Système de Notation

L'application utilise un système de notation à 4 niveaux :

| Notation | Signification | Points | Usage |
|----------|---------------|--------|-------|
| **A** | Conforme | 20 | Exigence respectée |
| **B** | Non-conformité mineure | 10 | Écart mineur, action corrective simple |
| **C** | Non-conformité majeure | 0 | Écart important, action corrective urgente |
| **N/A** | Non applicable | - | Point non concerné par l'activité |

### Coefficients de criticité

Les catégories sont pondérées selon leur importance :

- **CRITIQUE** (x2.0) : Sécurité des aliments, Hygiène
- **MAJEUR** (x1.5) : Réglementation, Exigences BIOCOOP spécifiques
- **STANDARD** (x1.0) : Maîtrise des origines, OGM

### Niveau de conformité global

| Score | Niveau | Signification |
|-------|--------|---------------|
| ≥ 90% | EXCELLENT | Conformité exemplaire |
| 75-89% | SATISFAISANT | Bonne conformité générale |
| 60-74% | ACCEPTABLE | Conformité acceptable, améliorations nécessaires |
| 40-59% | INSUFFISANT | Non-conformités importantes |
| < 40% | NON CONFORME | Niveau de conformité critique |

## 🎯 Utilisation de l'Application

### Étape 1 : Informations Fournisseur

Renseignez toutes les informations du fournisseur :
- Identification (nom, adresse, interlocuteurs)
- Contacts (effectif, personne qualité, contact crise)
- Certifications (bio, qualité, dates de validité)
- Informations sur le partenariat avec BIOCOOP

**Champs obligatoires** marqués d'un astérisque (*)

### Étape 2 : Checklist d'Audit

Pour chaque point d'audit :

1. **Lire attentivement** la question et les détails associés
2. **Observer** sur site et consulter les documents
3. **Sélectionner la notation** appropriée (A, B, C ou N/A)
4. **Commenter** vos observations dans le champ prévu :
   - Décrire les constats
   - Mentionner les preuves observées
   - Expliquer les écarts identifiés

**Conseils pour un audit de qualité :**
- Demander les preuves documentaires (certificats, procédures, enregistrements)
- Observer les pratiques réelles sur le terrain
- Interroger le personnel
- Prendre des photos si nécessaire (à conserver séparément)

### Étape 3 : Rapport Final

#### Visualisation des résultats

- **Score global** : Moyenne pondérée de tous les points audités
- **Scores par catégorie** : Détail de la performance par thématique
- **Liste des non-conformités** : Tableau récapitulatif des points B et C

#### Génération du rapport Excel

Le rapport Excel contient 4 feuilles :

1. **Informations Fournisseur** : Toutes les données d'identification
2. **Résultats Audit** : Checklist complète avec notations et commentaires
3. **Plan d'Action** : Liste des non-conformités avec colonnes pour :
   - Action corrective à définir
   - Responsable
   - Délai de mise en œuvre
   - Statut de suivi
   - Date de clôture
4. **Synthèse** : Scores globaux et par catégorie

## 📁 Structure du Rapport Excel

### Feuille "Plan d'Action"

Le plan d'action est pré-rempli avec toutes les non-conformités identifiées. Il reste à compléter par le magasin référent :

| Colonne | Description | À compléter par |
|---------|-------------|-----------------|
| ID | Identifiant du point | ✅ Automatique |
| Point d'audit | Question auditée | ✅ Automatique |
| Non-conformité | Constat de l'auditeur | ✅ Automatique |
| Action corrective | Mesure à mettre en place | ⚠️ À définir |
| Responsable | Personne en charge | ⚠️ À définir |
| Délai | Date limite de mise en œuvre | ⚠️ À définir |
| Statut | En cours / Terminé | ⚠️ À suivre |
| Date de clôture | Quand l'action est finalisée | ⚠️ À renseigner |
| Commentaires | Suivi, remarques | ⚠️ À compléter |

**Codage couleur :**
- 🔴 **Rouge** : Non-conformité majeure (C) - À traiter en priorité
- 🟡 **Jaune** : Non-conformité mineure (B) - À traiter

## 🔧 Personnalisation

### Modifier la checklist

Pour adapter la checklist à vos besoins, modifiez la variable `CHECKLIST_AUDIT` dans `app.py` :

```python
"NOUVELLE_CATEGORIE": {
    "criticite": "MAJEUR",  # CRITIQUE, MAJEUR ou STANDARD
    "coefficient": 1.5,      # 2.0, 1.5 ou 1.0
    "items": [
        {
            "id": "XXX-001",
            "question": "Votre question d'audit",
            "details": "Précisions et attendus"
        }
    ]
}
```

### Modifier le système de notation

Ajustez les valeurs dans `NOTATION_OPTIONS` :

```python
NOTATION_OPTIONS = {
    "A": {"label": "A - Conforme", "points": 20, "color": "#28a745"},
    # Modifiez les points ou ajoutez de nouveaux niveaux
}
```

## 🌐 Déploiement en Ligne

### Option 1 : Streamlit Cloud (Gratuit)

1. Créez un compte sur [streamlit.io](https://streamlit.io/)
2. Connectez votre dépôt GitHub
3. Sélectionnez `app.py` comme fichier principal
4. Déployez !

Votre application sera accessible via une URL type : `https://votre-app.streamlit.app`

### Option 2 : Serveur propre

```bash
# Installation sur serveur Linux
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

Pour une utilisation en production, configurez un reverse proxy (Nginx) et HTTPS.

## 📚 Référentiels BIOCOOP

L'application intègre les exigences suivantes du cahier des charges BIOCOOP :

### ✅ Produits autorisés
- Produits certifiés bio (label européen)
- Produits en conversion
- Produits SPG (Nature et Progrès, Simples)
- Produits de la mer selon zones autorisées

### ❌ Interdictions
- Additifs : E551, E171
- Labels interdits : HVE, Zéro résidu, Bleu Blanc Cœur, etc.
- Transport aérien pour produits finis
- Serres chauffées (hors plants)

### 🌍 Commerce équitable obligatoire
- Café, Thé, Chocolat, Sucre de canne/coco
- Fruits secs spécifiques
- Beurre de karité, Huile d'argan
- Riz hors UE

### 🗺️ Maîtrise des origines
- Couples produits/origines interdits (ex: Ail de Chine)
- Zones obligatoires (ex: Agrumes du bassin méditerranéen)

## 🆘 Support et Maintenance

### Problèmes courants

**L'application ne démarre pas**
```bash
# Vérifier la version de Python
python --version  # Doit être ≥ 3.8

# Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall
```

**Erreur lors de la génération Excel**
- Vérifier que tous les champs obligatoires sont remplis
- S'assurer qu'au moins un item a été noté

**L'application est lente**
- Streamlit recharge à chaque interaction
- Pour de meilleures performances, déployez sur un serveur

### Contact

Pour toute question ou amélioration :
- Organisme de certification : [Votre contact]
- BIOCOOP Qualité Produits : Nicolas LOZANO (n.lozano@biocoop.fr)

## 📄 Licence et Droits

© 2025 - Application développée pour les audits fournisseurs BIOCOOP
Conforme au cahier des charges valeurs BIOCOOP (version octobre 2025)

---

**Version** : 1.0  
**Dernière mise à jour** : Octobre 2025  
**Développé avec** : Streamlit 🎈
