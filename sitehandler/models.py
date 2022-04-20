from pyexpat import model
from django.db import models

# Create your models here.
class Doctors(models.Model):
	name = models.CharField(max_length=50)
	email = models.EmailField(unique=True)
	password = models.CharField(max_length=200)
	gender = models.CharField(max_length=10)
	phonenumber = models.CharField(max_length=11)
	address = models.CharField(max_length=100)
	birthdate = models.DateField()
	bloodgroup = models.CharField(max_length=5)
	specialization = models.CharField(max_length=50)
	is_verified=models.BooleanField(default=True)


	def __str__(self):
		return self.name

class Patients(models.Model):
	name = models.CharField(max_length=50)
	email = models.EmailField(unique=True)
	password = models.CharField(max_length=200)
	gender = models.CharField(max_length=10)
	phonenumber = models.CharField(max_length=11)
	address = models.CharField(max_length=100)
	birthdate = models.DateField()
	bloodgroup = models.CharField(max_length=5)
	auth_token=models.CharField(max_length=200)
	is_verified=models.BooleanField(default=False)


	def __str__(self):
		return self.name


class Appointment(models.Model):
	doctorname = models.CharField(max_length=50)
	doctoremail = models.EmailField(max_length=50)
	patientname = models.CharField(max_length=50)
	patientemail = models.EmailField(max_length=50)
	appointmentdate = models.DateField(max_length=10)
	appointmenttime = models.TimeField(max_length=10)
	symptoms = models.CharField(max_length=100)
	status = models.BooleanField()
	prescription = models.CharField(max_length=200)
	
	def __str__(self):
		return self.patientname+" you have appointment with "+self.doctorname