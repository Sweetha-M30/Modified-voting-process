import pandas as pd
import json
import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from deepface import DeepFace
import cv2

def index(request):
    return render(request, 'voting_web/index.html')

def panel(request):
    return render(request, 'voting_web/panel_po.html')

def register_user(request):
    return render(request, 'voting_web/register_user.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        path = os.path.join(settings.BASE_DIR, 'voting_web/data/pollingOfficerLogin.xlsx')
        df = pd.read_excel(path)

        if any((df['username'] == username) & (df['password'] == password)):
            return redirect('panel')
        else:
            return JsonResponse({'success': False, 'message': 'Invalid credentials'})

    return render(request, 'voting_web/login_po.html')

def add_user(request):
    if request.method == 'POST':
        username = request.POST['userid']
        password = request.POST['Password']

        path = os.path.join(settings.BASE_DIR, 'voting_web/data/pollingOfficerLogin.xlsx')
        df = pd.read_excel(path)

        df = pd.concat([df, pd.DataFrame({'username':[username],'password':[password]})])
        df.to_excel(path, index=False)

        return JsonResponse({'success': True})

def vote_panel(request):
    return render(request, 'voting_web/vote_panel.html')

def increase_vote(request):
    data = json.loads(request.body)
    party = data['color']

    path = os.path.join(settings.BASE_DIR, 'voting_web/data/Votes.xlsx')
    df = pd.read_excel(path)
    df.loc[df['Party_Name'] == party, 'Votes_Count'] += 1
    df.to_excel(path, index=False)

    return JsonResponse({'success': True})

def show_results(request):
    path = os.path.join(settings.BASE_DIR, 'voting_web/data/Votes.xlsx')
    df = pd.read_excel(path)

    winner = df.loc[df['Votes_Count'].idxmax()]['Party_Name']
    return JsonResponse({'winner': winner})

def reset_votes(request):
    data = json.loads(request.body)
    if data['password'] == "Admin123":
        path = os.path.join(settings.BASE_DIR, 'voting_web/data/Votes.xlsx')
        df = pd.read_excel(path)
        df['Votes_Count'] = 0
        df.to_excel(path, index=False)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
