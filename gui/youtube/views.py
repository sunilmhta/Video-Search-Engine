# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,render_to_response
from django import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from youtube.forms import initialSearch,userLogin,userRegistration
import sys
sys.path.insert(0, '/home/sunil/Documents/assignment/gui/youtube/databaseCreate')
import didyoumean
import mongoSearch
import neoSearch
import json
import handler
import sql_checklogin
# import didyoumean
#session_running=False


def index(request):

    if '0' in request.session:
    	output=handler.history(request.session['0'])
    else:
    	output=handler.nonHistory()
    #print output
    finalOutput={}
    for video_id in output:
    	#print video_id[0]
    	individual_output=mongoSearch.searchIndividual(video_id[0])
    	#print individual_output
    	for i in individual_output:
    		finalOutput[video_id[0]]=i
    username='login'
    if '0' in request.session:
    	username=request.session['0']
    context={"flag":username,"message":finalOutput}


    #print finalOutput

    return render(request,'youtube/index.html',context)
def logout(request):
	if '0' in request.session:
		del request.session['0']
		request.session.modified=True
	return render(request,'youtube/logout.html',{})
	# return HttpResponseRedirect("youtube/index.html/")
def submit(request):
	context={}
	username='login'
	if request.method == "GET":
		data=request.GET.get('search_key_text','')
		correctedSuggestion=didyoumean.didyoumeanResult(data)
		flag=0
		if correctedSuggestion != data:
			flag=1
			data=correctedSuggestion
		if '0' in request.session:
			username=request.session['0']
		if data:
			context={"message":data}
			neo_data=data
			mongoSearch.search(context,username)
			searchedOutput=mongoSearch.sorted_output
			if flag==1:
				context={"username":username,"flag":correctedSuggestion,"message":searchedOutput}
			else:
				context={"username":username,"message":searchedOutput}
			length=len(searchedOutput)
			return render(request,'youtube/submit.html',context)
	return render(request,'youtube/submit.html',{})
def login(request):
	# pass
	#print "i am vishal"
	return render(request,'youtube/login.html',{})


def watch(request,video_id):
	neoSearchOutput=neoSearch.search_on_click(video_id)
	relatedVideo={}
	username='login'
	for obj in neoSearchOutput:
		for data in obj:
			singleOutput=mongoSearch.searchIndividual(obj[data]['id'])
			for ii in singleOutput:
				relatedVideo[obj[data]['id']]=ii
	current_video_info=mongoSearch.searchIndividual(video_id)
	current_detail={}
	for obj in current_video_info:
		current_detail=obj
	if '0' in request.session:
		username=request.session['0']
		handler.add_history(request.session['0'],video_id)
		handler.non_signed_history(video_id)
	else:
		handler.non_signed_history(video_id)
	output={"message":relatedVideo,"current_detail":current_detail,"username":username}
	print mongoSearch.increase_view_count(video_id)
	return render(request,'youtube/watch.html',output)

def neo(request,neo_data):
	print 'neodata'
	data=request.GET.get('')
	#print neo_data
	return render(request,'youtube/neo.html',{'message':neo_data})
def checklogin(request):
	# request.session[0]=''
	form=userLogin(request.POST)
	if request.method=='POST':
		#form.save()
		if form.is_valid():
			username=form.cleaned_data['username']
			password=form.cleaned_data['password']
			#print username,password
			# userExistingStatus=sql(username,password)
			status=sql_checklogin.checkLogin(username,password)
			# request.session['user_id']=username
			# print 'status',type(status)
			# print 'session',request.session['0']
			if status!=0:
				request.session[0]=username
				session_running=True
			#print request.session['0']
	return render(request,'youtube/status.html',{})

def thanks(request):
	form=userRegistration(request.POST)
	if request.method=='POST':
		if form.is_valid():
			first_name=form.cleaned_data['first_name']
			last_name=form.cleaned_data['last_name']
			#password=form.cleaned_data['password']
			#email=form.cleaned_data['email']
			#age=form.cleaned_data['age']
			#sex=form.cleaned_data['sex']
			status=handler.user_registration([first_name,last_name,'sex','age','vishal_email','password'])
			if status:
				message='thanks for registration'
				return render(request,'youtube/thanks.html',{"message":message})
			#print first_name,last_name
			message='Already registered.Please login to continue.'
			return render(request,'youtube/thanks.html',{"message":message})



def history(request):
	username=''
	if '0' in request.session:
		output=handler.history(request.session['0'])
		finalOutput={}
		for video_id in output:
			individual_output=mongoSearch.searchIndividual(video_id[0])
			for i in individual_output:
				finalOutput[video_id[0]]=i
		username=request.session['0']
	context={"user_id":username,"message":finalOutput}
	return render(request,'youtube/history.html',context)
	#return render(request,'youtube/history',{})
    	# output=handler.history(request.session['0'])
	    # #print output
	    # finalOutput={}
	    # for video_id in output:
	    # 	#print video_id[0]
	    # 	individual_output=mongoSearch.searchIndividual(video_id[0])
	    # 	#print individual_output
	    # 	for i in individual_output:
	    # 		finalOutput[video_id[0]]=i
	    # username='login'
	    # if '0' in request.session:
	    # 	username=request.session['0']
	    # context={"flag":username,"message":finalOutput}

