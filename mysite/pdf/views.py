from django.shortcuts import render
from .models import Profile 
import pdfkit
from django.http import HttpResponse
from django.template import loader
import io


# Create your views here.
def index(request):
    if request.method == 'POST':
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        summary = request.POST.get('summary','')
        degree = request.POST.get('degree','')
        school = request.POST.get('school','')
        university = request.POST.get('university','')
        previous_work = request.POST.get('previous_work','')
        skills = request.POST.get('skills','')

        profile = Profile(name=name, email=email, phone=phone, summary=summary, degree=degree, school=school, university=university, previous_work=previous_work, skills=skills)
        profile.save()
        
    return render(request, 'pdf/index.html')

def resume(request, id):
    user_profile = Profile.objects.get(pk=id)
    template = loader.get_template('pdf/resume.html')
    html = template.render({'user_profile':user_profile})
    options = {
        'page-size': 'Letter',
        'no-outline': None,
        'disable-javascript': True,  # Disable JavaScript if not needed
        'no-images': True,  # Disable image loading if not required
        'encoding': 'UTF-8'
    }
    #SET TO UR PATH
    config = pdfkit.configuration(wkhtmltopdf=r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    pdf = pdfkit.from_string(html, False, options=options, configuration=config) #from_string :- tankes an html strings and it convert that html string to a pdf document
    # try:
    #     pdf = pdfkit.from_string(html, False, options=options, configuration=config)
    # except OSError as e:
    #     print("Error with wkhtmltopdf:", e)
    #     # Handle error appropriately
    #     return HttpResponse("Error generating PDF.")
    response = HttpResponse(pdf,content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'

    return response

def list(request):
    profiles = Profile.objects.all()
    return render(request, 'pdf/list.html',{'profiles':profiles})