from flask import Flask, render_template, request, redirect
from web import *
from db import *
from datetime import datetime
import os
import ast
import threading

app = Flask(__name__)

# Scan execute
def executeScan(uuid, url, enumeration, spidering):

    # Store scan status as running on SQLite
    scanStatus(uuid,'running')

    # Get user options
    proxy = optionGet('proxy')
    payload_file = optionGet('payload_file')

    try:
        # Set Scan object
        scan = Scan(url,proxy)
        # Store INFO results in SQLite
        resultSet(uuid,'info','status',scan.response.status_code)
        resultSet(uuid,'info','reason',scan.response.reason)
        resultSet(uuid,'info','headers',scan.headers)

        # Run Web Heads
        returnSecureHeaders, returnSensitiveHeaders = scan.heads()
        # Store HEADERS results in SQLite
        resultSet(uuid,'headers','rawHeaders',scan.headers)
        resultSet(uuid,'headers','secureHeaders',returnSecureHeaders)
        resultSet(uuid,'headers','sensitiveHeaders',returnSensitiveHeaders)

        # Run Web Method
        returnMethods = scan.method()
        # Store METHODS results in SQLite
        resultSet(uuid,'methods','methods',returnMethods)

        if enumeration == 1:
            enum = scan.enum(payload_file)
            # Store ENUM results in SQLite 
            resultSet(uuid,'enum','directories',enum)
        # Store DETAILS results in SQLite
        date_hour = datetime.now().strftime('%d/%m/%Y %H:%M')
        resultSet(uuid, 'details', 'date', date_hour)
        # Store scan status as completed on SQLite
        scanStatus(uuid,'completed')
    except Exception as error:
        print (error)
        scanStatus(uuid,'failed')

# Home page
@app.route('/')
def home():
    # Return home page with scans in scanGetAll function
    return render_template('home.html', title='My scans', scans=scanGetAll())

# New scan
@app.route('/new', methods=['GET', 'POST'])
def new():

    # If GET request...
    if request.method == 'GET':

        # Return new Scan page
        return render_template('new.html', title='Create a new scan')

    # If POST request...
    if request.method == 'POST':

        # Get request POST form data
        name = request.form['name']
        url = request.form['url']
        enumeration = request.form['enumeration']
        #spidering = request.form['spidering']

        # Store new Scan in SQLite  
        scanSet(name,url,enumeration)

        # Redirect to home page    
        return redirect('/')

# Scan edit
@app.route('/edit/<uuid>', methods=['POST','GET'])
def editScan(uuid):

    # If GET request...
    if request.method == 'GET':
        # Return edit page with selected uuid scan in scanGet function
        return render_template('edit.html', title='Edit', scan=scanGet(uuid))

    # If POST request...
    if request.method == 'POST':

        # Get request POST form data
        name = request.form['name']
        url = request.form['url']
        enumeration = request.form['enumeration']
        spidering = request.form['spidering']

        # Update Scan in SQLite
        scanUpdate(uuid,name,url,enumeration,spidering)

        # Redirect to home page
        return redirect('/')

# Scan delete
@app.route('/delete/<uuid>', methods=['GET'])
def deleteScan(uuid):

    # Delete selected uuid scan in SQLite
    scanDelete(uuid)

    # Redirect to home page
    return redirect('/')

# Start scan
@app.route('/start/<uuid>', methods=['GET'])
def startScan(uuid):

    # Get scan selected uuid scan in SQLite
    scan = scanGet(uuid)

    # Clear all scans results
    resultDelete(uuid)
    uuid = scan['uuid']
    url = scan['url']
    enumeration = scan['enumeration']
    spidering = scan['spidering']
    thread = threading.Thread(target=executeScan, args=(uuid,url,enumeration,spidering))
    thread.start()
    return redirect('/')

@app.route('/results/<uuid>', methods=['POST','GET'])
def resultScan(uuid):
    if request.method == 'GET':
        secureHeaders = ast.literal_eval(resultGet(uuid,'headers','secureHeaders'))
        secure = ['X-Frame-Options', 
                  'X-XSS-Protection',
                  'Content-Security-Policy',
                  'Strict Transport Security',
                  'X-Content-Type-Options',
                  'X-Permitted-Cross-Domain-Policies',
                  'Referrer-Policy',
                  'Expect-CT'
                  'Feature-Policy']
        scan = scanGet(uuid)
        name = scan['name']
        url = scan['url']
        date = resultGet(uuid,'details','date')
        status = resultGet(uuid,'info','status')
        reason = resultGet(uuid,'info','reason')
        headers = ast.literal_eval(resultGet(uuid,'info','headers'))
        sensitiveHeaders = ast.literal_eval(resultGet(uuid,'headers','sensitiveHeaders'))
        methods = ast.literal_eval(resultGet(uuid,'methods','methods'))
        try:
            enum = ast.literal_eval(resultGet(uuid,'enum','directories'))
        except:
            enum = ''
            pass
        return render_template('results.html', title='Results | '+date+'  '+name+' - '+url, name=name, url=url, date=date, status=status, 
        reason=reason, headers=headers, secure=secure, secureHeaders=secureHeaders, 
        sensitiveHeaders=sensitiveHeaders, methods=methods, enum=enum)

@app.route('/configuration', methods=['GET','POST'])
def PayloadsConfiguration():
    if request.method == "GET":
        proxy = optionGet('proxy')
        payload_file = optionGet('payload_file')
        path = os.path.join(os.getcwd(),'payload_files')
        list_of_files = []
        for filename in os.listdir(path):
            list_of_files.append(filename)
        return render_template('configuration.html', title="Configuration",proxy=proxy,
                                file=payload_file,
                                list_of_files = list_of_files)
    if request.method == "POST":
        proxy = request.form['proxy']
        payload_file = request.form['payload_file']
        try:
            file = request.files['upload_file']
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        except:
            pass
        optionUpdate('proxy',proxy)
        optionUpdate('payload_file',payload_file)            
        return redirect('/')

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(),'payload_files')
app.run(host='0.0.0.0', debug=True)