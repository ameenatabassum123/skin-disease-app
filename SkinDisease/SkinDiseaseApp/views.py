from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import pymysql
from django.http import HttpResponse
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import seaborn as sns
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import  MaxPooling2D
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.models import model_from_json
import pickle
import os
import matplotlib.pyplot as plt
from django.core.files.storage import FileSystemStorage
import cv2
from django.conf import settings

global cnn_algorithm, X_train, X_test, y_train, y_test
class_labels = ['Actinic Keratosis','Basal Cell Carcinoma','Dermatofibroma','Melanoma','Nevus','Pigmented Benign Keratosis',
                'Seborrheic Keratosis','Squamous Cell Carcinoma','Vascular Lesion']

def DiseasePrediction(request):
    if request.method == 'GET':
        return render(request, 'DiseasePrediction.html', {})

def DiseasePredictionAction(request):
    if request.method == 'POST' and request.FILES.get('t1'):
        try:
            # Load the model
            with open(os.path.join(settings.BASE_DIR, 'model', 'model.json'), "r") as json_file:
                loaded_model_json = json_file.read()
                classifier = model_from_json(loaded_model_json)
            json_file.close()    
            classifier.load_weights(os.path.join(settings.BASE_DIR, "model", "model_weights.h5"))
            
            # Process the uploaded image
            myfile = request.FILES['t1']
            fs = FileSystemStorage()
            filename = fs.save('samples/test.png', myfile)
            image_path = os.path.join(settings.BASE_DIR, 'SkinDiseaseApp', 'static', filename)
            
            image = cv2.imread(image_path)
            if image is None:
                return render(request, 'DiseasePrediction.html', {'error': 'Could not process the image. Please try another image.'})
                
            img = cv2.resize(image, (32,32))
            im2arr = np.array(img)
            im2arr = im2arr.reshape(1,32,32,3)
            img = np.asarray(im2arr)
            img = img.astype('float32')
            img = img/255
            
            preds = classifier.predict(img)
            predict = np.argmax(preds)
            
            # Clean up the temporary file
            if os.path.exists(image_path):
                os.remove(image_path)
            
            # Return the result
            result = class_labels[predict]
            confidence = np.max(preds) * 100
            
            context = {
                'result': result,
                'confidence': f"{confidence:.2f}%",
                'confidence_value': confidence,
            }
            
            return render(request, 'DiseasePrediction.html', context)
        except Exception as e:
            return render(request, 'DiseasePrediction.html', {'error': f'Error processing image: {str(e)}'})

def CNNtestPrediction(name, classifier, X_test, y_test):
    predict = classifier.predict(X_test)
    predict = np.argmax(predict, axis=1)
    y_test = np.argmax(y_test, axis=1)
    p = precision_score(y_test, predict,average='macro') * 100
    r = recall_score(y_test, predict,average='macro') * 100
    f = f1_score(y_test, predict,average='macro') * 100
    a = accuracy_score(y_test,predict)*100
    output = '<table border=1 align=center><tr><th><font size="" color="black">Algorithm Name</th><th><font size="" color="black">Accuracy</th>'
    output += '<th><font size="" color="black">Precision</th><th><font size="" color="black">Recall</th><th><font size="" color="black">FScore</th></tr>'
    output += '<tr><td><font size="" color="black">'+name+'</td>'
    output += '<td><font size="" color="black">'+str(a)+'</td>'
    output += '<td><font size="" color="black">'+str(p)+'</td>'
    output += '<td><font size="" color="black">'+str(r)+'</td>'
    output += '<td><font size="" color="black">'+str(f)+'</td></tr>'
    conf_matrix = confusion_matrix(y_test, predict) 
    return conf_matrix, output 

