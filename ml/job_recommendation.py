import os
import pandas as pd


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATASET_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "jobs.csv"
)


def recommend_jobs(skills, top_n=5):

    data = pd.read_csv(DATASET_PATH)

    seeker_skills = set(
        skill.strip().lower()
        for skill in skills.split()
    )

    recommendations = []

    for _, job in data.iterrows():

        job_skills = set(
            skill.strip().lower()
            for skill in str(job["skills"]).split()
        )

        matched_skills = seeker_skills.intersection(job_skills)

        if len(job_skills) > 0:
            match_percentage = (
                len(matched_skills) / len(job_skills)
            ) * 100
        else:
            match_percentage = 0

        if match_percentage > 0:
            recommendations.append({
                "title": job["title"],
                "company": job["company"],
                "location": job["location"],
                "salary": job["salary"],
                "skills": job["skills"],
                "description": job["description"],
                "match_percentage": round(
                    match_percentage,
                    2
                )
            })

    recommendations.sort(
        key=lambda x: x["match_percentage"],
        reverse=True
    )

    return recommendations[:top_n]