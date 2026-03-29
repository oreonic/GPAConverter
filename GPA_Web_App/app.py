from flask import Flask, render_template, request

app = Flask(__name__)

# OLSAS conversion scale (simplified for Waterloo)
GPA_SCALE = [(90, 4.00), (85, 3.90), (80, 3.70), (77, 3.30), (73, 3.00), (70, 2.70),
             (67, 2.30), (63, 2.00), (60, 1.70), (57, 1.30), (53, 1.00), (50, 0.70)]

LAW_SCHOOLS = [('UofT', 3.90), ('McGill', 3.80), ('UBC', 3.75), ('Osgoode', 3.70),
                ('Western', 3.70), ('Queens', 3.70), ('uOttawa', 3.70),
                ('uAlberta', 3.80), ('Dalhousie', 3.70), ('Windsor', 3.12)]

def calculate_gpa(courses):
    total_weighted_points = 0
    total_weight = 0
    for course in courses:
        try:
            grade = float(course['grade'])
            weight = float(course['weight'])
            course_gpa = 0.0
            for threshold, gpa_val in GPA_SCALE:
                if grade >= threshold:
                    course_gpa = gpa_val
                    break
            total_weighted_points += (course_gpa * weight)
            total_weight += weight
        except (ValueError, TypeError):
            continue
    if total_weight == 0: return 0
    return round(total_weighted_points / total_weight, 2)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    eligible_schools = []
    if request.method == 'POST':
        grades = request.form.getlist('grade')
        weights = request.form.getlist('weight')
        courses = []
        for g, w in zip(grades, weights):
            if g and w:
                courses.append({'grade': g, 'weight': w})
        if courses:
            result = calculate_gpa(courses)
            eligible_schools = [s for s, a in LAW_SCHOOLS if result >= a]
    return render_template('index.html', result=result, schools=eligible_schools)

if __name__ == '__main__':
    app.run(debug=True)