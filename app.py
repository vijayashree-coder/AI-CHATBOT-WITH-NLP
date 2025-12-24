from flask import Flask, render_template, request
import nltk
import string
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('wordnet')

app = Flask(__name__)
lemmatizer = WordNetLemmatizer()

# Career knowledge base
career_data = {
    "data scientist": ["python", "machine learning", "statistics", "sql"],
    "data analyst": ["python", "sql", "excel", "power bi"],
    "web developer": ["html", "css", "javascript", "python"],
    "software engineer": ["python", "java", "data structures"],
    "ml engineer": ["python", "machine learning", "deep learning"]
}

def preprocess(text):
    tokens = nltk.word_tokenize(text.lower())
    return [lemmatizer.lemmatize(word) for word in tokens if word not in string.punctuation]

def recommend_career(user_skills, interest):
    user_skills = preprocess(user_skills)
    interest = interest.lower()

    for career, required_skills in career_data.items():
        if interest in career:
            missing = set(required_skills) - set(user_skills)
            return career.title(), ", ".join(missing)

    # Default recommendation
    career = list(career_data.keys())[0]
    missing = set(career_data[career]) - set(user_skills)
    return career.title(), ", ".join(missing)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        degree = request.form["degree"]
        skills = request.form["skills"]
        interest = request.form["interest"]
        experience = request.form["experience"]

        role, missing_skills = recommend_career(skills, interest)

        tip = "Add internships and projects to your resume." if experience == "Fresher" \
              else "Highlight work experience and achievements."

        result = {
            "role": role,
            "missing": missing_skills if missing_skills else "No major skill gaps!",
            "tip": tip
        }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
