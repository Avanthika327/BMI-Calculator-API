from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Grade Calculator</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f9; color: #333; }
        .container { max-width: 500px; background: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: auto; }
        h2 { text-align: center; color: #007bff; }
        label { font-weight: bold; display: block; margin-top: 15px; }
        input { display: block; margin: 8px 0; padding: 10px; width: 95%; border: 1px solid #ccc; border-radius: 5px; font-size: 14px; }
        button { background: #007bff; color: white; border: none; padding: 12px; width: 100%; border-radius: 5px; cursor: pointer; font-size: 16px; margin-top: 15px; font-weight: bold; }
        button:hover { background: #0056b3; }
        #result { margin-top: 20px; font-weight: bold; background: #e9ecef; padding: 15px; border-radius: 5px; white-space: pre-line; border-left: 5px solid #007bff; font-size: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Student Grade Calculator</h2>
        <label>Student Name:</label>
        <input type="text" id="name" placeholder="E.g., Asha">
        
        <label>Marks (comma separated):</label>
        <input type="text" id="marks" placeholder="E.g., 95,92,98">
        
        <button onclick="calculate()">Calculate Grade</button>
        <div id="result" style="display:none;"></div>
    </div>

    <script>
        function calculate() {
            let name = document.getElementById('name').value;
            let marksStr = document.getElementById('marks').value;
            if(!name || !marksStr) { alert("Please fill all fields!"); return; }
            let marks = marksStr.split(',').map(Number);
            
            fetch('/calculate-grades', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ "students": [{ "name": name, "marks": marks }] })
            })
            .then(res => res.json())
            .then(data => {
                let resDiv = document.getElementById('result');
                resDiv.style.display = "block";
                let resData = data.output[0];
                resDiv.innerText = `👤 Student Name: ${resData.name}\\n📊 Average Marks: ${resData.average}%\\n🏅 Final Grade: ${resData.grade}`;
            });
        }
    </script>
</body>
</html>
"""

@app.route('/my-ui')
def my_ui():
    return render_template_string(HTML_TEMPLATE)

@app.route('/calculate-grades', methods=['POST'])
def calculate_grades():
    data = request.get_json()
    students = data.get('students', [])
    output = []
    
    for s in students:
        marks = s.get('marks', [])
        avg = sum(marks) / len(marks) if marks else 0
        
        # Unga assignment-oda exact automatic New Grade Logic!
        if avg >= 95:
            grade = "A+"
        elif avg >= 90:
            grade = "A"
        elif avg >= 75:
            grade = "B"
        elif avg >= 60:
            grade = "C"
        else:
            grade = "D"
            
        output.append({
            "name": s.get('name'),
            "average": round(avg, 2),
            "grade": grade
        })
        
    return jsonify({"output": output})

if __name__ == '__main__':
    app.run(port=5000, debug=True)