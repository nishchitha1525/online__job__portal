import os
import pandas as pd
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline


# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATASET_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "salary_dataset.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "salary_model.pkl"
)


# ---------------------------------------------------------
# TRAIN MODEL
# ---------------------------------------------------------

def train_salary_model():

    data = pd.read_csv(DATASET_PATH)

    X = data[
        [
            "job_title",
            "experience",
            "education",
            "skills"
        ]
    ]

    y = data["salary"]

    categorical_features = [
        "job_title",
        "education",
        "skills"
    ]

    numerical_features = [
        "experience"
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(
                    handle_unknown="ignore"
                ),
                categorical_features
            ),
            (
                "numerical",
                "passthrough",
                numerical_features
            )
        ]
    )

    model = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor
            ),
            (
                "regressor",
                RandomForestRegressor(
                    n_estimators=100,
                    random_state=42
                )
            )
        ]
    )

    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)

    return model


# ---------------------------------------------------------
# PREDICT SALARY
# ---------------------------------------------------------

def predict_salary(
    job_title,
    experience,
    education,
    skills
):

    if not os.path.exists(MODEL_PATH):
        model = train_salary_model()
    else:
        model = joblib.load(MODEL_PATH)

    input_data = pd.DataFrame(
        [
            {
                "job_title": job_title,
                "experience": float(experience),
                "education": education,
                "skills": skills
            }
        ]
    )

    prediction = model.predict(input_data)

    return round(float(prediction[0]), 2)