from django.shortcuts import render,redirect
from django.contrib.auth.models import User,Group
from .models import *
import uuid
from django.contrib.auth import authenticate,logout,login
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail



# Create your views here.

def homepage(request):
	return render(request,'index.html')

def aboutpage(request):
	return render(request,'about.html')

def Login_admin(request):
	error = ""
	if request.method == 'POST':
		u = request.POST['username']
		p = request.POST['password']
		user = authenticate(username=u,password=p)
		try:
			if user.is_staff:
				login(request,user)
				error = "no"
			else:
				error = "yes"
		except:
			error = "yes"
	d = {'error' : error}
	return render(request,'adminlogin.html',d)

def loginpage(request):
	error = ""
	page = ""
	if request.method == 'POST':
		u = request.POST['email']
		p = request.POST['password']
		user = authenticate(request,username=u,password=p)
		if user is None:
			error="yes"
		try:
			if user is not None:
				login(request,user)
				error = "no"
				g = request.user.groups.all()[0].name
				if g == 'Doctor':
					page = "doctors"
					d = {'error': error,'page':page}
					return render(request,'doctorhome.html',d)
				elif g == 'Patient':
					page = "patients"
					d = {'error': error,'page':page}
					return render(request,'patienthome.html',d)

			else:
				error = "yes"
		except Exception as e:
			error = "yes"
	d = {'error': error}
	if error == "yes":
		d = {'error': error}
	elif error == "notv":
		d = {'error': error}
	return render(request,'login.html',d)

def createaccountpage(request):
	error = ""
	user="none"
	auth_token = str(uuid.uuid4())
	is_verified = False
	if request.method == 'POST':
		name = request.POST['name']
		email = request.POST['email']
		password = request.POST['password']
		repeatpassword = request.POST['repeatpassword']
		gender = request.POST['gender']
		phonenumber = request.POST['phonenumber']
		address = request.POST['address']
		birthdate = request.POST['dateofbirth']
		bloodgroup = request.POST['bloodgroup']

		try:
			if password == repeatpassword:
				send_mail_after_registration(email , auth_token)
				Patients.objects.create(name=name,email=email,password=password,gender=gender,phonenumber=phonenumber,address=address,birthdate=birthdate,bloodgroup=bloodgroup, auth_token=auth_token,is_verified =is_verified)
				user = User.objects.create_user(first_name=name,email=email,password=password,username=email)
				pat_group = Group.objects.get(name='Patient')
				pat_group.user_set.add(user)
				user.save()
				error = "no"
			else:
				error = "yes"
		except Exception as e:
			error = "yes"
	d = {'error' : error}
	return render(request,'createaccount.html',d)

def send_mail_after_registration(email , token):
    subject = 'Your account need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )


def verify(request , auth_token):
    try:
        profile_obj = Patients.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
            return redirect('homepage')
        else:
            return redirect('/')
    except Exception as e:
        return redirect('/')
 

def adminaddDoctor(request):
	error = ""
	user="none"
	if not request.user.is_staff:
		return redirect('login_admin')

	if request.method == 'POST':
		name = request.POST['name']
		email = request.POST['email']
		password = request.POST['password']
		repeatpassword =  request.POST['repeatpasssword']
		gender = request.POST['gender']
		phonenumber = request.POST['phonenumber']
		address = request.POST['address']
		birthdate = request.POST['dateofbirth']
		bloodgroup = request.POST['bloodgroup']
		specialization = request.POST['specialization']
		
		try:
			if password == repeatpassword:
				Doctors.objects.create(name=name,email=email,password=password,gender=gender,phonenumber=phonenumber,address=address,birthdate=birthdate,bloodgroup=bloodgroup,specialization=specialization)
				user = User.objects.create_user(first_name=name,email=email,password=password,username=email)
				doc_group = Group.objects.get(name='Doctor')
				doc_group.user_set.add(user)
				user.save()
				error = "no"
			else:
				error = "yes"
		except Exception as e:
			error = "yes"
	d = {'error' : error}
	return render(request,'adminadddoctor.html',d)

def adminviewDoctor(request):
	if not request.user.is_staff:
		return redirect('login_admin')
	doc = Doctors.objects.all()
	d = { 'doc' : doc }
	return render(request,'adminviewDoctors.html',d)

def adminviewPatient(request):
	if not request.user.is_staff:
		return redirect('login_admin')
	doc = Patients.objects.all()
	d = { 'doc' : doc }
	return render(request,'adminviewPatient.html',d)

def admin_delete_doctor(request,pid,email):
	if not request.user.is_staff:
		return redirect('login_admin')
	doctor = Doctors.objects.get(id=pid)
	doctor.delete()
	users = User.objects.filter(username=email)
	users.delete()
	return redirect('adminviewDoctor')
def admin_delete_patient(request,pid,email):
	if not request.user.is_staff:
		return redirect('login_admin')
	patient = Patients.objects.get(id=pid)
	patient.delete()
	users = User.objects.filter(username=email)
	users.delete()
	return redirect('adminviewPatient')

