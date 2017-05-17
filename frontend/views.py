from django.shortcuts import render, redirect
from jobs.forms import RegistrationJobForm, MeshJobForm
from jobs.models import File, Registration, Mesh
from django.views.decorators.csrf import csrf_protect


def index(request):
    registration_jobs = Registration.objects.all()
    return render(request, 'frontend/index.html', {'registration_jobs': registration_jobs})


@csrf_protect
def registration_job_form(request):
    messages = list()
    if request.method == 'POST':
        form = RegistrationJobForm(request.POST)
        form.fields['files'].required = False
        files = request.FILES.getlist('files')
        if form.is_valid() and files:
            name = form.cleaned_data['name']
            log_level = form.cleaned_data['log_level']
            max_correspondence = form.cleaned_data['max_correspondence']
            max_iterations = form.cleaned_data['max_iterations']
            transformation_epsilon = form.cleaned_data['transformation_epsilon']
            leaf_size = form.cleaned_data['leaf_size']
            job = Registration.create(name, log_level, max_correspondence, max_iterations, transformation_epsilon,
                                      leaf_size)
            for f in files:
                File.create(f, job)
            return redirect('index')
        else:
            messages.append("Form could not be validated")
    form = RegistrationJobForm()
    return render(request, 'frontend/registration_form.html', {'form': form, 'error_messages': messages})


def mesh_job_form(request):
    messages = list()
    if request.method == 'POST':
        form = MeshJobForm(request.POST)
        files = request.FILES.getlist('file')
        if form.is_valid() and files:
            name = form.cleaned_data['name']
            log_level = form.cleaned_data['log_level']
            job = Mesh.create(name, log_level)
            File.create(files[0], job)
            return render(request, 'frontend/index.html')
        else:
            messages.append("Form could not be validated")
    form = MeshJobForm()
    return render(request, 'frontend/mesh_form.html', {'form': form, 'error_messages': messages})


def registration_job_show(request):
    job_id = request.GET.get('id', '')
    reg_object = Registration.objects.filter(id=job_id)
    files = File.objects.filter(job=job_id)
    return render(request, 'frontend/registration_job.html', locals())


def registration_job_delete(request):
    job_id = request.GET.get('id', '')
    Registration.objects.filter(id=job_id).delete()
    File.objects.filter(id=job_id).delete()
    return redirect(index)