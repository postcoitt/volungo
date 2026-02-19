from django.shortcuts import render
from django.http import JsonResponse

def my_button_action(request):
    result = {"message": 'Кнопка натиснулась і працює! Слава Богу!'}
    return JsonResponse(result)


def filters_button_action(request):
    filters = [
        {"filter1": "filter", "text": "Button"},
        {"filter2": "filter", "text": "Button"},
        {"filter3": "filter", "text": "Button"}
               ]
    return JsonResponse({"buttfiltersons": filters})