def patient_delete_appointment(request,pid):
	if not request.user.is_active:
		return redirect('loginpage')
	appointment = Appointment.objects.get(id=pid)
	appointment.delete()
	return redirect('viewappointments')

def adminviewAppointment(request):
	if not request.user.is_staff:
		return redirect('login_admin')
	upcomming_appointments = Appointment.objects.filter(appointmentdate__gte=timezone.now(),status=True).order_by('appointmentdate')
	d = { "upcomming_appointments" : upcomming_appointments}
	return render(request,'adminviewappointments.html',d)
def adminviewprevious(request):
	if not request.user.is_staff:
		return redirect('login_admin')
	previous_appointments = Appointment.objects.filter(appointmentdate__lt=timezone.now()).order_by('-appointmentdate') | Appointment.objects.filter(status=False).order_by('-appointmentdate')
	d = {"previous_appointments" : previous_appointments }
	return render(request,'adminviewprevious.html',d)

def Logout(request):
	if not request.user.is_active:
		return redirect('loginpage')
	logout(request)
	return redirect('loginpage')

def Logout_admin(request):
	if not request.user.is_staff:
		return redirect('login_admin')
	logout(request)
	return redirect('login_admin')

def AdminHome(request):
	#after login user comes to this page.
	if not request.user.is_staff:
		return redirect('login_admin')
	return render(request,'adminhome.html')

def Home(request):
	if not request.user.is_active:
		return redirect('loginpage')

	g = request.user.groups.all()[0].name
	if g == 'Doctor':
		return render(request,'doctorhome.html')
	elif g == 'Patient':
		return render(request,'patienthome.html')

def profile(request):
	if not request.user.is_active:
		return redirect('loginpage')
	g = request.user.groups.all()[0].name
	if g == 'Patient':
		patient_detials = Patients.objects.all().filter(email=request.user)
		d = { 'patient_detials' : patient_detials }
		return render(request,'pateintprofile.html',d)
	elif g == 'Doctor':
		doctor_detials = Doctors.objects.all().filter(email=request.user)
		d = { 'doctor_detials' : doctor_detials }
		return render(request,'doctorprofile.html',d)

def MakeAppointments(request):
	error = ""
	if not request.user.is_active:
		return redirect('loginpage')
	alldoctors = Doctors.objects.all()
	d = { 'alldoctors' : alldoctors }
	g = request.user.groups.all()[0].name
	if g == 'Patient':
		if request.method == 'POST':
			doctoremail = request.POST['doctoremail']
			doctorname = request.POST['doctorname']
			patientname = request.POST['patientname']
			patientemail = request.POST['patientemail']
			appointmentdate = request.POST['appointmentdate']
			appointmenttime = request.POST['appointmenttime']
			symptoms = request.POST['symptoms']
			try:
				Appointment.objects.create(doctorname=doctorname,doctoremail=doctoremail,patientname=patientname,patientemail=patientemail,appointmentdate=appointmentdate,appointmenttime=appointmenttime,symptoms=symptoms,status=True,prescription="")
				error = "no"
			except:
				error = "yes"
			e = {"error":error}
			return render(request,'pateintmakeappointments.html',e)
		elif request.method == 'GET':
			return render(request,'pateintmakeappointments.html',d)

def viewappointments(request):
	if not request.user.is_active:
		return redirect('loginpage')
	g = request.user.groups.all()[0].name
	if g == 'Patient':
		upcomming_appointments = Appointment.objects.filter(patientemail=request.user,appointmentdate__gte=timezone.now(),status=True).order_by('appointmentdate')
		d = { "upcomming_appointments" : upcomming_appointments}
		return render(request,'patientviewappointments.html',d)
	
	elif g == 'Doctor':
		if request.method == 'POST':
			prescriptiondata = request.POST['prescription']
			idvalue = request.POST['idofappointment']
			Appointment.objects.filter(id=idvalue).update(prescription=prescriptiondata,status=False)
		upcomming_appointments = Appointment.objects.filter(doctoremail=request.user,appointmentdate__gte=timezone.now(),status=True).order_by('appointmentdate')
		d = { "upcomming_appointments" : upcomming_appointments}
		return render(request,'doctorviewappointment.html',d)

def viewprevious(request):
	if not request.user.is_active:
		return redirect('loginpage')
	g = request.user.groups.all()[0].name
	if g == 'Patient':
		previous_appointments = Appointment.objects.filter(patientemail=request.user,appointmentdate__lt=timezone.now()).order_by('-appointmentdate') | Appointment.objects.filter(patientemail=request.user,status=False).order_by('-appointmentdate')
		d = {"previous_appointments" : previous_appointments }
		return render(request,'patientviewprevious.html',d)
	elif g == 'Doctor':
		previous_appointments = Appointment.objects.filter(doctoremail=request.user,appointmentdate__lt=timezone.now()).order_by('-appointmentdate') | Appointment.objects.filter(doctoremail=request.user,status=False).order_by('-appointmentdate')
		d = { "previous_appointments" : previous_appointments }
		return render(request,'doctorviewprevious.html',d)