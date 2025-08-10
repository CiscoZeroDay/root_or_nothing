import os
import json
import hashlib
from flask import Flask, render_template, render_template_string, request, redirect, url_for, flash, session
from markupsafe import Markup, escape
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash("Veuillez vous connecter pour accéder à cette page.", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

app = Flask(__name__)
app.secret_key = 'une_clef_secrete_pour_la_session'
app.jinja_env.sandbox = False
app.jinja_env.autoescape = False

EMPLOYES = [
    {"nom": "James Anderson", "poste": "Ingénieur Logiciel", "departement": "Informatique", "contrat": "CDI"},
    {"nom": "Jhon Carter", "poste": "Responsable RH", "departement": "Ressources Humaines", "contrat": "CDD"},
    {"nom": "Michael Johnson", "poste": "Commercial", "departement": "Ventes", "contrat": "CDI"},
    {"nom": "Olivia Thompson", "poste": "Data Analyst", "departement": "Informatique", "contrat": "CDI"},
    {"nom": "William Davis", "poste": "Technicien Support", "departement": "Informatique", "contrat": "CDD"},
    {"nom": "Leondo Martinez", "poste": "Chargé de Communication", "departement": "Marketing", "contrat": "CDI"},
    {"nom": "Phillipe Price", "poste": "Directeur Général", "departement": "Direction", "contrat": "CDI"},
    {"nom": "Gideon Goddard", "poste": "Directeur Technique", "departement": "Informatique", "contrat": "CDI"},
    {"nom": "Darlen Alderson", "poste": "Data Analyst / Scientist", "departement": "Informatique", "contrat": "CDI"},
    {"nom": "Tyrell Wellick", "poste": "RH Manager", "departement": "Ressources Humaines", "contrat": "CDI"},
    {"nom": "Mr. Robot", "poste": "Security Analyst", "departement": "Sécurité", "contrat": "CDD"},
    {"nom": "Elliot Alderson", "poste": "Pentester / Ethical Hacker", "departement": "Sécurité", "contrat": "CDI"},
    {"nom": "Claire Dubois", "poste": "Assistante RH", "departement": "Ressources Humaines", "contrat": "CDI"},
    {"nom": "Marc Lemoine", "poste": "Développeur", "departement": "Informatique", "contrat": "CDI"},
    {"nom": "Sophie Martin", "poste": "Commerciale", "departement": "Ventes", "contrat": "CDI"},
    {"nom": "Antoine Dupont", "poste": "Technicien Support", "departement": "Informatique", "contrat": "CDD"},
    {"nom": "Yasmine El Amrani", "poste": "Responsable Recrutement", "departement": "Ressources Humaines", "contrat": "CDI"},
    {"nom": "Omar Bensalah", "poste": "Administrateur Systèmes", "departement": "Informatique", "contrat": "CDI"},
    {"nom": "Hajar Benhaddou", "poste": "Chargée de Communication", "departement": "Marketing", "contrat": "CDD"},
    {"nom": "Mehdi El Idrissi", "poste": "Analyste Financier", "departement": "Finance", "contrat": "CDI"},
    {"nom": "Nadia Laabidi", "poste": "Comptable", "departement": "Finance", "contrat": "CDI"},
    {"nom": "Samir Bouziane", "poste": "Technicien Réseau", "departement": "Informatique", "contrat": "CDD"},
    {"nom": "Fatima Zahra Mourchid", "poste": "Responsable Formation", "departement": "Ressources Humaines", "contrat": "CDI"},
    {"nom": "Adil El Fassi", "poste": "Chef de Projet", "departement": "Informatique", "contrat": "CDI"},
    {"nom": "Imane Kharbouch", "poste": "Assistante Commerciale", "departement": "Ventes", "contrat": "CDD"},
    {"nom": "Karim Tazi", "poste": "Ingénieur DevOps", "departement": "Informatique", "contrat": "CDI"},
    {"nom": "Zineb El Hafidi", "poste": "Consultante RH", "departement": "Ressources Humaines", "contrat": "CDI"},
    {"nom": "Youssef Ghallab", "poste": "Technicien Hotline", "departement": "Support", "contrat": "CDD"},
    {"nom": "Salma Oulhaj", "poste": "Responsable Paie", "departement": "Ressources Humaines", "contrat": "CDI"},
    {"nom": "Hamza Ait Benhammou", "poste": "Data Analyst", "departement": "Informatique", "contrat": "CDI"},
    {"nom": "Rania El Khatib", "poste": "Chargée de Clientèle", "departement": "Ventes", "contrat": "CDI"},
    {"nom": "Mohamed El Bakali", "poste": "Responsable Informatique", "departement": "Informatique", "contrat": "CDI"},
    {"nom": "Sara Bennani", "poste": "Assistante Administrative", "departement": "Administration", "contrat": "CDD"},
    {"nom": "Ismail Chafai", "poste": "Responsable Support", "departement": "Support", "contrat": "CDI"},
    {"nom": "Khadija Raji", "poste": "Chargée RH Junior", "departement": "Ressources Humaines", "contrat": "CDD"},
    {"nom": "Walid Kharroubi", "poste": "Développeur Web", "departement": "Informatique", "contrat": "CDI"},
    {"nom": "Lamiae Mernissi", "poste": "Contrôleuse de Gestion", "departement": "Finance", "contrat": "CDI"},
    {"nom": "Othmane Jebli", "poste": "Community Manager", "departement": "Marketing", "contrat": "CDD"},
    {"nom": "Ilham Zahidi", "poste": "Responsable Juridique", "departement": "Juridique", "contrat": "CDI"},
    {"nom": "Anas El Bouhali", "poste": "Administrateur Base de Données", "departement": "Informatique", "contrat": "CDI"},
    {"nom": "Soukaina El Ouali", "poste": "Chargée Qualité", "departement": "Qualité", "contrat": "CDD"},
    {"nom": "Hicham Mouline", "poste": "Chef d'Équipe Support", "departement": "Support", "contrat": "CDI"},
    {"nom": "Myriam Bouchaib", "poste": "Assistante Juridique", "departement": "Juridique", "contrat": "CDD"},
    {"nom": "Noureddine Filali", "poste": "Responsable Logistique", "departement": "Logistique", "contrat": "CDI"},
    {"nom": "Wafae Kabbaj", "poste": "Chargée des Achats", "departement": "Achats", "contrat": "CDD"},
    {"nom": "Reda El Ghali", "poste": "Chef de Produit", "departement": "Marketing", "contrat": "CDI"},
]

# Charger les utilisateurs
def load_users():
    with open('user.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# Sauvegarder les utilisateurs
def save_users(users):
    with open('user.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

# Trouver un utilisateur par email ou username
def find_user(email):
    with open('user.json', 'r') as f:
        users = json.load(f)
        for user in users:
            if user['email'].lower() == email.lower():
                return user
    return None


@app.route('/')
def landing():
   return render_template('landing.html')

'''@app.route('/dashboard')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_input = request.form.get('email')
        password = request.form.get('password')
        user = find_user(login_input)

        if user and hashlib.md5(password.encode()).hexdigest() == user['password']:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash('Connexion réussie !', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email ou mot de passe incorrect.', 'error')

    return render_template('login.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        method = request.form.get('choice')
        if method == 'email':
            return redirect(url_for('reset_password_email'))
        elif method == 'security':
            return redirect(url_for('reset_password_security'))
    return render_template('forgot_password.html')

@app.route('/reset-password-email', methods=['GET', 'POST'])
def reset_password_email():
    if request.method == 'POST':
        email = request.form.get('email')
        user = find_user(email)
        if not user:
            flash("L'adresse email est invalide.", "error")
            return redirect(url_for('reset_password_email'))
        else:
            # Ici, tu peux simuler l'envoi d'un email avec un lien sécurisé
            flash(f"Un lien de réinitialisation a été envoyé à {email}.", "success")
            return redirect(url_for('login'))
    return render_template('reset_password_email.html')



@app.route('/reset-password-security', methods=['GET', 'POST'])
def reset_password_security():
    if request.method == 'POST':
        email = request.form.get('email')
        pet = request.form.get('pet')
        spouse = request.form.get('spouse')
        meeting_place = request.form.get('meeting_place')

        users = load_users()

        # Étape 1 : Vérifier si on a juste envoyé l'e-mail
        if email and not (pet and spouse and meeting_place):
            user = next((u for u in users if u['email'].lower() == email.lower()), None)
            if not user:
                flash("Email non trouvé.")
                return render_template('reset_password_security.html', show_questions=False)
            session['reset_email'] = email
            return render_template('reset_password_security.html', show_questions=True)

        # Étape 2 : Vérifier les réponses de sécurité
        elif pet and spouse and meeting_place:
            email = session.get('reset_email')
            user = next((u for u in users if u['email'].lower() == email.lower()), None)

            if not user:
                flash("Session expirée ou email invalide.")
                return redirect(url_for('reset_password_security'))

            questions = user.get('security_questions', {})
            if questions.get('pet', '').lower() == pet.lower() and \
               questions.get('spouse', '').lower() == spouse.lower() and \
               questions.get('meeting_place', '').lower() == meeting_place.lower():
                session['security_verified'] = True
                return redirect(url_for('set_new_password'))
            else:
                flash("Les réponses ne correspondent pas.")
                return render_template('reset_password_security.html', show_questions=True)

    return render_template('reset_password_security.html', show_questions=False)


@app.route('/set-new-password', methods=['GET', 'POST'])
def set_new_password():
    if 'reset_email' not in session or not session.get('security_verified'):
        flash("Accès non autorisé. Veuillez recommencer.", "error")
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if new_password != confirm_password:
            flash("Les mots de passe ne correspondent pas.", "error")
        else:
            users = load_users()
            for user in users:
                if user['email'] == session['reset_email']:
                    user['password'] = hashlib.md5(new_password.encode()).hexdigest()
                    save_users(users)
                    flash("Mot de passe mis à jour avec succès. Veuillez vous connecter.", "success")
                    # 🔹 Nettoyer la session
                    session.pop('reset_email', None)
                    session.pop('security_verified', None)
                    return redirect(url_for('login'))
            flash("Erreur : utilisateur introuvable.", "error")
            return redirect(url_for('forgot_password'))

    return render_template('set_new_password.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Merci de vous connecter pour accéder au tableau de bord.', 'error')
        return redirect(url_for('login'))
    return render_template('index.html', username=session['username'])

@app.route('/gestion-personnel')
@login_required
def gestion_personnel():
    return render_template('gestion-personnel.html')

@app.route('/gestion-temps')
@login_required
def gestion_temps():
    return render_template('gestion-temps.html')

@app.route("/dossiers-rh")
@login_required
def dossiers_rh():
    return render_template("dossiers_rh.html")

@app.route("/equipes-departements")
@login_required
def equipes_departements():
    return render_template("equipes_departements.html")

@app.route("/messagerie")
@login_required
def messagerie_interne():
    return render_template("messagerie_interne.html")

FILES_DIR = os.path.dirname(__file__)  # dossier où est app.py

def load_files():
    files = {}
    for fname in ("credentials.txt", "flag.txt", "moncv.pdf"):
        path = os.path.join(FILES_DIR, fname)
        if os.path.isfile(path):
            if fname.endswith(".pdf"):
                files[fname] = "[Contenu PDF non affiché]"
            else:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    files[fname] = f.read()
    return files


@app.route('/search')
def search():
    query = request.args.get('q', '').strip()

    # Blacklist pour éviter la lecture des fichiers sensibles
    blacklist = ["app.py", ".venv", "__pycache__", "docker-compose.yml", "Dockerfile","user.json"]
    if any(bad.lower() in query.lower() for bad in blacklist):
        return render_template_string("""
            <h2>Accès refusé</h2>
            <p>Le fichier ou contenu demandé est protégé.</p>
        """)
    if not query:
        return render_template_string("""
            <h2>Recherche d'employés</h2>
            <p>Veuillez entrer un nom dans la barre de recherche.</p>
        """)

    files = load_files()

    # Affichage direct du contenu des fichiers si query correspond
    if query in files:
        html = """
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background:#f4f7fc; color:#1e293b; padding:20px; }
                pre { background:#eef6ff; padding:12px; border-radius:8px; white-space: pre-wrap; }
            </style>
            <h2>Résultats pour : {query}</h2>
            <pre>{content}</pre>
        """.format(query=query, content=files[query])
        return html

    results = [emp for emp in EMPLOYES if query.lower() in emp["nom"].lower()]

    if results:
        cards_html = "".join(f"""
            <div class="card">
                <h3>{emp['nom']}</h3>
                <p><strong>Poste :</strong> {emp['poste']}</p>
                <p><strong>Département :</strong> {emp['departement']}</p>
                <p><strong>Contrat :</strong> {emp['contrat']}</p>
            </div>
        """ for emp in results)
    else:
        cards_html = query

    page = """
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: #f4f7fc;
                color: #1e293b;
                padding: 20px;
            }
            .card {
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                padding: 20px;
                margin-bottom: 20px;
                max-width: 600px;
                transition: transform 0.3s ease;
            }
            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 20px rgba(37, 99, 235, 0.2);
            }
            h2 {
                font-weight: 700;
                margin-bottom: 20px;
            }
            pre {
                background: #eef6ff;
                border: 1px solid #cfe6ff;
                padding: 12px;
                border-radius: 8px;
                white-space: pre-wrap;
            }
        </style>

        <h2>Résultats pour : {{ query }}</h2>
        {% if results %}
            {{ cards_html|safe }}
        {% else %}
            {{ cards_html|safe }}
        {% endif %}
    """

    rendered_page = render_template_string(page, query=query, cards_html=Markup(cards_html), results=bool(results), files=files, request=request)

    if not results:
        return render_template_string(rendered_page, query=query, cards_html=Markup(cards_html), results=bool(results), files=files, request=request)
    
    return rendered_page



'''@app.route('/debug')
def debug():
    import os
    cwd = os.getcwd()
    files = os.listdir(cwd)
    return f"Dossier courant : {cwd}<br>Fichiers : {files}"
'''

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

