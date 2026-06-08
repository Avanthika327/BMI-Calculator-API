from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# ==========================================
# TASK 4: Pure Business Logic Function 🧠
# ==========================================
def calculate_bmi_logic(weight, height):
    # Core mathematical formula
    bmi = weight / (height ** 2)
    bmi = round(bmi, 2)
    
    # Category logic conditions
    if bmi < 18.5:
        category = "Underweight 🦴"
    elif 18.5 <= bmi < 24.9:
        category = "Normal weight ✅"
    elif 25 <= bmi < 29.9:
        category = "Overweight ⚠️"
    else:
        category = "Obesity 🚨"
        
    return {
        "bmi": bmi,
        "category": category
    }

# ==========================================
# TASK 5: Flask REST API Route 🌐
# ==========================================
@app.route('/')
def home():
    return render_template('bmi.html')

@app.route('/calculate-bmi', methods=['POST'])
def calculate_bmi():
    data = request.get_json()
    
    # Input parameter validation
    if not data or 'name' not in data or 'weight' not in data or 'height' not in data:
        return jsonify({"error": "Missing parameters!"}), 400
    
    try:
        name = data['name']
        weight = float(data['weight'])
        height = float(data['height'])
        
        # Inga namma Task 4 function-ah call panni result vaangrom! 🎯
        result = calculate_bmi_logic(weight, height)
        
        return jsonify({
            "name": name,
            "bmi": result["bmi"],
            "category": result["category"]
        })
        
    except ValueError:
        return jsonify({"error": "Invalid input values!"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5002)