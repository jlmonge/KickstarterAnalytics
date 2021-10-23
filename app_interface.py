import os
import json
import io
from flask import Flask, render_template, request, redirect, url_for, flash #imports from flask
from userInput import exampleForm, kickStarterForm # import forms here. We import these to keep ourselves organized.
from category_searches import highest_usd_pledged_search#functions from the category_searches file. Use them to search a specific category
from add_function import add_to_json
# notice here that index.html does not need to be passed in. That is because it is in the templates folder
# In the future we might use templates to reduce redundant html code.

# instructions to upload 
# py -m venv env
# env/Scripts/Activate
# export FLASK_APP=app_interface.py
# export FLASK_DEBUG=1
# flask run

# GLOBAL VARIABLES
file_name =  'ks-projects-201801.json'
data = list()

def search_helper(key, method="GET"):
    if method == 'POST': # will only run below code if client is posting
        # below code: exampleForm is just an imported class.
        # request.form looks at the html in the render_template function.
        # It finds the input given the name 'nm' and returns the user input.
        # form = exampleForm(request.form["id"])
        value = request.form.get(key)
        if not value or value.isspace():
            return redirect(request.url)
        #with open('test.txt', 'w') as f:   # needed once we edit values in the json file
            #f.write(id)
        return redirect(url_for('results', key=key, value=value))
    return render_template(f'search-{key.lower()}.html')

app = Flask(__name__) # neccessary for flask

@app.before_first_request
def loadJsonFile():
    file = os.path.join(app.static_folder, file_name) # location of json file
    with open(file ,encoding='utf-8-sig') as json_file:
        global data 
        data = json.load(json_file) # json --> dictionary

@app.route("/") # creates "/" directory for homepage
def index():
    return render_template('index.html')

@app.route("/id", methods=['POST','GET']) # creates "/" directory and accepts 'POST' and 'GET' Requests
def search_ID():
    return search_helper('ID', request.method)

@app.route("/name", methods=['POST','GET']) # creates "/" directory and accepts 'POST' and 'GET' Requests
def search_name():
    return search_helper('name', request.method)

@app.route("/category", methods=['POST','GET']) # creates "/" directory and accepts 'POST' and 'GET' Requests
def search_category():
    return search_helper('category', request.method)

@app.route("/state", methods=['POST','GET']) # creates "/" directory and accepts 'POST' and 'GET' Requests
def search_state():
    return search_helper('state', request.method)

@app.route("/launched", methods=['POST','GET']) # creates "/" directory and accepts 'POST' and 'GET' Requests
def search_month():
    return search_helper('launched', request.method)

@app.route("/update_database")
def update_database():
    file = os.path.join(app.static_folder, file_name) # location of json file
    with open(file,"r+" ,encoding='utf-8-sig') as json_file:
        json_file.seek(0)
        json.dump(data, json_file, indent=4)
        json_file.truncate()
    return render_template('sentanceMessage.html', message = "Successfully updated database file")

@app.route("/import_file", methods=['POST','GET'])
def import_file():
    if request.method == 'POST':
        if 'passed_file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files["passed_file"]
        if file:#and allowed_file(request.url)
            file_path = os.path.join(app.static_folder, file.filename)
            file.save(file_path) 
            with open(file_path, encoding='utf-8-sig') as json_file:
                global data
                data = json.load(json_file) # json --> dictionary
            global file_name
            file_name = file.filename
            return redirect(request.url)
    return render_template("import_file.html")

@app.route("/search/key=<key>&value=<value>")
def results(key, value):
    #file = os.path.join(app.static_folder, file_name) # location of json file
    projects = [] # the project(s) being looked for
    #with open(file, encoding='utf-8-sig') as json_file:
        #data = json.load(json_file) # json --> dictionary
    for proj in data:
        if key == 'ID' and value == proj.get(key):
            projects.append(proj)
        elif (key == 'name' or key == 'state' or key == 'category' or key == 'launched') and value.lower() in proj.get(key).lower():
            projects.append(proj)
    return render_template('results.html', projects=projects)

@app.route("/search",methods=['POST','GET'])
def search():
    if request.method == 'POST': # will only run below code if client is posting
        choiceSearch = request.form.get('choice')
        if not choiceSearch or choiceSearch.isspace():
            return redirect(request.url)
        #return redirect(url_for('get_id', id=id))
    return render_template('searches.html')


@app.route("/delete",methods=['POST','GET'])
def delete_kickstarter():
    if request.method == 'POST': # will only run below code if client is posting
        deleteChoice = request.form.get('id_to_delete')
        if not deleteChoice or deleteChoice.isspace():
            return redirect(request.url)
        return redirect(url_for('do_delete', id_to_delete=deleteChoice))
    return render_template('deleteKickstarter.html')

@app.route("/delete/<id_to_delete>")
def do_delete(id_to_delete):
    #databaseFile = os.path.join(app.static_folder, file_name)
    #with open(databaseFile, "r+") as file:
    #with open(databaseFile, "r+",encoding='utf-8-sig') as file:
        located = False
        pos = 0
        #data = json.load(file) # json --> dictionary
        #data = json.load(file)
        for i in data:
            if i['ID'] == id_to_delete:
                located = True
                break
            else:
                pos += 1
        if located:
            data.pop(pos)
            successMessage = "Project %s was deleted successfully."%id_to_delete
            return render_template('sentanceMessage.html',message = successMessage)
        else:
            errorMessage = "Error: Project %s could not be found!"%id_to_delete
            return render_template('sentanceMessage.html',message = errorMessage)

