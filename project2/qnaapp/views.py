from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .models import Question
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from . import gemini
import json

@ensure_csrf_cookie
def home (request):
    context = {
        "user_id": request.session.get("user_id"),
        "username": request.session.get("username")
    }
    return render(request, "index.html", context)

@ensure_csrf_cookie
def user_create (request):
    return render(request, "usercreate.html", {})

@ensure_csrf_cookie
def user_login (request):
    return render(request, "login.html", {})

@ensure_csrf_cookie
def view_all_questions (request):
    context = {
        "user_id": request.session.get("user_id"),
        "username": request.session.get("username")
    }
    return render(request, "questions.html", context)

def user_logout (request):
    request.session.flush()
    return JsonResponse({
        "status": True
    })

def create_user (request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            user = User.objects.create_user(
                username=data.get("username"),
                email=data.get("email"),
                password=data.get("password"),
                first_name=data.get("first_name")
            )

            user.save()
            return JsonResponse({
                "status": True,
                "message": "User Created"
            }, status=201)
        except Exception:
            return JsonResponse({
                "status": False,
                "message": "Could not Create User"
            }, status=500)


def login_user (request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            user = authenticate(username=data.get("username"), password=data.get("password"))

            if user is not None:
                request.session['user_id'] = user.pk
                request.session['username'] = user.first_name
                return JsonResponse({
                    "status": True,
                    "message": "User logged in!"
                })
            return JsonResponse({
                "status": False,
                "message": "Invalid Credentials"
            })

        except Exception:
            return JsonResponse({
                "status": False,
                "message": "Could not Log User"
            }, status=500)

def create_question (request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            topic = data.get("topic")

            generated_question = gemini.generate_question(topic)

            if generated_question is None:
                return JsonResponse({
                    "status": False,
                    "detail": "Something Went Wrong. Please Try Again Later"
                }, status=404)

            Question.objects.create(
                topic=topic,
                question=generated_question.question,
                correct_answer=generated_question.correct_answer,
                user_id=request.session.get("user_id")
            )

            return JsonResponse({
                "status": True,
                "topic": topic,
                "question": generated_question.question,
                "correct_answer": generated_question.correct_answer
            }, status=201)
        except json.JSONDecodeError:
            return JsonResponse({
                "status": False,
                "message": "Invalid JSON"
            })
    return JsonResponse({
        "status": False,
        "message": "Method Not Allowed"
    }, status=500)

def get_question (request):
    try:
        user_id = request.session.get("user_id")
        questions = Question.objects.filter(user_id=user_id).order_by('-pk')[:5]

        data = []
        
        for q in questions:
            data.append({
                "question_id": q.pk,
                "topic": q.topic,
                "question": q.question,
                "answer": q.correct_answer
            })

        return JsonResponse(data, safe=False)
    except Exception:
        return JsonResponse({
            "status": False,
            "message": "Could not get Questions"
        })

def delete_question (request, question_id):
    if request.method == "DELETE":
        try:
            question = Question.objects.filter(pk=question_id).first()

            question.delete()
            return HttpResponse("Question Deleted", status=204)
        except Exception:
            return JsonResponse({
                "status": False,
                "message": "Something went wrong when Deleting"
            })

def get_all_questions (request):
    try:
        user_id = request.session.get("user_id")
        question = Question.objects.filter(user_id=user_id).order_by('-pk')

        data = []

        for q in question:
            data.append({
                "question_id": q.pk,
                "topic": q.topic,
                "question": q.question,
                "answer": q.correct_answer
            })

        return JsonResponse(data, safe=False)
    except Exception:
        return JsonResponse({
            "status": False,
            "message": "Could not get Questions"
        })