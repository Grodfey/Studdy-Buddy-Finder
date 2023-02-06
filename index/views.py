from datetime import datetime as datetime
from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
import requests
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User

from .models import userMeeting, Course, UserInfo, Friend, Meeting, Member, UserBio
from .forms import ChangeProfileForm, ChangeBioForm
import json
from django.views.generic.edit import ProcessFormView, FormMixin

# Friend related views
# - add()
# - remove()
# - result_view()
# - user_search()
def removeFriend(request):
    friend_to_delete = request.POST['remove_friend']
    request.user.friend_set.get(addee_uid=friend_to_delete).delete()
    return HttpResponseRedirect(reverse('index:profile'))
def addedFriend(request):
    # Example data: Carter Quentin Freeman @ cqf4bq
    data = request.POST['user_data'].split('@')
    Friend.objects.create(adder=request.user, addee_uid=data[1], addee_nom=data[0])
    return render(request, 'index/addedFriend.html')
def usersearch(request):
    if (request.method == "POST"):
        searched = request.POST['searched']        
        friend_set = list(map(str.strip, list( request.user.friend_set.all().values_list('addee_uid', flat=True) )))
        invalid_set = [ request.user.username ] + friend_set
        users = User.objects.exclude(username__in=invalid_set)
        # friends_list = list(request.user.friend_set.objects.all().values_list('User', flat=True))
        # print([ User for User in request.user.friend_set ])
        return render(request, 'index/user-search.html', {
            "searched": searched,
            "users": users
            })
    return render(request, 'index/user-search.html')
class UserResultsListView(generic.ListView):
    model = Course
    template_name = 'index/userresults.html'
    def get_queryset(self): # will need to change this based on the profile data and the SIS API
        query = self.request.GET.get("q")
        return Course.objects.filter(Q(course_number__icontains=query) | Q(instructor__icontains=query))


# def class_search_dummy(request):
#     query = request.POST['department'].upper()
#     domain = "luthers-list.herokuapp.com"
#     api = f"http://{domain}/api/dept/{query}/"
#     response = requests.get(api).json()
#     if (request.method == "POST"):
#         return render(request, 'index/class-results-new.html', {
#             'searched': True,
#             'query': searched,
#             'classes' : response,
#             })
#     return render(request, 'index/class-results-new.html', {
#         'searched': False,
#     })

# Class based view for class search results
# Replaces get_results
"""
@login_required(login_url='{% url "index:index" %}') 
class ClassResultsListView(generic.ListView, FormMixin):
    context_object_name = 'response'
    template_name = 'index/class-search-new.html'
    # paginate_by = 10
    # def post(self, request, *args, **kwargs):
        # return FormView.as_view()(request)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(**kwargs)
        try:
            query = request.POST['searchDept'].upper()
            domain = "luthers-list.herokuapp.com"
            api = f"http://{domain}/api/dept/{query}/"
            results = requests.get(api).json()
            context = results
        except:
            context['searched'] = True
        return context
    def get_queryset(self, request):
        # print( 'JSON:', response )
        print( 'UserInfo:', UserInfo.objects.filter(user_id=user.id) )
        return response
        # results.exclude( ... )
        # return Course.objects.filter(Q(course_number__icontains=query) | Q(instructor__icontains=query))        
"""
# Class related views
# - search()
# - add()
# - remove()
# - ResultsView

def class_search(request):
    if (request.method == "POST"):
        url = "http://luthers-list.herokuapp.com/api/dept"
        searched = request.POST['searchDept'].upper()
        query_url = f"{url}/{searched}/"
        response = requests.get(query_url).json()
        return render(request, 'index/class-search.html', {
            'searched': True,
            'query': searched,
            'classes' : response,
            })
    return render(request, 'index/class-search.html', {
        'searched': False,
    })
# Function based view for class search results
# @login_required(login_url='{% url "index:index" %}')
def get_Results(request):
    api = "http://luthers-list.herokuapp.com/api/dept/REPLACE/"
    api = api.replace( "REPLACE", request.POST['searchDept'].upper() )
    response = requests.get(api).json()
    # print( 'Class data:', response, 'User:', request.user.userinfo_set )
    return render(request, 'index/class-results.html', {'response' : response})

def class_success(request):
    class_info = request.POST['thatClass'].split("-")
    keys = ['user', 'class_subject','class_number','class_section']
    info = [request.user] + class_info
    current_classes = list( request.user.userinfo_set.all().values_list('class_subject','class_number','class_section') )
    # Do not allow users to add the same class multiple times
    if tuple(class_info) in current_classes:
        return render(request, 'index/class-results.html', {'error_message': "Class already added"})
    UserInfo.objects.create(**dict(zip(keys, info)))
    return render(request, 'index/class_success.html')

