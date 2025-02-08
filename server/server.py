from flask import Flask, request, jsonify, render_template, send_from_directory
import util
import os

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict_stroke', methods=['POST', 'GET'])
def predict_stroke():
    try:
        # Extract form data
        gender = int(request.form['gender'])
        age = int(request.form['age'])
        hypertension = int(request.form['hypertension'])
        heart_disease = int(request.form['heart_disease'])
        ever_married = int(request.form['ever_married'])
        work_type = int(request.form['work_type'])
        Residence_type = int(request.form['Residence_type'])
        avg_glucose_level = float(request.form['avg_glucose_level'])
        bmi = float(request.form['bmi'])
        smoking_status = int(request.form['smoking_status'])

        # Predict stroke
        estimated_stroke = util.get_prediction(
            gender, age, hypertension, heart_disease, ever_married,
            work_type, Residence_type, avg_glucose_level, bmi, smoking_status
        )

        # Convert NumPy int64 to Python int
        estimated_stroke = int(estimated_stroke)

        # Create response
        response = jsonify({
            'status': 'success',
            'stroke': estimated_stroke
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    except KeyError as e:
        return jsonify({'error': f'Missing parameter: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'error': 'Invalid input data'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    print("Starting Python Flask Server For Stroke Prediction...")
    try:
        util.load_saved_artifacts()
    except Exception as e:
        print(f"Error loading artifacts: {str(e)}")
        exit(1)

    app.run(debug=True)  # Use debug=True for development