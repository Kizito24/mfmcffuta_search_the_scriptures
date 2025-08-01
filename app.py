from flask import Flask, render_template, request, jsonify # type: ignore
from flask_pymongo import PyMongo # type: ignore
from dotenv import load_dotenv # type: ignore
import random
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# MongoDB Setup
app.config["MONGO_URI"] = "mongodb+srv://kizitochiazor:W8tvPuFJWDxesxqs@cluster0.lq5sv.mongodb.net/hub_assignments?retryWrites=true&w=majority"
mongo = PyMongo(app)
db = mongo.cx["hub_assignments"]
assignments_col = db["assignments"]

# Hubs
HUBS = [
    {
        "name": "Hub of Wisdom",
        "description": "Welcome to the Hub of Wisdom Family 🙏🏼\n\nWe are excited to have you on board! Our hub is dedicated to nurturing your spiritual growth and fostering a community of love, support, and encouragement.\n\nOur anchor scripture is Proverbs 4:7. And we believe it will inspire and guide you.\nAs you fellowship with your hub members, remember to share love, kindness, and respect 🙇🏾.\nGod bless 🙏",
        "whatsapp": "https://chat.whatsapp.com/Cdf0FcUylNG8yQpiERGweO?mode=ac_t",
        "theme": {"color": "info", "icon": "bi-lightbulb-fill"}
    },
    {
        "name": "Hub of Righteousness",
        "description": "Welcome to the Hub of Righteousness Family 🙏🏼\n\nWe are excited to have you on board! Our hub is dedicated to nurturing your spiritual growth and fostering a community of love, support, and encouragement.\n\nOur anchor scripture is Malachi 4:2. And we believe it will inspire and guide you.\nAs you fellowship with your hub members, remember to share love, kindness, and respect 🙇🏾.\nGod bless 🙏",
        "whatsapp": "https://chat.whatsapp.com/ImkpsadXk8LDsxicZCYwLk?mode=ac_t",
        "theme": {"color": "success", "icon": "bi-shield-check"}
    },
    {
        "name": "Hub of Greatness",
        "description": "Welcome to the Hub of Greatness Family 🙏🏼\n\nWe are excited to have you on board! Our hub is dedicated to nurturing your spiritual growth and fostering a community of love, support, and encouragement.\n\nOur anchor scripture is Genesis 12:2. And we believe it will inspire and guide you.\nAs you fellowship with your hub members, remember to share love, kindness, and respect 🙇🏾.\nGod bless 🙏",
        "whatsapp": "https://chat.whatsapp.com/H2mbJkUKVKQK1hoouSld6z?mode=ac_t",
        "theme": {"color": "warning", "icon": "bi-trophy-fill"}
    },
    {
        "name": "Hub of the Mighty",
        "description": "Welcome to the Hub of the Mighty Family 🙏🏼\n\nWe are excited to have you on board! Our hub is dedicated to nurturing your spiritual growth and fostering a community of love, support, and encouragement.\n\nOur anchor scripture is Judges 6:12. And we believe it will inspire and guide you.\nAs you fellowship with your hub members, remember to share love, kindness, and respect 🙇🏾.\nGod bless 🙏",
        "whatsapp": "https://chat.whatsapp.com/HQLaTWBGw642zU0tpMaDXH?mode=ac_t",
        "theme": {"color": "warning", "icon": "bi-lightning-fill"}
    },
    {
        "name": "The Overcomers Hub",
        "description": "Welcome to the Overcomers Family 🙏🏼\n\nWe are excited to have you on board! Our hub is dedicated to nurturing your spiritual growth and fostering a community of love, support, and encouragement.\n\nOur anchor scripture is 1 John 4:4. And we believe it will inspire and guide you.\nAs you fellowship with your hub members, remember to share love, kindness, and respect 🙇🏾.\nGod bless 🙏",
        "whatsapp": "https://chat.whatsapp.com/KLyC1rZGQmE36r3pMQiJgw?mode=ac_t",
        "theme": {"color": "danger", "icon": "bi-award-fill"}
    }
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/assign', methods=['POST'])
def assign():
    name = request.form['name'].strip().title()
    phone = request.form['phone'].strip()

    if phone.startswith("0"):
        phone = "+234" + phone[1:]
    elif phone.startswith("234") and not phone.startswith("+"):
        phone = "+" + phone

    existing = assignments_col.find_one({"phone": phone})

    if existing:
        hub_name = existing["hub"]
        hub = next((h for h in HUBS if h["name"] == hub_name), None)
        message = "You have been previously assigned to this hub."
    else:
        hub = random.choice(HUBS)
        assignments_col.insert_one({
            "name": name,
            "phone": phone,
            "hub": hub['name']
        })
        message = "You have been successfully assigned to a hub!"

    return jsonify({
        "hub": hub['name'],
        "description": hub['description'],
        "whatsapp": hub['whatsapp'],
        "theme": hub['theme'],
        "message": message
    })

if __name__ == '__main__':
    app.run(debug=True)
