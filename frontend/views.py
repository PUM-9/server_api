from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormView
from jobs.forms import RegistrationJobForm
from jobs.models import File, Registration
from django.views.decorators.csrf import csrf_protect


def index(request):
    registration_jobs = Registration.objects.all()

    return render(request, 'frontend/index.html', {'registration_jobs': registration_jobs})


@csrf_protect
def registration_job_form(request):
    form = RegistrationJobForm()
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        if form.is_valid():
            name = form.cleaned_data['name']
            log_level = form.cleaned_data['log_level']
            max_correspondence = form.cleaned_data['max_correspondence']
            max_iterations = form.cleaned_data['max_iterations']
            transformation_epsilon = form.cleaned_data['transformation_epsilon']
            leaf_size = form.cleaned_data['leaf_size']
            job_id = Registration.create(name, log_level, max_correspondence, max_iterations, transformation_epsilon,
                                         leaf_size)
            for f in files:
                File.create(f, job_id)
            return render(request, 'frontend/index.html')
        else:
            print(form.errors)
            print("form invalid")
            return render(request, 'frontend/index.html')
    else:
        return render(request, 'frontend/registration_form.html', {'form': form})
