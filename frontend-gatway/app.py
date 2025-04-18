from flask import Flask, render_template, request, redirect, jsonify, session
import requests

app = Flask(__name__)
app.secret_key = "your-secret-key"  # For session handling

AUTH_SERVICE_URL = "http://auth-service:5001"
PATIENT_SERVICE_URL = "http://patient-service:5002"


@app.route('/')
def index():
    return render_template('index.html')


# ================= AUTH ROUTES =================

@app.route('/auth', methods=['GET'])
def auth_page():
    return render_template('auth_form.html')


@app.route('/register', methods=['POST'])
def gateway_register():
    data = request.form  # From form submission
    payload = {
        "name": data.get('name'),
        "email": data.get('email'),
        "password": data.get('password'),
        "age": data.get('age'),
        "gender": data.get('gender')
    }
    print(data)
    response = requests.post(f"{AUTH_SERVICE_URL}/register", json=payload)
    return jsonify(response.json()), response.status_code


@app.route('/login', methods=['POST'])
def gateway_login():
    data = request.form
    payload = {
        "email": data.get('email'),
        "password": data.get('password')
    }
    response = requests.post(f"{AUTH_SERVICE_URL}/login", json=payload)

    if response.status_code == 200:
        res_data = response.json()
        token = res_data.get("token")
        role = res_data.get("user", {}).get("role")

        # Store token in session
        session["token"] = token
        session["role"] = role

        # Redirect based on role
        if role == "admin":
            return redirect("/admin/dashboard")
        else:
            return redirect("/chatbot")
    return "Invalid credentials", 401


@app.route('/logout', methods=['GET'])
def gateway_logout():
    token = session.get("token")
    if not token:
        return redirect("/auth")

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{AUTH_SERVICE_URL}/logout", headers=headers)

    session.clear()
    return redirect("/auth")



# ================= PATIENT ROUTES =================

@app.route('/chatbot', methods=['GET'])
def chatbot_interface():
    token = session.get("token")
    if not token:
        return redirect("/auth")

    return render_template("chatbot.html")


@app.route('/submit_query', methods=['POST'])
def submit_query():
    token = session.get("token")
    if not token:
        return jsonify({"error": "Unauthorized"}), 401

    headers = {"Authorization": f"Bearer {token}"}
    payload = {"question": request.form.get("question")}

    response = requests.post(f"{PATIENT_SERVICE_URL}/patient/query", json=payload, headers=headers)
    return jsonify(response.json()), response.status_code


@app.route('/my_queries', methods=['GET'])
def get_my_queries():
    token = session.get("token")
    if not token:
        return jsonify({"error": "Unauthorized"}), 401

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{PATIENT_SERVICE_URL}/patient/my_queries", headers=headers)
    return jsonify(response.json()), response.status_code


# You can similarly add /profile, /update_profile routes if needed

if __name__ == '__main__':
    app.run(port=5000, debug=True, host="0.0.0.0")
