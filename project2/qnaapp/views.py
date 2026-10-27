from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .models import Question, Topic
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
def view_topics (request):
    context = {
        "user_id": request.session.get("user_id"),
        "username": request.session.get("username")
    }
    return render(request, "topics.html", context)

def view_questions (request, topic_id: int):
    user_id = request.session.get('user_id')
    data = Question.objects.filter(topic_id=topic_id, user_id=user_id).values()
    topic = Topic.objects.filter(pk=topic_id, user_id=user_id).first()

    if data is None or topic is None:
        return HttpResponse("There Are No Questions Available", status=404)
    questions = {
        "user_id": request.session.get("user_id"),
        "topic": topic.topic,
        "questions": data
    }
    return render(request, 'questions.html', questions)

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
            user_id = request.session.get("user_id")
            data = json.loads(request.body)
            topic = data.get("topic")
            count = data.get("count")

            generated_question = gemini.generate_question(topic, count)

            if generated_question is None:
                return JsonResponse({
                    "status": False,
                    "detail": "Something Went Wrong. Please Try Again Later"
                }, status=404)

            t = Topic.objects.create(
                topic=topic,
                count=count,
                user_id=user_id
            )

            for q in generated_question.questions:
                Question.objects.create(
                    topic_id=t.pk,
                    question=q.question,
                    correct_answer=q.correct_answer,
                    user_id=user_id
                )

            return JsonResponse({
                "status": True,
                "topic_id": t.pk,
                "topic": topic,
                "count": count
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

def get_recents (request):
    try:
        user_id = request.session.get("user_id")
        topics = Topic.objects.filter(user_id=user_id).order_by('-pk')[:5]

        data = [{
            "topic_id": q.pk,
            "topic": q.topic,
            "count": q.count
        } for q in topics]

        return JsonResponse(data, safe=False)
    except Exception:
        return JsonResponse({
            "status": False,
            "message": "Could not get Topics"
        },status=404)

def delete_topic (request, topic_id):
    if request.method == "DELETE":
        try:
            topic = Topic.objects.filter(pk=topic_id).first()

            topic.delete()
            return HttpResponse("topic Deleted", status=204)
        except Exception:
            return JsonResponse({
                "status": False,
                "message": "Something went wrong when Deleting"
            })

def get_topics (request):
    try:
        user_id = request.session.get("user_id")
        topics = Topic.objects.filter(user_id=user_id).order_by('-pk')
    
        data = [{
            "topic_id": q.pk,
            "topic": q.topic,
            "count": q.count
        } for q in topics]
    
        return JsonResponse(data, safe=False)
    except Exception:
        return JsonResponse({
            "status": False,
            "message": "Could not get Topics"
        },status=404)