def removeClass(request):
    request.user.userinfo_set.get(pk=request.POST['remove_class']).delete()
    return HttpResponseRedirect(reverse('index:profile'))

# Meeting related views
# - join()
# - add()
# - MeetingsView
# - MeetingAddView
# - IndeView
def joinMeeting(request):
    split = request.POST['join'].split("-")
    member = f'{split[0]} {split[1]} ({split[2]})'
    id = split[3]
    joined = False
    for m in Member.objects.all():
        if m.meeting == Meeting.objects.get(pk=id) and member == m.member_text:
            for m2 in userMeeting.objects.all():
                if m2.user == request.user and m2.meeting == m.meeting:
                    m2.delete() # thing to test: if you are the owner of the meeting and you leave it
            joined = True
            m.delete()
    if not joined:
        Member.objects.create(meeting=Meeting.objects.get(pk=id), member_text=member)
        userMeeting.objects.create(user=request.user, meeting=Meeting.objects.get(pk=id))
    return HttpResponseRedirect('/meetings')

def addMeeting(request): # bug: error when empty input
    try:
        print(request.POST['confirm'])
        split = request.POST['confirm'].split("-")

        title_filled = bool(request.POST['title'] != '')
        descr_filled = bool(request.POST['description'] != '')
        date_filled = bool(request.POST['date'])
        start_filled = bool(request.POST['start'] != '')
        end_filled = bool(request.POST['end'] != '')

        if  title_filled or descr_filled or date_filled or start_filled or end_filled:
            new_meeting = Meeting(
                owner_text = f'{split[0]} {split[1]} ({split[2]})',
                title_text = request.POST['title'],
                description_text = request.POST['description'],
                date = request.POST['date'],
                start_date = request.POST['start'],
                end_date = request.POST['end'],
                creation_date = datetime.strftime(timezone.now(), '%Y-%m-%d %H:%M'),
            )
            new_meeting.save()
            userMeeting.objects.create(user=request.user, meeting=new_meeting)
            return redirect('index:meetings')
        else:
            res = {'error_message': "Fill all required information before creating a meeting."}
            return render(request, 'index/addmeeting.html', res)
    except:
        res = {'error_message': "An error has occurred."}
        return render(request, 'index/addmeeting.html', res)

class MeetingsView(generic.ListView):
    template_name = 'index/meetings.html'
    context_object_name = 'latest_meeting_list'
    def get_queryset(self):
        return Meeting.objects.filter(creation_date__lte=timezone.now()).order_by('-creation_date')[:30]
class MeetingAddView(generic.ListView):
    template_name = 'index/addmeeting.html'
    get_queryset = lambda self: None
class IndexView(generic.ListView):
    template_name = 'index/index.html'
    model = userMeeting
    #context_object_name = 'latest_meeting_list'
    def get_queryset(self):
        #print(userMeeting.objects)
        return userMeeting.objects
        # return the most recent 300 meetings
        # return Meeting.objects.filter(
        #     creation_date__lte=timezone.now()
        # ).order_by('-creation_date')[:300]

# User profile related views
class ProfileView(generic.ListView):
    model = UserInfo
    template_name = 'index/profile.html'
    get_queryset = lambda self: UserInfo.objects
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        template_name = 'index/profile.html'
        # Add in a QuerySet of all the books
        try:
            context['bio'] = self.request.user.userbio.bio
            context['degree'] = self.request.user.userbio.degree            
            context['year'] = self.request.user.userbio.year
        except:
            UserBio.objects.create(user=self.request.user, bio="Default Bio", degree="????", year="????")
            context['bio'] = self.request.user.userbio.bio
            context['degree'] = self.request.user.userbio.degree
            context['year'] = self.request.user.userbio.year
        return context
        # def get_template_names(self):
        #     if self.request.user.username != context['user'].username:
        #         return 'index/view-profile.html'
        #     return 'index/profile.html'
        
class ProfileEditView(generic.UpdateView):
    form_class = ChangeProfileForm
    template_name = 'index/editprofile.html'
    success_url = reverse_lazy('index:profile')
    get_object = lambda self: self.request.user
def EditBio(request):
    if request.method == "POST":
        form = ChangeBioForm(request.POST, instance=request.user.userbio)
        if form.is_valid():
            post = form.save()
            post.save()
            return HttpResponseRedirect(reverse('index:profile'))
    else:
        form = ChangeBioForm(request.POST, instance=request.user.userbio)
    return render(request, 'index/editbio.html', {'form': form})


# def peek(request):
#     return render(request, 'index/editbio.html', {'form': form})