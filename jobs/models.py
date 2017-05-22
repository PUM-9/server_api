from django.db import models
from enum import Enum
from django.utils import timezone
from users.models import User
from web_application.settings import FILE_UPLOAD_DIR
import random
import string
import os
import subprocess


def random_word(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


class LogLevel(Enum):
    TRACE = 0
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4


class Job(models.Model):
    created = models.DateTimeField('created')
    started = models.DateTimeField('started', null=True)
    finished = models.DateTimeField('finished', null=True)
    log_level = models.SmallIntegerField('log_level', default=LogLevel.WARNING)
    name = models.CharField('name', max_length=200)


class Registration(Job):
    max_correspondence = models.FloatField('max_correspondence')
    max_iterations = models.IntegerField('max_iterations')
    transformation_epsilon = models.FloatField('transformation_epsilon')

    @classmethod
    def create(cls, name, log_lvl, max_corr, max_it, trans_eps):
        created = timezone.now()
        try:
            log_lvl = int(log_lvl)
        except ValueError:
            log_lvl = LogLevel.INFO
        registration = cls(name=name, created=created, log_level=log_lvl, max_correspondence=max_corr,
                           max_iterations=max_it, transformation_epsilon=trans_eps)
        registration.save()
        return registration

    def execute(self):
        self.started = timezone.now()
        self.save()
        command = list(['~/TDDD96/3DCopy/3DCopy'])
        command.append('-r')
        command.append('-d')
        command.append(str(self.max_correspondence))
        command.append('-i')
        command.append(str(self.max_iterations))
        files = File.objects.filter(job=self.id)
        for file in files:
            command.append(file.path)
        output_name = random_word(10)
        while len(File.objects.all().filter(name=output_name+".pcd")) > 0:
            output_name = random_word(10)
        output_path = os.path.join(FILE_UPLOAD_DIR, output_name)
        command.append(output_path)
        output_path += ".pcd"
        print(' '.join(command))
        timeout = 5 * 60 * 60  # Timeout after 5 hours.
        try:
            job_process = subprocess.run(' '.join(command), timeout=timeout, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                         shell=True)
        except Exception as e:
            print("FAIL")
            print(e)
        print("registration done")
        print("STANDARD OUTPUT:\n")
        print(job_process.stdout.decode())
        print("STANDARD ERROR:\n")
        print(job_process.stderr.decode())
        Registration.objects.filter(id=self.id).update(finished=timezone.now())
        File.save_output(output_name+".pcd", output_path, self, "pcd")
        return

    def class_name(self):
        return self.__class__.__name__


class Mesh(Job):

    @classmethod
    def create(cls, name, log_lvl):
        created = timezone.now()
        try:
            log_lvl = int(log_lvl)
        except ValueError:
            log_lvl = LogLevel.INFO
        mesh = cls(name=name, created=created, log_level=log_lvl)
        mesh.save()
        return mesh

    def execute(self):
        self.started = timezone.now()
        self.save()
        command = list(['~/TDDD96/3DCopy/3DCopy'])
        command.append('-m')
        file = File.objects.filter(job=self.id)
        command.append(file.path)
        output_name = random_word(10)
        while len(File.objects.all().filter(name=output_name+".pcd")) > 0:
            output_name = random_word(10)
        output_path = os.path.join(FILE_UPLOAD_DIR, output_name)
        command.append(output_path)
        output_path += ".stl"
        print(' '.join(command))
        timeout = 5 * 60 * 60  # Timeout after 5 hours.
        try:
            job_process = subprocess.run(' '.join(command), timeout=timeout, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                         shell=True)
        except Exception as e:
            print("FAIL")
            print(e)
        print("meshing done")
        print("STANDARD OUTPUT:\n")
        print(job_process.stdout.decode())
        print("STANDARD ERROR:\n")
        print(job_process.stderr.decode())
        Mesh.objects.filter(id=self.id).update(finished=timezone.now())
        File.save_output(output_name+".stl", output_path, self, "stl")
        return

    def class_name(self):
        return self.__class__.__name__


class File(models.Model):
    name = models.CharField('name', max_length=20)
    created = models.DateTimeField('created')
    path = models.CharField('path', max_length=300)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    file_type = models.CharField('type', max_length=30)
    is_input = models.BooleanField('is_input')

    @classmethod
    def upload_pcd(cls, uploaded_file, job):
        name = random_word(15) + ".pcd"
        while len(File.objects.all().filter(name=name)) > 0:
            name = random_word(15) + ".pcd"
        created = timezone.now()
        if len(uploaded_file.name.split('.')) > 1 and uploaded_file.name.split('.')[-1] == "pcd":
            path = os.path.join(FILE_UPLOAD_DIR, name)
            file = open(path, "wb")
            for chunk in uploaded_file.chunks():
                file.write(chunk)
            file.close()
        else:
            return False
        db_file = cls(name=name, created=created, path=path, job=job, file_type='pcd', is_input=True)
        db_file.save()
        return db_file

    @classmethod
    def save_output(cls, name, path, job, file_type):
        created = timezone.now()
        db_file = cls(name=name, created=created, path=path, job=job, file_type=file_type, is_input=False)
        db_file.save()
        return db_file
