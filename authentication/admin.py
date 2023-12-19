from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField


from .models import AuthUser
from .models import Schedule


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password Confirmation", widget=forms.PasswordInput)

    class Meta:
        model = AuthUser
        fields = ('username', 'email', 'contact_number', 'date_of_birth', 'bmdc_reg_number', 'image', 'about')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label= ("Password"),
        help_text= ("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"../password/\">this form</a>."))


    class Meta:
        model = AuthUser
        fields = ('username', 'email', 'password' ,'contact_number', 'date_of_birth', 'bmdc_reg_number', 'about', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]



class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 1




class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('name', 'username', 'email','is_active','is_admin')
    list_filter = ( 'is_active',)
    fieldsets = (
        (None,{'fields': ('username', 'email','password')}),
        ("Personal Info",{'fields':('name','contact_number', 'date_of_birth', 'bmdc_reg_number','about','image')}),
        ("Authority",{"fields":('is_active', 'is_admin')}),
    )

    add_fieldsets = (
        (None,{
            'classes': 'wide',
            'fields' : ('username', 'email', 'name', 'contact_number', 'bmdc_reg_number', 'date_of_birth','image','about', 'password1', 'password2')
        }),
    )

    search_fields = ('name', 'email')
    ordering = ('name', 'email',)
    filter_horizontal = ()
    inlines = [ ScheduleInline,]


admin.site.register(AuthUser, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Schedule)