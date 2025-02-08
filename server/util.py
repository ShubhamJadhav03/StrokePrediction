import pickle
import json
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

__data_columns = None
__model = None

def get_prediction(gender, age, hypertension, heart_disease, ever_married, work_type, Residence_type, avg_glucose_level, bmi, smoking_status):
    try:
        x = np.zeros(len(__data_columns))
        x[0] = gender
        x[1] = age
        x[2] = hypertension
        x[3] = heart_disease
        x[4] = ever_married
        x[5] = work_type
        x[6] = Residence_type
        x[7] = avg_glucose_level
        x[8] = bmi
        x[9] = smoking_status

        return __model.predict([x])[0]
    except Exception as e:
        logging.error(f"Error in get_prediction: {str(e)}")
        raise

def load_saved_artifacts():
    global __data_columns
    global __model

    try:
        logging.info("Loading saved artifacts...start")
        with open("./artifacts/columns.json", "r") as f:
            __data_columns = json.load(f)['data_columns']

        if __model is None:
            with open("./artifacts/stroke_prediction_model.pickle", "rb") as f:
                __model = pickle.load(f)

        logging.info("Loading saved artifacts...done")
    except FileNotFoundError as e:
        logging.error(f"File not found: {str(e)}")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {str(e)}")
        raise
    except pickle.UnpicklingError as e:
        logging.error(f"Error unpickling model: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise

def get_data_columns():
    return __data_columns

if __name__ == '__main__':
    load_saved_artifacts()