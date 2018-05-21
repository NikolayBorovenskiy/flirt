from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from accounts.forms import UserChangeForm, UserCreationForm
from accounts.models import DatingUser
from bookmarks.models import Bookmark


class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['date_created', 'owner']
    search_fields = ['owner__email']
    fields = ['owner', 'marked_user_id']
    exclude = ['date_created']

    class Meta:
        model = Bookmark


class BookmarkInLine(admin.TabularInline):
    model = Bookmark


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'last_name', 'first_name', 'avatar')}),
        ('Personal info', {'fields': (
            'gender', 'date_of_birth', 'country', 'university', 'job', 'bio')}),
        ('Social networks', {'fields': ('twitter', 'facebook', 'instagram',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'date_of_birth', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    inlines = [BookmarkInLine]


# Now register the new UserAdmin...
admin.site.register(DatingUser, UserAdmin)
admin.site.register(Bookmark, BookmarkAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
