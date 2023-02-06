from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Member, UserInfo, Friend, Meeting, UserBio, userMeeting #, Course

class UserInline(admin.TabularInline):
    model = UserInfo
    extra = 1

class MeetingMemberInline(admin.TabularInline):
    model = userMeeting
    extra = 1

class MemberInline(admin.TabularInline):
    model = Member
    extra = 1

class UserBioInline(admin.TabularInline):
    model = UserBio

class UserInfoAdmin(UserAdmin):
    inlines = [UserInline, MeetingMemberInline, UserBioInline]
    #list_display = ('user', 'class_subject', 'class_number', 'class_section')

class userMeetingAdmin(admin.ModelAdmin):
    inlines = [userMeeting]

class MeetingAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title_text']}),  # Title
        (None, {'fields': ['description_text']}),
        (None, {'fields': ['owner_text']}),
        ('Date information', {'fields': ['creation_date', 'start_date', 'end_date'], 'classes': ['collapse']}),]
    inlines = [MemberInline]
    list_display = ('title_text', 'creation_date', 'description_text', 'start_date', 'end_date')
    list_filter = ['creation_date']
    search_fields = ['title_text']

# class CourseAdmin(admin.ModelAdmin):
#     list_display: ('course_name', 'instructor',)


# Register your models here..
# admin.site.register(Course, CourseAdmin)
admin.site.unregister(User)
admin.site.register(User, UserInfoAdmin)
# admin.site.register(userMeeting, userMeetingAdmin)
admin.site.register(Meeting, MeetingAdmin)