def runCNN(request):
    if request.method == 'GET':
        try:
            global cnn_algorithm, X_train, X_test, y_train, y_test
            X = np.load(os.path.join(settings.BASE_DIR, 'model', 'X.txt.npy'))
            Y = np.load(os.path.join(settings.BASE_DIR, 'model', 'Y.txt.npy'))
            X = X.astype('float32')
            X = X/255
            indices = np.arange(X.shape[0])
            np.random.shuffle(indices)
            X = X[indices]
            Y = Y[indices]
            Y = to_categorical(Y)
            X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)
            
            if os.path.exists(os.path.join(settings.BASE_DIR, 'model', 'model.json')):
                with open(os.path.join(settings.BASE_DIR, 'model', 'model.json'), "r") as json_file:
                    loaded_model_json = json_file.read()
                    classifier = model_from_json(loaded_model_json)
                json_file.close()    
                classifier.load_weights(os.path.join(settings.BASE_DIR, "model", "model_weights.h5"))
            else:
                classifier = Sequential()
                #defining convolution neural network layer with 32 layers to filter dataset features 32 times and then max pooling will collect all important features
                classifier.add(Conv2D(32, (3, 3), input_shape = (32, 32, 3), activation = 'relu'))
                #pooling layer to collect filtered features
                classifier.add(MaxPooling2D(pool_size = (2, 2)))
                #defining another layer with 32 filters
                classifier.add(Conv2D(32, (3, 3), activation = 'relu'))
                classifier.add(MaxPooling2D(pool_size = (2, 2)))
                classifier.add(Flatten())
                classifier.add(Dense(256, activation = 'relu'))
                classifier.add(Dense(y_train.shape[1], activation = 'softmax'))
                #now compiling the model
                classifier.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
                #now training CNN model with X and Y array data
                hist = classifier.fit(X, Y, batch_size=8, epochs=50, shuffle=True, verbose=2, validation_data=(X_test, y_test))
                classifier.save_weights(os.path.join(settings.BASE_DIR, 'model', 'cnn_model_weights.h5'))            
                model_json = classifier.to_json()
                with open(os.path.join(settings.BASE_DIR, "model", "cnn_model.json"), "w") as json_file:
                    json_file.write(model_json)
                json_file.close()
            
            cnn_algorithm = classifier    
            conf_matrix, output = CNNtestPrediction("CNN Skin Disease Classification",classifier,X_test,y_test)
            context= {'data':output}
            
            # For web deployment, we'll return the results as HTML instead of showing a plot
            return render(request, 'ViewOutput.html', context)
        except Exception as e:
            return render(request, 'ViewOutput.html', {'error': f'Error running CNN: {str(e)}'})

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})   

def Signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        contact = request.POST.get('contact', False)
        email = request.POST.get('email', False)
        address = request.POST.get('address', False)
        output = "none"
        
        try:
            con = pymysql.connect(
                host=os.environ.get('DATABASE_HOST', '127.0.0.1'),
                port=int(os.environ.get('DATABASE_PORT', 3306)),
                user=os.environ.get('DATABASE_USER', 'root'),
                password=os.environ.get('DATABASE_PASSWORD', 'root'),
                database=os.environ.get('DATABASE_NAME', 'skindisease'),
                charset='utf8'
            )
            with con:
                cur = con.cursor()
                cur.execute("select username FROM register")
                rows = cur.fetchall()
                for row in rows:
                    if row[0] == username:
                        output = username+" Username already exists"
                        break
            if output == "none":
                db_connection = pymysql.connect(
                    host=os.environ.get('DATABASE_HOST', '127.0.0.1'),
                    port=int(os.environ.get('DATABASE_PORT', 3306)),
                    user=os.environ.get('DATABASE_USER', 'root'),
                    password=os.environ.get('DATABASE_PASSWORD', 'root'),
                    database=os.environ.get('DATABASE_NAME', 'skindisease'),
                    charset='utf8'
                )
                db_cursor = db_connection.cursor()
                student_sql_query = "INSERT INTO register(username,password,contact,email,address) VALUES(%s,%s,%s,%s,%s)"
                db_cursor.execute(student_sql_query, (username, password, contact, email, address))
                db_connection.commit()
                if db_cursor.rowcount == 1:
                    output = "success"
            if output == "success":
                context= {'data':'Signup Process Completed'}
                return render(request, 'Register.html', context)
            else:
                context= {'data':'Username already exists'}
                return render(request, 'Register.html', context)
        except Exception as e:
            context= {'data':f'Error during signup: {str(e)}'}
            return render(request, 'Register.html', context)

def UserLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        index = 0
        
        try:
            con = pymysql.connect(
                host=os.environ.get('DATABASE_HOST', '127.0.0.1'),
                port=int(os.environ.get('DATABASE_PORT', 3306)),
                user=os.environ.get('DATABASE_USER', 'root'),
                password=os.environ.get('DATABASE_PASSWORD', 'root'),
                database=os.environ.get('DATABASE_NAME', 'skindisease'),
                charset='utf8'
            )
            with con:
                cur = con.cursor()
                cur.execute("select * FROM register")
                rows = cur.fetchall()
                for row in rows:
                    if row[0] == username and row[1] == password:
                        index = 1
                        break
            if index == 1:
                context= {'data':'welcome '+username}
                return render(request, 'UserScreen.html', context)
            if index == 0:
                context= {'data':'Invalid login details'}
                return render(request, 'Login.html', context)
        except Exception as e:
            context= {'data':f'Error during login: {str(e)}'}
            return render(request, 'Login.html', context)
