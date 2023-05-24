from django.shortcuts import render, redirect
from .models import Signup,Image,Quiz,Question,Answer,Marks_Of_User
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth  import authenticate,  login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.http import HttpResponse
from .forms import *
import cv2
from django.http import StreamingHttpResponse
from camera import VideoCamera
import csv
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
import numpy as np
from keras.preprocessing import image
import tensorflow as tf
import pickle
from tensorflow import keras

# Create your views here.
filename = r'C:\\Users\\hpw\\Desktop\\project with cnn\\Attendance.csv'

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
    return StreamingHttpResponse(gen(VideoCamera()), content_type='multipart/x-mixed-replace; boundary=frame')
    
@csrf_exempt
def capture_image(request):
    face_classifier = cv2.CascadeClassifier(r"C:\\Users\\hpw\\Desktop\\project with cnn\\Quiz2\\home\\haarcascade_frontalface_default.xml")

    def face_cropped(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        if len(faces) == 0:
            return None
        for (x, y, w, h) in faces:
            cropped_face = img[y:y+h, x:x+w]
        return cropped_face

    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    cropped_face = face_cropped(frame)

    if cropped_face is not None:
        face = cv2.resize(cropped_face, (200, 200))
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        image_path = os.path.join(settings.MEDIA_ROOT, 'captured_image.jpg')
        cv2.imwrite(image_path, face)
        camera.release()
        model = keras.models.load_model(r'C:\\Users\\hpw\\Desktop\\project with cnn\\Quiz2\\classifier_model.h5')
        # Load the ResultMap
        with open(r'C:\\Users\\hpw\\Desktop\\project with cnn\\Quiz2\\ResultsMap.pkl', 'rb') as file:
            ResultMap = pickle.load(file)

        ImagePath=r'C:\\Users\\hpw\\Desktop\\project with cnn\\Quiz2\\media\\captured_image.jpg' #testing image
        test_image=tf.keras.utils.load_img(ImagePath,target_size=(64, 64))
        test_image=tf.keras.utils.img_to_array(test_image)

        test_image=np.expand_dims(test_image,axis=0)
        result=model.predict(test_image,verbose=0)
        if ResultMap[np.argmax(result)] == Login.username:
            login(request,user=authenticate(username=Login.username, password=Login.password))
            return JsonResponse({'redirect_url': '/'})
        else:
            return JsonResponse({'redirect_url': '/login'})
    else:
        camera.release()
        return HttpResponse('No face detected in the captured image.')
    
def stop_video_feed(request): 
    with open(filename, 'r+') as file:
      reader = csv.reader(file)
      for row in reader:
        if not (row):    
            continue
        open(filename,'w+')
        if(row[0] == Login.username.upper()):
            login(request,user=authenticate(username=Login.username, password=Login.password))
            request.session['redirected_to_home'] = True
            return redirect('/')
    request.session['redirected_to_login'] = True
    return render(request,'login.html')

def plot_csv():
    response = HttpResponse(open('Attendance.csv',content_type="text/csv"))
    response['Content-Disposition'] = 'attachment_filename = "Attendance.csv"'
    return response
    

def image_view(request):
	if request.method == 'POST':
		form = ImageForm(request.POST, request.FILES)

		if form.is_valid():
			form.save()
			return render(request,'login.html')
	else:
		form = ImageForm()
	return render(request, 'image_upload.html', {'form': form})


def index(request):
    request.session['redirected_to_login'] = False
    quiz = Quiz.objects.all()
    para = {'quiz' : quiz}
    return render(request, "index.html", para)

@login_required(login_url = '/login')
def quiz(request, myid):
    quiz = Quiz.objects.get(id=myid)
    return render(request, "quiz.html", {'quiz':quiz})

def quiz_data_view(request, myid):
    quiz = Quiz.objects.get(id=myid)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.content)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'time': quiz.time,
    })


def save_quiz_view(request, myid):
    if request.COOKIES.get('myid') is not None:
        questions = []
        data = request.POST
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')
        for k in data_.keys():
            print('key: ', k)
            question = Question.objects.get(content=k)
            questions.append(question)
        user = request.user
        quiz = Quiz.objects.get(id=myid)
        score = 0
        marks = []
        for q in questions:
            a_selected = request.POST.get(q.content)
            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                correct_answer = None
                for a in question_answers:
                    if a_selected == a.content:
                        if a.correct:
                            score += 1
                        correct_answer = a.content
                    elif a.correct:
                        correct_answer = a.content
                marks.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                marks.append({str(q): 'not answered'})

        Marks_Of_User.objects.create(quiz=quiz, user=user, score=score)

        return HttpResponse({'score': score, 'marks':marks})
    
    return HttpResponseRedirect('/results/')

def Signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method=="POST":   
        username = request.POST['username']
        email = request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password = request.POST['password1']
        confirm_password = request.POST['password2']
        
        if password != confirm_password:
            return redirect('/register')
        
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        #user.profile_pic = profile_pic
        user.save()
        return redirect("/image_upload")  
    return render(request, "signup.html")

def Login(request):
    #request.session['redirected_to_login'] = False
    if request.user.is_authenticated:
        return redirect('/')
    if request.method=="POST":
        Login.username = request.POST['username']
        Login.password = request.POST['password']
    
        user = authenticate(username=Login.username, password=Login.password)
        
        if user is not None:
            #login(request, user)
            return render(request,'capture.html')
            #return redirect('/capture')
        else:
            return render(request, "login.html") 
    
    return render(request, "login.html")

def Logout(request):
    logout(request)
    return redirect('/')


def add_quiz(request):
    if request.method=="POST":
        form = QuizForm(data=request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.save()
            obj = form.instance
            return render(request, "add_quiz.html", {'obj':obj})
    else:
        form=QuizForm()
    return render(request, "add_quiz.html", {'form':form})

def add_question(request):
    questions = Question.objects.all()
    questions = Question.objects.filter().order_by('-id')
    if request.method=="POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "add_question.html")
    else:
        form=QuestionForm()
    return render(request, "add_question.html", {'form':form, 'questions':questions})

def delete_question(request, myid):
    question = Question.objects.get(id=myid)
    if request.method == "POST":
        question.delete()
        return redirect('/add_question')
    return render(request, "delete_question.html", {'question':question})


def add_options(request, myid):
    question = Question.objects.get(id=myid)
    QuestionFormSet = inlineformset_factory(Question, Answer, fields=('content','correct', 'question'), extra=4)
    if request.method=="POST":
        formset = QuestionFormSet(request.POST, instance=question)
        if formset.is_valid():
            formset.save()
            alert = True
            return render(request, "add_options.html", {'alert':alert})
    else:
        formset=QuestionFormSet(instance=question)
    return render(request, "add_options.html", {'formset':formset, 'question':question})

def results(request):
    marks = Marks_Of_User.objects.all()
    return render(request, "results.html", {'marks':marks})

def delete_result(request, myid):
    marks = Marks_Of_User.objects.get(id=myid)
    if request.method == "POST":
        marks.delete()
        return redirect('/results')
    return render(request, "delete_result.html", {'marks':marks})