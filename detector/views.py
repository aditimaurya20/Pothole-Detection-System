from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .utils import detect_image_pothole, detect_video_pothole, detect_live
from django.shortcuts import redirect
import os
import time
# ---------------- HOME ----------------
def home(request):
    return render(request, 'index.html')


# ---------------- PAGES ----------------
def image_page(request):
    return render(request, 'image.html')

def video_page(request):
    return render(request, 'video.html')

def live_page(request):
    return render(request, 'live.html')


# ---------------- IMAGE ----------------
def detect_image(request):

    if request.method == 'POST' and request.FILES.get('image'):

        image = request.FILES['image']
        fs = FileSystemStorage()

        filename = fs.save(image.name, image)
        path = fs.path(filename)

        output_name = "out_" + image.name
        output_path = fs.path(output_name)

        detected, severity = detect_image_pothole(path, output_path)

        return render(request, 'image.html', {
            "result": "Pothole Detected" if detected else "No Pothole",
            "severity": severity,
            "output_image": fs.url(output_name)
        })

    return render(request, 'image.html')

def detect_video(request):

    if request.method == 'POST' and request.FILES.get('video'):

        video = request.FILES['video']
        fs = FileSystemStorage()

        filename = fs.save(video.name, video)
        input_path = fs.path(filename)

        output_name = "processed_" + video.name
        output_path = fs.path(output_name)

        detected = detect_video_pothole(input_path, output_path)

        for _ in range(10): 
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                break
            time.sleep(0.5)

        return render(request, 'video.html', {
            "result": "Pothole Detected" if detected else "No Pothole",
            "output_video": fs.url(output_name)
        })

    return render(request, 'video.html')

# ---------------- LIVE ----------------
def run_live(request):
    detect_live()
    return render(request, 'live.html')

from .utils import send_pothole_email

def send_email_view(request):

    if request.method == "POST":

        location = request.POST.get("location")

        pothole_count = request.POST.get("count", 0)

        send_pothole_email(location, pothole_count)

    return redirect("/video/")

def send_email_view(request):

    if request.method == "POST":

        location = request.POST.get("location")
        pothole_count = 1

        send_pothole_email(location, pothole_count)

    return redirect("/image/")