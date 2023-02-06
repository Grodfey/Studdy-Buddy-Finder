from django.urls import path

from . import views

app_name = 'index'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit', views.ProfileEditView.as_view(), name='editprofile'),
    path('profile/editBio/', views.EditBio, name='editbio'),
    path('profile/removeClass/', views.removeClass, name='removeClass'),
    path('profile/removeFriend/', views.removeFriend, name='removeFriend'),
    #path('profile/edit/confirm', views.confirmedit, name='confirmprofile'),
    #path('search/', views.SearchView.as_view(), name='search'),
    path('meetings/', views.MeetingsView.as_view(), name='meetings'),
    path('meetings/add', views.MeetingAddView.as_view(), name='addmeeting'),
    path('meetings/confirm/', views.addMeeting, name='confirmMeeting'),
    path('meetings/join/', views.joinMeeting, name='joinMeeting'),
    # Add classes
    # # Legacy
    path('search/', views.class_search, name='class_search'),
    path('search/results/', views.get_Results, name='class_results'),
    # # Newer
    # path('classes/search/', views.class_search_dummy, name='class_search_new'),
    # path('classes/results/', views.ClassResultsListView, name='class_results_new'),
    # # Success
    path('search/results/class_success/', views.class_success, name='class_success'),
    # Add users
    path('usersearch/', views.usersearch, name='usersearch'),
    path('usersearch/results/', views.UserResultsListView.as_view(), name='userresults'),
    path('usersearch/addedFriend/', views.addedFriend, name='addedFriend'),
    # path('view/', views.addedFriend, name='addedFriend'),
    
]