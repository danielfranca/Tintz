# -*- coding: iso-8859-1 -*-

import re

from django import forms
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils.encoding import smart_unicode
from profiles.models import *

from misc.utils import get_send_mail
send_mail = get_send_mail()

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from emailconfirmation.models import EmailAddress
from account.models import Account

from timezones.forms import TimeZoneField

import logging

alnum_re = re.compile(r'^\w+$')

class LoginForm(forms.Form):

    username = forms.CharField(label=_(u"Usu�rio ou E-mail"), max_length=60, widget=forms.TextInput(),
                error_messages = {'required': u'Campo Usu�rio � obrigat�rio.' } )
    password = forms.CharField(label=_(u"Senha"), widget=forms.PasswordInput(render_value=False),
                error_messages = {'required': u'Campo Senha � obrigat�rio.' } )
    remember = forms.BooleanField(label=_(u"Lembrar de mim"), required=False)

    user = None

    def clean(self):
        if self._errors:
            return
        username = self.cleaned_data["username"]

        if username.find('@') > -1:
            email = EmailAddress.objects.filter(email__iexact=username, verified=True)[0]
            username = email.user.username

        user = authenticate(username=username, password=self.cleaned_data["password"])
        
        email_address = EmailAddress.objects.get_primary(user)
        
        if user:
            if user.is_active and email_address != None:
                self.user = user
            else:
                raise forms.ValidationError(_(u"Esta conta est� inativa."))
        else:
            raise forms.ValidationError(_(u"Usu�rio ou senha incorretos."))
        return self.cleaned_data

    def login(self, request):
        if self.is_valid():
            login(request, self.user)
            #request.user.message_set.create(message=ugettext("Logado com sucesso com %(username)s.") % {'username': self.user.username})
            if self.cleaned_data['remember']:
                request.session.set_expiry(60 * 60 * 24 * 7 * 3)
            else:
                request.session.set_expiry(0)
            return True
        return False


class SignupForm(forms.Form):

    username  = forms.CharField(label=_(u"Usu�rio"), max_length=60, widget=forms.TextInput(), 
                               error_messages = {'required': u'Campo Usu�rio � obrigat�rio.' } )     
    email       = forms.EmailField(label=_(u"E-mail"), required=True, widget=forms.TextInput(), 
                                              error_messages = {'required': u'Campo Email � obrigat�rio.' } )
    password1  = forms.CharField(label=_(u"Senha"), widget=forms.PasswordInput(render_value=False), 
                                error_messages = {'required': u'Campo Senha � obrigat�rio.' } ) 
    password2  = forms.CharField(label=_(u"Redigite a Senha"), widget=forms.PasswordInput(render_value=False), 
                                error_messages = {'required': u'Por favor redigite sua senha.' } ) 
    confirmation_key = forms.CharField(max_length=40, required=False, widget=forms.HiddenInput(), 
                                       error_messages = {'required': u'Este campo � obrigat�rio.' } )
    
    def clean_username(self):
        if not alnum_re.search(self.cleaned_data["username"]):
            raise forms.ValidationError(_(u"Nome de Usu�rio deve conter apenas letras, n�meros e underscores."))
        try:
            user = User.objects.get(username__iexact=self.cleaned_data["username"])
        except User.DoesNotExist:
            return self.cleaned_data["username"]
        raise forms.ValidationError(_(u"Usu�rio j� existe. Escolha outro."))

    def clean_email(self):
        emails = []

        try:
            emails = EmailAddress.objects.filter(email=self.cleaned_data["email"])
        except:
            return

        if len(emails) == 0:
            return self.cleaned_data["email"]
        raise forms.ValidationError(_(u"Este email j� est� associado com uma conta."))

    def clean(self):
        if "password1" in self.cleaned_data and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                raise forms.ValidationError(_(u"Senhas n�o conferem."))
        return self.cleaned_data

    def save(self):
        username = self.cleaned_data["username"]
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password1"]
        
        new_user = User.objects.create_user(username, email, password)
        if email:
            #new_user.message_set.create(message=ugettext(u"Confirma��o enviada para %(email)s") % {'email': email})
            EmailAddress.objects.add_email(new_user, email)
        
        return username, password,  email # required for authenticate()


class ForgotPasswordForm(forms.Form):

    email       = forms.EmailField(label=_(u"E-mail"), required=True, widget=forms.TextInput(),
                                              error_messages = {'required': u'Campo Email � obrigat�rio.','invalid':u'E-mail informado � inv�lido' } )

    def clean_email(self):
 
        try:
            email = EmailAddress.objects.filter(email__iexact=self.cleaned_data["email"], verified=True)[0]
            user = email.user
            new_password = User.objects.make_random_password()
            user.set_password(new_password)
            user.save()
            subject = _("Tintz - Alterar Senha")
            message = render_to_string(u"account/password_reset_message.txt", {
                "user": user,
                "new_password": new_password,
            })
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], priority="high")

        except Exception, e:
            raise forms.ValidationError(_(u"Este email n�o possui conta associada."))
            return

