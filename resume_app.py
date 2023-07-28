import streamlit as st
import string
from resume_parser import resumeparse
from pyresparser import ResumeParser

def process_resume_matching(resume_path, requirement_path):
    data = ResumeParser(resume_path).get_extracted_data()
    have_skills = [i for i in data['skills']]

    req_skills = resumeparse.read_file(requirement_path)
    skills = [i for i in req_skills['skills']]

    punc = string.punctuation
    text_p = " ".join([char for char in have_skills if char not in punc])

    alph = list(string.ascii_lowercase)
    alph.append(' ')
    alph.append('+')

    have_skills_lower = []
    for i in have_skills:
        w = ''
        for j in i:
            try:
                j = j.lower()
            except:
                pass
            if j in alph:
                w = w + j
            else:
                pass

        have_skills_lower.append(w.lower().lstrip())
    have_skills_set = set(have_skills_lower)
    have_skills_lower = list(have_skills_set)

    skills_lower = [i.lower() for i in skills]
    skill_set = set(skills_lower)
    skills_lower = list(skill_set)

    count = 0
    matched_skills = []
    for i in have_skills_lower:
        if i in skills_lower:
            matched_skills.append(i)
            count += 1
    per = (count / len(skills_lower)) * 100
    return per, matched_skills

def main():
    st.title("Skill Matching from Resume")
    st.write("Upload your resume and a requirement file to check how many skills you've matched.")

    # File upload
    resume_input = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
    requirement_input = st.file_uploader("Upload the requirement file (PDF)", type=["pdf"])

    if resume_input and requirement_input:
        resume_path = "user_resume.pdf"
        requirement_path = "user_requirement.pdf"

        with open(resume_path, "wb") as f:
            f.write(resume_input.read())

        with open(requirement_path, "wb") as f:
            f.write(requirement_input.read())

        matching_percentage, matched_skills = process_resume_matching(resume_path, requirement_path)

        st.write(f"Matching Skills: {', '.join(matched_skills)}")
        st.write(f"Matching Percentage: {matching_percentage:.2f}%")

if __name__ == "__main__":
    main()