@app.route("/add",methods=['POST','GET'])#NOT WORKING
def add_kickstarter():
    if request.method == 'POST': # will only run below code if client is posting
        ksToAdd = kickStarterForm(request.form.get('id'),request.form.get('name'),request.form.get('category'),request.form.get('main_category'),request.form.get('currency'),
        request.form.get('deadline'),request.form.get('goal'),request.form.get('date_launched'),request.form.get('time_launched'),request.form.get('number_pledged'),request.form.get('state'),
        request.form.get('number_backers'), request.form.get('country'), request.form.get('amount_usd_pledged'), request.form.get('amount_usd_pledged_real'))      
        if not len(ksToAdd.error_msgs) == 0:
            return render_template('sentanceMessage.html',message = "Error on one or more field")
        
        add_to_json(data,ksToAdd.id,ksToAdd.name,ksToAdd.category,ksToAdd.main_category,ksToAdd.currency,ksToAdd.deadline,ksToAdd.goal,ksToAdd.date_launched,
            ksToAdd.number_pledged,ksToAdd.state,ksToAdd.number_backers,ksToAdd.country,ksToAdd.amount_usd_pledged,ksToAdd.amount_usd_pledged_real)
        return render_template('sentanceMessage.html',message = "Successfully added kickstarter "+ksToAdd.name)
    return render_template('addKickstarter.html')

@app.route("/edit", methods=['POST','GET'])
def edit_project():
    if request.method == 'POST':
        id = request.form.get('id_to_edit')
        # these if statements prevent flask errors when any new value is left blank
        if not id or id.isspace():
            return redirect(request.url)
        new_id = request.form.get('new_id')
        if not new_id:
            new_id = '\n'
        new_name = request.form.get('new_name')
        if not new_name:
            new_name = '\n'
        new_category = request.form.get('new_category')
        if not new_category:
            new_category = '\n'
        new_main_category = request.form.get('new_main_category')
        if not new_main_category:
            new_main_category = '\n'
        new_currency = request.form.get('new_currency')
        if not new_currency:
            new_currency = '\n'
        new_deadline = request.form.get('new_deadline')
        if not new_deadline:
            new_deadline = '\n'
        new_goal = request.form.get('new_goal')
        if not new_goal:
            new_goal = '\n'
        new_launched = request.form.get('new_launched')
        # slicing is done to match the format of the rest of the launched values
        new_launched = new_launched[:10] + " " + new_launched[11:]
        if not new_launched:
            new_launched = '\n'
        new_pledged = request.form.get('new_pledged')
        if not new_pledged:
            new_pledged = '\n'
        new_state = request.form.get('new_state')
        if not new_state:
            new_state = '\n'
        new_backers = request.form.get('new_backers')
        if not new_backers:
            new_backers = '\n'
        new_country = request.form.get('new_country')
        if not new_country:
            new_country = '\n'
        return redirect(url_for('do_edit', id=id, new_id=new_id, new_name=new_name, new_category=new_category,
            new_main_category=new_main_category, new_currency=new_currency, new_deadline=new_deadline,
            new_goal=new_goal, new_launched=new_launched, new_pledged=new_pledged, new_state=new_state,
            new_backers=new_backers, new_country=new_country))
    return render_template('edit.html')

@app.route('''/edit/id=<id>&new_id=<new_id>&new_name=<new_name>&new_category=<new_category>
    &new_main_category=<new_main_category>&new_currency=<new_currency>&new_deadline=<new_deadline>
    &new_goal=<new_goal>&new_launched=<new_launched>&new_pledged=<new_pledged>&new_state=<new_state>
    &new_backers=<new_backers>&new_country=<new_country>''', methods=['POST','GET'])
def do_edit(id, new_id, new_name, new_category, new_main_category, new_currency, new_deadline, new_goal, 
    new_launched, new_pledged, new_state, new_backers, new_country):
    #file = os.path.join(app.static_folder, file_name) # location of json file
    projectFound = False # the project being looked for
    #with open(file, 'r+', encoding='utf-8-sig') as json_file:
        #data = json.load(json_file) # json --> dictionary
    for proj in data:
        if id == proj.get('ID'):
            projectFound = True
            # these if statements prevent flask errors when any new value is left blank
            if new_id != '\n':
                proj['ID'] = new_id 
            if new_name != '\n':
                proj['name'] = new_name
            if new_category != '\n':
                proj['category'] = new_category
            if new_main_category != '\n':
                proj['main_category'] = new_main_category
            if new_currency != '\n':
                proj['currency'] = new_currency
            if new_deadline != '\n':
                proj['deadline'] = new_deadline
            if new_goal != '\n':
                proj['goal'] = new_goal
            if new_launched != '\n':
                proj['launched'] = new_launched
            if new_pledged != '\n':
                proj['pledged'] = new_pledged
            if new_state != '\n':
                proj['state'] = new_state
            if new_backers != '\n':
                proj['backers'] = new_backers
            if new_country != '\n':
                proj['country'] = new_country
            break
    if not projectFound:
        return render_template('sentanceMessage.html',message = "Project not found")
    '''
    with open(file, 'w', encoding='utf-8-sig') as json_file:
        json.dump(data, json_file, indent=4)
    
    print(proj)
    print(new_id, new_name, new_category, new_main_category, new_currency, new_deadline, new_goal, new_launched, \
        new_pledged, new_state, new_backers, new_country)
    print(proj['ID'], proj['name'], proj['category'], proj['main_category'], proj['currency'], proj['deadline'], \
        proj['goal'], proj['launched'], proj['pledged'], proj['state'], proj['backers'], proj['country'])
    '''
    return render_template('edit-success.html', project=proj)




'''
@app.route("/id/<id>/edit") # needed to edit later on
def set_id()
'''