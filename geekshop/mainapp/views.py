from django.shortcuts import render
import json



def main(request):
    return render(request, 'mainapp/index.html', {'title': 'главная'})


def products(request):
    with open('links.json', 'r') as file:
        links_menu = json.load(file)
    context = {'title': 'продукты', 'links_menu': links_menu}
    return render(request, 'mainapp/products.html', context)


def contact(request):
    return render(request, 'mainapp/contact.html', {'title': 'контакты'})