class SignupCompleteForm(forms.Form):
   
    first_name      = forms.CharField(label=_(u'Nome'),  max_length=30, widget=forms.TextInput(), 
                                 error_messages = {'required': u'Campo Nome � obrigat�rio.' } ) 
    last_name = forms.CharField(label=_(u'Sobrenome'),  max_length=70, widget=forms.TextInput(), 
                                 error_messages = {'required': u'Campo Sobrenome � obrigat�rio.' } )
    birth_date = forms.DateField(('%d/%m/%Y',), label=_(u'Data Nasc.(dd/mm/aaaa)'),  widget=forms.DateTimeInput(format='%d/%m/%Y'), required=True, 
                                 error_messages = {'required': u'Campo Data Nasc. � obrigat�rio.', 'invalid':u'Informe uma data v�lida.' } )

    about     = forms.CharField(label=u'Sobre', widget=forms.Textarea,  required=False)
    interests = forms.CharField(label=u'Interesses', widget=forms.Textarea,  required=False)
    location = forms.CharField(label=u'Cidade',  required=False)
    state    = forms.ChoiceField(label=u'Estado', widget=forms.Select, choices=Profile.STATE_CHOICE,  required=False)
    country  = forms.CharField(label=u'Pa�s', required=False) 
    website  = forms.URLField(label=u'Website', required=False)
    #account_type  = forms.ModelChoiceField(label=u'Tipo da Conta',queryset=AccountType.objects.all(), required=True,
    #                                       error_messages = {'required': u'Favor escolher o tipo da conta.' })


    def clean(self):
        return self.cleaned_data

    def save(self, request):
        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]
        birth_date = self.cleaned_data["birth_date"]
        about = self.cleaned_data["about"]
        interests = self.cleaned_data["interests"]
        location = self.cleaned_data["location"]
        state = self.cleaned_data["state"]
        country = self.cleaned_data["country"]
        website = self.cleaned_data["website"]
        
        new_user = User.objects.get(username=request.user.username)
        #new_user.is_active = 1
        #new_user.save()
        
        create_profile(new_user, name=new_user.username)
        profile, created = Profile.objects.get_or_create(user=new_user)
        profile.first_name = first_name
        profile.last_name = last_name
        profile.birth_date = birth_date
        profile.about = about
        profile.interests = interests
        profile.location = location
        profile.state = state
        profile.country = country
        profile.website = website
        profile.save()

        return new_user.username, new_user.password, new_user.email # required for authenticate()


class OpenIDSignupForm(forms.Form):
    username = forms.CharField(label=_(u"Usu�rio"), max_length=30, widget=forms.TextInput())
    email = forms.EmailField(label=_(u"Email (opcional)"), required=False, widget=forms.TextInput())
    
    def __init__(self, *args, **kwargs):
        # Remember provided (validated!) OpenID to attach it to the new user later.
        self.openid = kwargs.pop("openid")
        # TODO: do something with this?
        reserved_usernames = kwargs.pop("reserved_usernames")
        super(OpenIDSignupForm, self).__init__(*args, **kwargs)
    
    def clean_username(self):
        if not alnum_re.search(self.cleaned_data["username"]):
            raise forms.ValidationError(_(u"Nome de Usu�rio deve conter apenas letras, n�meros e underscores."))
        try:
            user = User.objects.get(username__exact=self.cleaned_data["username"])
        except User.DoesNotExist:
            return self.cleaned_data["username"]
        raise forms.ValidationError(_(u"Usu�rio j� existe. Escolha outro."))

    def save(self):
        username = self.cleaned_data["username"]
        email = self.cleaned_data["email"]
        new_user = User.objects.create_user(username, "", "!")

        if email:
            #new_user.message_set.create(message=u"Confirma��o enviada para %s" % email)
            EmailAddress.objects.add_email(new_user, email)

        if self.openid:
            # Associate openid with the new account.
            new_user.openids.create(openid = self.openid)
        return new_user


class UserForm(forms.Form):

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(UserForm, self).__init__(*args, **kwargs)

class AccountForm(UserForm):

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        try:
            self.account = Account.objects.get(user=self.user)
        except Account.DoesNotExist:
            self.account = Account(user=self.user)


