from flask import Flask, render_template, request, jsonify
import csv, os, random

app = Flask(__name__)

CSV_FILE = 'hubs.csv'

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

def load_assignments():
    if not os.path.exists(CSV_FILE):
        return {}
    with open(CSV_FILE, newline='') as f:
        return {row[0]: {"phone": row[1], "hub": row[2]} for row in csv.reader(f)}

def save_assignment(name, phone, hub_name):
    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([name, phone, hub_name])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/assign', methods=['POST'])
def assign():
    name = request.form['name'].strip().title()
    phone = request.form['phone'].strip()
    assignments = load_assignments()

    if name in assignments:
        hub_name = assignments[name]["hub"]
        hub = next((h for h in HUBS if h['name'] == hub_name), None)
    else:
        hub = random.choice(HUBS)
        save_assignment(name, phone, hub['name'])

    return jsonify({
        "hub": hub['name'],
        "description": hub['description'],
        "whatsapp": hub['whatsapp'],
        "theme": hub['theme']
    })

if __name__ == '__main__':
    app.run(debug=True)
