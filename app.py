from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo  # type: ignore
from flask_session import Session  # ✅ Missing import added
from dotenv import load_dotenv
import random
import os

# Load .env file (if used)
load_dotenv()

app = Flask(__name__)

# MongoDB Setup
app.config["MONGO_URI"] = "mongodb+srv://kizitochiazor:W8tvPuFJWDxesxqs@cluster0.lq5sv.mongodb.net/hub_assignments?retryWrites=true&w=majority"
mongo = PyMongo(app)

# Session Configuration
app.config["SESSION_TYPE"] = "mongodb"
app.config["SESSION_MONGODB"] = mongo.cx  # ✅ Use PyMongo client
app.config["SESSION_MONGODB_DB"] = "hub_assignments"
app.config["SESSION_MONGODB_COLLECT"] = "sessions"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
Session(app)

# Assign collection after mongo is set
db = mongo.cx["hub_assignments"]
assignments_col = db["assignments"]

# Hub data
HUBS = [
    {
        "name": "Hub of Wisdom",
        "description": "A gathering of seekers and thinkers, led by divine insight. Members of this hub are encouraged to pursue knowledge, discernment, and spiritual understanding.",
        "whatsapp": "https://wa.me/xxxxxxxxxx1",
        "theme": {
            "color": "info",
            "icon": "bi-lightbulb-fill"
        }
    },
    {
        "name": "Hub of Righteousness",
        "description": "This hub stands for purity, integrity, and a life of holiness. Together, members grow in character, discipline, and the pursuit of God’s standards.",
        "whatsapp": "https://wa.me/xxxxxxxxxx2",
        "theme": {
            "color": "success",
            "icon": "bi-shield-check"
        }
    },
    {
        "name": "Hub of Greatness",
        "description": "A place where potential meets purpose. This hub inspires excellence in all areas of life and spiritual growth toward greatness in Christ.",
        "whatsapp": "https://wa.me/xxxxxxxxxx3",
        "theme": {
            "color": "warning",
            "icon": "bi-trophy-fill"
        }
    },
    {
        "name": "Hub of the Mighty",
        "description": "Made for warriors in the spirit. Members of this hub are prayerful, bold, and fearless — equipped to overcome battles and impact lives.",
        "whatsapp": "https://wa.me/xxxxxxxxxx4",
        "theme": {
            "color": "warning",
            "icon": "bi-lightning-fill"
        }
    },
    {
        "name": "The Overcomers Hub",
        "description": "This hub celebrates victory over trials. Members are encouraged to share testimonies, lift one another, and walk daily in triumph through Christ.",
        "whatsapp": "https://wa.me/xxxxxxxxxx5",
        "theme": {
            "color": "danger",
            "icon": "bi-award-fill"
        }
    }
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/assign', methods=['POST'])
def assign():
    name = request.form['name'].strip().title()
    phone = request.form['phone'].strip()

    existing = assignments_col.find_one({"name": name})

    if existing:
        hub_name = existing["hub"]
        hub = next((h for h in HUBS if h['name'] == hub_name), None)
    else:
        hub = random.choice(HUBS)
        assignments_col.insert_one({
            "name": name,
            "phone": phone,
            "hub": hub['name']
        })

    return jsonify({
        "hub": hub['name'],
        "description": hub['description'],
        "whatsapp": hub['whatsapp'],
        "theme": hub['theme']
    })

if __name__ == '__main__':
    app.run(debug=True)