class AddEmailForm(UserForm):

    email = forms.EmailField(label=_("Email"), required=True, widget=forms.TextInput(attrs={'size':'60'}))

    def clean_email(self):
        try:
            EmailAddress.objects.get(email=self.cleaned_data["email"])
        except EmailAddress.DoesNotExist:
            return self.cleaned_data["email"]
        raise forms.ValidationError(_(u"Este email j� est� associado com uma conta."))

    def save(self):
        #self.user.message_set.create(message=ugettext(u"Confirma��o enviada para %(email)s") % {'email': self.cleaned_data["email"]})
        return EmailAddress.objects.add_email(self.user, self.cleaned_data["email"])


class ChangePasswordForm(UserForm):

    oldpassword = forms.CharField(label=_("Senha Atual"), widget=forms.PasswordInput(render_value=False))
    password1 = forms.CharField(label=_("Nova Senha"), widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label=_("Redigite Nova Senha"), widget=forms.PasswordInput(render_value=False))

    def clean_oldpassword(self):
        if not self.user.check_password(self.cleaned_data.get("oldpassword")):
            raise forms.ValidationError(_("Please type your current password."))
        return self.cleaned_data["oldpassword"]

    def clean_password2(self):
        if "password1" in self.cleaned_data and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                raise forms.ValidationError(_(u"Senhas n�o conferem."))
        return self.cleaned_data["password2"]

    def save(self):
        self.user.set_password(self.cleaned_data['password1'])
        self.user.save()
        #self.user.message_set.create(message=ugettext(u"Senha alterada com sucesso."))


class SetPasswordForm(UserForm):
    
    password1 = forms.CharField(label=_("Senha"), widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label=_("Redigite a Senha"), widget=forms.PasswordInput(render_value=False))
    
    def clean_password2(self):
        if "password1" in self.cleaned_data and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                raise forms.ValidationError(_(u"Senhas n�o conferem."))
        return self.cleaned_data["password2"]
    
    def save(self):
        self.user.set_password(self.cleaned_data["password1"])
        self.user.save()
        #self.user.message_set.create(message=ugettext(u"Senhada criada com sucesso."))

class ResetPasswordForm(forms.Form):

    email = forms.EmailField(label=_("Email"), required=True, widget=forms.TextInput(attrs={'size':'60'}))

    def clean_email(self):
        if EmailAddress.objects.filter(email__iexact=self.cleaned_data["email"], verified=True).count() == 0:
            raise forms.ValidationError(_("Email n�o verificado para a conta"))
        return self.cleaned_data["email"]

    def save(self):
        for user in User.objects.filter(email__iexact=self.cleaned_data["email"]):
            new_password = User.objects.make_random_password()
            user.set_password(new_password)
            user.save()
            subject = _("Tintz Alterar Senha")
            message = render_to_string("account/password_reset_message.txt", {
                "user": user,
                "new_password": new_password,
            })
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], priority="high")
        return self.cleaned_data["email"]


class ChangeTimezoneForm(AccountForm):

    timezone = TimeZoneField(label=_("Timezone"), required=True)

    def __init__(self, *args, **kwargs):
        super(ChangeTimezoneForm, self).__init__(*args, **kwargs)
        self.initial.update({"timezone": self.account.timezone})

    def save(self):
        self.account.timezone = self.cleaned_data["timezone"]
        self.account.save()
        #self.user.message_set.create(message=ugettext(u"Timezone successfully updated."))

class ChangeLanguageForm(AccountForm):

    language = forms.ChoiceField(label=_("Language"), required=True, choices=settings.LANGUAGES)

    def __init__(self, *args, **kwargs):
        super(ChangeLanguageForm, self).__init__(*args, **kwargs)
        self.initial.update({"language": self.account.language})

    def save(self):
        self.account.language = self.cleaned_data["language"]
        self.account.save()
        #self.user.message_set.create(message=ugettext(u"Language successfully updated."))


# @@@ these should somehow be moved out of account or at least out of this module

from account.models import OtherServiceInfo, other_service, update_other_services

class TwitterForm(UserForm):
    username = forms.CharField(label=_("Username"), required=True)
    password = forms.CharField(label=_("Password"), required=True,
                               widget=forms.PasswordInput(render_value=False))

    def __init__(self, *args, **kwargs):
        super(TwitterForm, self).__init__(*args, **kwargs)
        self.initial.update({"username": other_service(self.user, "twitter_user")})

    def save(self):
        from microblogging.utils import get_twitter_password
        update_other_services(self.user,
            twitter_user = self.cleaned_data['username'],
            twitter_password = get_twitter_password(settings.SECRET_KEY, self.cleaned_data['password']),
        )
        #self.user.message_set.create(message=ugettext(u"Successfully authenticated."))
