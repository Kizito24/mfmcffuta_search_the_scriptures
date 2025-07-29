from flask import Flask, render_template, request, jsonify
import csv, os, random

app = Flask(__name__)

CSV_FILE = 'hubs.csv'

HUBS = [
    {
        "name": "Love Hub",
        "description": "A hub focused on community outreach and care.",
        "whatsapp": "https://wa.me/xxxxxxxxxx1",
        "theme": {
            "color": "danger",
            "icon": "bi-heart-fill"
        }
    },
    {
        "name": "Faith Hub",
        "description": "This hub builds spiritual strength through prayer.",
        "whatsapp": "https://wa.me/xxxxxxxxxx2",
        "theme": {
            "color": "primary",
            "icon": "bi-cloud-lightning-rain-fill"
        }
    },
    {
        "name": "Power Hub",
        "description": "Focused on youth leadership and evangelism.",
        "whatsapp": "https://wa.me/xxxxxxxxxx3",
        "theme": {
            "color": "success",
            "icon": "bi-lightning-charge-fill"
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
