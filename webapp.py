import flask
from flask import render_template, request, redirect, url_for
from backend.datasource import *
import json
import sys

app = flask.Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def homepage():
    majors = DataSource().getMajorList()
    return render_template('homepage.html', majors=majors)

@app.route('/about_the_data')
def about_the_data():
    return render_template('about_the_data.html')

@app.route('/majors')
def majors():
    majors = DataSource().getMajorList()
    return render_template('major.html', majors=majors)

@app.route('/majors/<major>')
def get_major_info(major):
    '''
    this method gets the relevant information for a specific major from datasource.py
    '''
    major_salary = DataSource().getSalary(major)
    major_type_of_institution = DataSource().getMaxInstitutionPopularity(major)[0][0]
    popularity_of_institution = DataSource().getMaxInstitutionPopularity(major)[0][1]
    major_male = DataSource().getMaleAndFemalePopularityPercentage(major)[0]
    major_female = DataSource().getMaleAndFemalePopularityPercentage(major)[1]
    major_popularity = DataSource().getPopularity(major)
    majors_dropdown = DataSource().getMajorList()
    return render_template('each_major.html', major=major, major_salary=major_salary,
                           major_type_of_institution=major_type_of_institution, popularity_of_institution=popularity_of_institution,
                           major_male=major_male, major_female=major_female,  major_popularity=major_popularity, majors=majors_dropdown)

@app.route('/salary')
def salary():
    majors_dropdown = DataSource().getMajorList()
    return render_template('salary.html', majors=majors_dropdown)

@app.route('/salary_results', methods = ['POST'])
def salary_results():
    '''
    this method formats the salary input in the form and checks the input to return appropriate information
    '''
    salary = DataSource().getMaxAndMinSalary()
    database_min = salary[0][1]
    database_max = salary[0][0]
    majors_dropdown = DataSource().getMajorList()
    min = 0
    max = 0
    form_min = request.form['minimum']
    form_max = request.form['maximum']
    if form_min.isdigit() and form_max.isdigit():
        if form_min != '':
            if int(form_min) < database_min:
                min = database_min
            elif int(form_min) > database_max:
                min = database_max
            else:
                min = int(form_min)
        else:
            min = database_min
        if form_max != '':
            if int(form_max) > database_max:
                max = database_max
            elif int(form_max) < database_min:
                max = database_min
            else:
                max = int(form_max)
        else:
            max = database_max
        if min > max:
            min = max
        minSalary = str(min)
        maxSalary = str(max)
        salary_major_list = DataSource().getMajorsBySalary(minSalary, maxSalary)
        salary_string = "Minimum: $" + minSalary + ", Maximum: $" + maxSalary
    else:
        salary_string = "Please input digits only"
        salary_major_list = []
    return render_template('salary.html', salary_output = salary_string, salary_major_list=salary_major_list, majors = majors_dropdown )

@app.route('/popularity')
def popularity():
    majors_dropdown = DataSource().getMajorList()
    return render_template('popularity.html', majors=majors_dropdown)

@app.route('/popularity_results', methods = ['POST'])
def popularity_results():
    '''
    this method formats the popularity input in the form and checks the input to return appropriate information
    '''
    popularity = DataSource().getMaxAndMinPopularity()
    database_min = popularity[0][1]
    database_max = popularity[0][0]
    majors_dropdown = DataSource().getMajorList()
    min = 0
    max = 0
    form_min = request.form['minimum']
    form_max = request.form['maximum']
    if form_min.isdigit() and form_max.isdigit():
        if form_min != '':
            if int(form_min) < database_min:
                min = database_min
            elif int(form_min) > database_max:
                min = database_max
            else:
                min = int(form_min)
        else:
            min = database_min
        if form_max != '':
            if int(form_max) > database_max:
                max = database_max
            elif int(form_max) < database_min:
                max = database_min
            else:
                max = int(form_max)
        else:
            max = database_max
        if min > max:
            min = max
        minPop = str(min)
        maxPop = str(max)
        popularity_major_list = DataSource().getMajorsByPopularity(minPop, maxPop)
        if min > 999:
            string = str(min)
            minPop = string[0] + "," + string[1:]
        else:
            minPop = str(min)
        if max > 999:
            string = str(max)
            maxPop = string[0] + "," + string[1:]
        else:
            maxPop = str(max)
        popularity_string = "Minimum popularity: " + minPop + ",000, Maximum Popularity: " + maxPop + ",000"
    else:
        popularity_string = "Please input digits only"
        popularity_major_list = []
    return render_template('popularity.html', popularity_output = popularity_string, popularity_major_list=popularity_major_list, majors = majors_dropdown )

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)
