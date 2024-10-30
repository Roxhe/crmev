# CRMEV - Gestion des Contrats et Événements

**CRMEV** est un projet conçu pour la gestion simplifiée de contrats et d'événements. Pour organiser, suivre et administrer les contrats et les événements d'une manière efficace. L'objectif est de rendre la gestion plus intuitive et accessible pour les équipes.

## Étapes d'Installation

1. **Créer le dossier dans lequel vous voulez créer le projet**

   ```bash
   mkdir mon_dossier_crmev
   cd mon_dossier_crmev
   ```

2. **Cloner le projet depuis GitHub**

   ```bash
   git clone https://github.com/Roxhe/crmev.git
   ```

3. **Aller dans le dossier du projet**

   ```bash
   cd crmev
   ```

4. **Créer et activer un environnement virtuel**

   ```bash
   python -m venv env
   source env/bin/activate   # Sous Linux/macOS
   env\Scripts\activate      # Sous Windows
   ```

5. **Configurer le chemin PYTHONPATH pour prévenir des problèmes de path**

   ```bash
   set PYTHONPATH=PATH_TO\CRMEV
   ```

6. **Initialiser la base de données**

   ```bash
   python app/init_db.py
   ```

   **Note** : Assurez vous de modifier l'URL de la base de données dans le code pour correspondre à votre propre base de données après cette étape. (valable également pour la base de données de test)

7. **Vérifier les commandes disponibles via l'application**

   ```bash
   python app/main.py --help
   ```

8. **Exécuter les tests et vérifier le coverage de l'application**

   ```bash
   pytest --cov
   ```

---


