from django.shortcuts import render, redirect
from .models import Signup,Image,Quiz,Question,Answer,Marks_Of_User
from django.http import JsonResponse
from django.contrib.auth  import authenticate,  login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.http import HttpResponse
from .forms import *
from django.http import StreamingHttpResponse
from camera import VideoCamera
import csv
from datetime import datetime
# Create your views here.
filename = r'C:\\Users\\hpw\\Desktop\\akanksha\\Attendance.csv'

# def capture(request):
#     with open(filename, 'r') as file:
#       reader = csv.reader(file)
#       for row in reader:
#         time_str = row[1]  # assuming the time is in the second column
#         time_obj = datetime.strptime(time_str, '%H:%M:%S')  # convert string to datetime object
#         now = datetime.now()  # get current time
#         if time_obj.time() == now.time():  # compare time only (not date)
#             if(row[0] == Login.username):
#                 return redirect('/')
#         else:
#             return HttpResponse('Ullu banaya bada maja aaya')
#     # if(request.method == "POST"):
#     #      return redirect('/')
#     # #print(Login.username)
#     # #print(Login.username)
#     return render(request,'capture.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
    try:
          return StreamingHttpResponse(gen(VideoCamera()), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass

def stop_video_feed(request):
    # Add any code to stop the video feed here
    print("Starting")
    with open(filename, 'r+') as file:
      reader = csv.reader(file)
      #file.truncate()
      
      for row in reader:
        if not (row):    
            continue
        time_str = row[1]  # assuming the time is in the second column
        print(time_str+"I am time str")
        time_obj = datetime.strptime(time_str, '%H:%M:%S')  # convert string to datetime object
        #print(str(time_obj)+"I am time obj")
        print("Go on 1")
        now = datetime.now()  # get current time
        #print(str(now)+"I am now")
        open(filename,'w+')
        print("Go on")

        if(time_obj.time() <= now.time() ):  # compare time only (not date)
            print("This is working")
            if(row[0] == Login.username.upper()):
                print("Something is Working")
                # f = open(filename, "w+")
                # f.close()

                return redirect('/')
    #return render(request,'index.html')
    # f = open(filename, "w+")
    # f.close()
  
    return render(request,'login.html')

def plot_csv():
    response = HttpResponse(open('Attendance.csv',content_type="text/csv"))
    response['Content-Disposition'] = 'attachment_filename = "Attendance.csv"'
    return response
    # return send_file('Attendance.csv',
    #                  mimetype='text/csv',
    #                  attachment_filename='Attendance.csv',
    #                  as_attachment=True)

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
    if request.is_ajax():
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
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.content)

            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.content:
                        if a.correct:
                            score += 1
                            correct_answer = a.content
                    else:
                        if a.correct:
                            correct_answer = a.content

                marks.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                marks.append({str(q): 'not answered'})
     
        Marks_Of_User.objects.create(quiz=quiz, user=user, score=score)
        
        return JsonResponse({'passed': True, 'score': score, 'marks': marks})
    

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
        user.save()
        return redirect('/image_upload')  
    return render(request, "signup.html")

def Login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method=="POST":
        Login.username = request.POST['username']
        password = request.POST['password']
    
        user = authenticate(username=Login.username, password=password)
        
        if user is not None:
            login(request, user)
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