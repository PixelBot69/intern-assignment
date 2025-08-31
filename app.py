from flask import Flask, request, jsonify, render_template, Response
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# ---------- AUTH ----------
USERNAME = os.getenv("ADMIN_USER", "admin")       
PASSWORD = os.getenv("ADMIN_PASS", "password123")  

def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

def authenticate():
    return Response(
        "Authentication required", 401,
        {"WWW-Authenticate": 'Basic realm="Login Required"'}
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


# ---------- MODELS ----------
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    education = db.Column(db.String(200))
    skills = db.Column(db.String(500)) 
    github = db.Column(db.String(200))
    linkedin = db.Column(db.String(200))
    portfolio = db.Column(db.String(200))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    description = db.Column(db.String(300))
    skills = db.Column(db.String(200)) 
    link = db.Column(db.String(200))


# ---------- ROUTES ----------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/profile", methods=["GET"])
def get_profile():
    profile = Profile.query.first()
    if profile:
        return jsonify({
            "name": profile.name,
            "email": profile.email,
            "education": profile.education,
            "skills": profile.skills.split(","),
            "links": {
                "github": profile.github,
                "linkedin": profile.linkedin,
                "portfolio": profile.portfolio
            }
        })
    return jsonify({"error": "No profile found"}), 404

@app.route("/projects", methods=["GET"])
def get_projects():
    skill = request.args.get("skill")
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 5))

    query = Project.query
    if skill:
        query = query.filter(Project.skills.like(f"%{skill}%"))

    projects = query.offset((page - 1) * limit).limit(limit).all()
    return jsonify([{
        "title": p.title,
        "description": p.description,
        "skills": p.skills.split(","),
        "link": p.link
    } for p in projects])

@app.route("/projects", methods=["POST"])
@requires_auth
def add_project():
    data = request.json
    project = Project(
        title=data.get("title"),
        description=data.get("description"),
        skills=",".join(data.get("skills", [])),
        link=data.get("link")
    )
    db.session.add(project)
    db.session.commit()
    return jsonify({"message": "Project added"}), 201

@app.route("/skills/top", methods=["GET"])
def top_skills():
    profile = Profile.query.first()
    if profile:
        return jsonify(profile.skills.split(","))
    return jsonify([])

@app.route("/search", methods=["GET"])
def search():
    q = request.args.get("q", "")
    projects = Project.query.filter(Project.title.like(f"%{q}%")).all()
    return jsonify([{
        "title": p.title,
        "description": p.description,
        "skills": p.skills.split(","),
        "link": p.link
    } for p in projects])


# ---------- ALWAYS RESEED DATA ----------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # Clear old data
        Profile.query.delete()
        Project.query.delete()
        db.session.commit()

        # Add fresh profile
        profile = Profile(
            name="Aryan Singh",
            email="indianpiear@gmail.com",
            education="B.Tech Computer Science",
            skills="Python,JavaScript,Flask,React,SQL",
            github="https://github.com/PixelBot69",
            linkedin="https://www.linkedin.com/in/aryan-singh-4b1869249/",
            portfolio="https://rayvynai.com/"
        )
        db.session.add(profile)

        # Add fresh projects
        db.session.add_all([
            Project(
                title="Internship Work – Smart Tech Website",
                description="Developed a smart tech company website during internship.",
                skills="HTML,CSS,JavaScript,Flask",
                link="https://github.com/PixelBot69/smart-tech-website"
            ),
            Project(
                title="Game Toxicity Detection",
                description="Built a BERT-based model to detect toxicity in online game chat.",
                skills="Python,Transformers,BERT,MachineLearning",
                link="https://github.com/PixelBot69/gamingtoxicity"
            ),
            Project(
                title="E-commerce App",
                description="Full-stack e-commerce project with modern stack.",
                skills="Python,Flask,React,SQL",
                link="https://github.com/PixelBot69/ecommerce"
            ),
            Project(
                title="Disaster Management System",
                description="App for reporting and managing disasters effectively.",
                skills="Python,Django,React,SQLite",
                link="https://github.com/PixelBot69/Disaster-Management"
            ),
            Project(
                title="SaaS Skill Learning Tool",
                description="A SaaS platform where people can learn skills for free in the most effective way.",
                skills="Python,Flask,React,APIs",
                link="https://github.com/PixelBot69/saas-skill-tool"
            )
        ])
        db.session.commit()

    app.run(host="0.0.0.0", port=8000, debug=False)
