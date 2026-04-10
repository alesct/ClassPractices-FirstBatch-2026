from flask import Flask, jsonify
import my_math

app = Flask(__name__)

@app.route('/api/report/section2')
def get_section_two(): 
    specs, missing = my_math.get_data_info("credit_data.csv")
    
    return jsonify({
        "title": "Data Profiling & Basic Exploration",
        "specs": specs,
        "missing_values": missing
    })

if __name__ == "__main__":
    print("Server starting on http://127.0.0.1:5000")
    app.run(debug=True)