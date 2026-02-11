from django.shortcuts import render
from django.contrib import messages
from .forms import ContactForm

def about(request):
    return render(request, "pages/about.html")

def contact(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks! Your message has been sent.")
            form = ContactForm()
    return render(request, "pages/contact.html", {"form": form})
