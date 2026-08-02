from flask import Flask, render_template, request
from PyPDF2 import PdfReader
import os
import re
app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        print("POST request recieved")
        resume = request.files["resume"]
        print("Filename:",resume.filename)
        filepath=os.path.join("uploads",resume.filename)
        print("Saving to:",filepath)
        resume.save(filepath)
        reader = PdfReader(filepath)
        text = ""
        for page in reader.pages:
          text += page.extract_text()
        email = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        if email:
            email = email[0]
        else:
            email = "Not Found"
        print("Email:", email)
        phone = re.findall(r'\b\d{10}\b', text)
        if phone:
            phone = phone[0]
        else:
            phone = "Not Found"
        print("Phone:", phone)
        lines = text.split("\n")
        name = "Not Found"
        for line in lines:
            if line.strip():
                name = line.strip()
                break
        print("Name:", name)
        print(text)
        required_skills = [
            "Python",
            "Java",
            "SQL",
            "Machine Learning",
            "Git",
            "HTML",
            "CSS",
            "Flask"]
        found_skills = []
        missing_skills = []
        for skill in required_skills:
            if skill.lower() in text.lower():
                found_skills.append(skill)
            else:
                missing_skills.append(skill)
        found_count = len(found_skills)
        total_count = len(required_skills)
        skill_score = (found_count / total_count) * 40
        section_score = 0
        if "education" in text.lower():
            section_score += 20
        if "projects" in text.lower():
            section_score += 20
        if "experience" in text.lower():
            section_score += 20
        score = skill_score + section_score
        if score >= 71:
            strength = "⭐⭐⭐⭐⭐ Excellent"
            bar_color="green"
            feedback = (
            "🎉 Great job! Your resume matches most of the required skills. "
            "You are a strong candidate for this role."
            )
        elif score >= 41:
            strength = "⭐⭐⭐☆☆ Good"
            bar_color="gold"
            feedback = (
                "👍 Good effort! Your resume has a solid foundation. "
                "Adding the missing skills and more projects will improve it."
             )
        else:
            strength = "⭐⭐☆☆☆ Needs Improvement"
            bar_color="red"
            feedback = (
                "⚠️ Your resume needs improvement. "
                "Focus on learning the missing skills and adding projects before applying."
            )
        suggestions = []
        for skill in missing_skills:
            suggestions.append(f"Learn {skill}")
        print("Resume Score:", round(score, 2), "%")
        print("Resume saved successfully!")
        return render_template(
            "index.html",
            message="✅ Resume Uploaded Successfully!",
            score=round(score, 2),
            strength=strength,
            found=found_skills,
            missing=missing_skills,
            suggestions=suggestions,
            bar_color=bar_color,
            feedback=feedback,
            name=name,
            email=email,
            phone=phone
)
        print("Found Skills:", found_skills)
        print("Missing Skills:", missing_skills)
        print("Suggestions:", suggestions)
    return render_template("index.html")
if __name__ == "__main__":
    app.run(debug=True)