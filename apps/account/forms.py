# -*- coding: utf-8 -*-

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

from tintzsettings.models import TintzSettings

import datetime

import logging

alnum_re = re.compile(r'^\w+$')

class LoginForm(forms.Form):

    username = forms.CharField(label=_(u"Usuário ou E-mail"), max_length=60, widget=forms.TextInput(),
                error_messages = {'required': u'Campo Usuário é obrigatório.' } )
    password = forms.CharField(label=_(u"Senha"), widget=forms.PasswordInput(render_value=False),
                error_messages = {'required': u'Campo Senha é obrigatório.' } )
    remember = forms.BooleanField(label=_(u"Lembrar de mim"), required=False)

    user = None

    def clean(self):
        if self._errors:
            return
        username = self.cleaned_data["username"].lower()

        if username.find('@') > -1:
            try:
                email = EmailAddress.objects.filter(email__iexact=username, verified=True)[0]
                username = email.user.username
            except IndexError:
                raise forms.ValidationError(_(u"Usuário ou senha incorretos."))

        user = authenticate(username=username, password=self.cleaned_data["password"])

        email_address = EmailAddress.objects.get_primary(user)

        if user:
            if user.is_active and email_address != None:
                self.user = user
            else:
                raise forms.ValidationError(_(u"Esta conta está inativa."))
        else:
            raise forms.ValidationError(_(u"Usuário ou senha incorretos."))
        return self.cleaned_data

    def login(self, request):
        if self.is_valid():
            self.user.username = self.user.username.lower()
            login(request, self.user)
            #request.user.message_set.create(message=ugettext("Logado com sucesso com %(username)s.") % {'username': self.user.username})
            if self.cleaned_data['remember']:
                request.session.set_expiry(60 * 60 * 24 * 7 * 3)
            else:
                request.session.set_expiry(0)
            return True
        return False


class SignupForm(forms.Form):

    username  = forms.CharField(label=_(u"Usuário"), max_length=60, widget=forms.TextInput(),
                               error_messages = {'required': u'Campo Usuário é obrigatório.' } )
    email       = forms.EmailField(label=_(u"E-mail"), required=True, widget=forms.TextInput(),
                                              error_messages = {'required': u'Campo Email é obrigatório.', 'invalid':u'Email inválido.' } )
    password1  = forms.CharField(label=_(u"Senha"), widget=forms.PasswordInput(render_value=False),
                                error_messages = {'required': u'Campo Senha é obrigatório.' } )
    password2  = forms.CharField(label=_(u"Redigite a Senha"), widget=forms.PasswordInput(render_value=False),
                                error_messages = {'required': u'Por favor redigite sua senha.' } )
    confirmation_key = forms.CharField(max_length=40, required=False, widget=forms.HiddenInput(),
                                       error_messages = {'required': u'Este campo é obrigatório.' } )

    def clean_username(self):
        if not alnum_re.search(self.cleaned_data["username"]):
            raise forms.ValidationError(_(u"Nome de Usuário deve conter apenas letras, números e underscores."))
        try:
            user = User.objects.get(username__iexact=self.cleaned_data["username"])
        except User.DoesNotExist:
            return self.cleaned_data["username"]
        raise forms.ValidationError(_(u"Usuário já existe. Escolha outro."))

    def clean_email(self):
        emails = []

        try:
            emails = EmailAddress.objects.filter(email=self.cleaned_data["email"])
        except:
            return

        if len(emails) == 0:
            return self.cleaned_data["email"]
        raise forms.ValidationError(_(u"Este email já está associado com uma conta."))

    def clean(self):
        if "password1" in self.cleaned_data and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                raise forms.ValidationError(_(u"Senhas não conferem."))
        return self.cleaned_data

    def save(self):
        username = self.cleaned_data["username"].lower()
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password1"]

        new_user = User.objects.create_user(username, email, password)
        if email:
            #new_user.message_set.create(message=ugettext(u"Confirmação enviada para %(email)s") % {'email': email})
            EmailAddress.objects.add_email(new_user, email)

        return username, password,  email # required for authenticate()


class ForgotPasswordForm(forms.Form):

    email       = forms.EmailField(label=_(u"E-mail"), required=True, widget=forms.TextInput(),
                                              error_messages = {'required': u'Campo Email é obrigatório.','invalid':u'E-mail informado é inválido' } )

    def clean_email(self):

        try:
            email = EmailAddress.objects.filter(email__iexact=self.cleaned_data["email"], verified=True)[0]
            user = email.user
            new_password = User.objects.make_random_password()
            user.set_password(new_password)
            user.save()

            self.user = user
            self.new_password = new_password
            self.email_address = email

        except Exception, e:
            raise forms.ValidationError(_(u"Este email não possui conta associada."))
            return

class ResendConfirmationForm(forms.Form):

    email       = forms.EmailField(label=_(u"E-mail"), required=True, widget=forms.TextInput(),
                                              error_messages = {'required': u'Campo Email é obrigatório.','invalid':u'E-mail informado é inválido' } )

    def clean(self):
        if self._errors:
            return
        email = self.cleaned_data["email"].lower()

        try:
            self.user = User.objects.get(email = email)
        except User.DoesNotExist:
            raise forms.ValidationError(_(u"Não existe usuário associado a esse email."))

        self.email_address = EmailAddress.objects.get_primary(self.user)

        if self.user:
            if self.user.is_active and self.email_address != None:
                raise forms.ValidationError(_(u"Esta conta não está inativa."))

        self.email_address = email

        return self.cleaned_data




class SignupCompleteForm(forms.Form):

    first_name      = forms.CharField(label=_(u'Nome'),  max_length=30, widget=forms.TextInput(),
                                 error_messages = {'required': u'Campo Nome é obrigatório.' } )
    last_name = forms.CharField(label=_(u'Sobrenome'),  max_length=70, widget=forms.TextInput(),
                                 error_messages = {'required': u'Campo Sobrenome é obrigatório.' } )
    birth_date = forms.DateField(('%d/%m/%Y',), label=_(u'Data Nasc.(dd/mm/aaaa)'), widget=forms.DateTimeInput(format='%d/%m/%Y'), required=True,
                                 error_messages = {'required': u'Campo Data Nasc. é obrigatório.', 'invalid':u'Informe uma data válida.' } )

    about     = forms.CharField(label=u'Sobre', widget=forms.Textarea,  required=False)
    interests = forms.CharField(label=u'Interesses', widget=forms.Textarea,  required=False)
    location = forms.CharField(label=u'Cidade',  required=False)
    state    = forms.ChoiceField(label=u'Estado', widget=forms.Select, choices=Profile.STATE_CHOICE,  required=False)
    country  = forms.CharField(label=u'País', required=False)
    website  = forms.URLField(label=u'Website', required=False)
    terms    = forms.BooleanField(label=u'Li e concordo', required=False,  initial=False)
    #account_type  = forms.ModelChoiceField(label=u'Tipo da Conta',queryset=AccountType.objects.all(), required=True,
    #                                       error_messages = {'required': u'Favor escolher o tipo da conta.' })


    def clean(self):
        if "birth_date" in self.cleaned_data:
            birth_date = self.cleaned_data["birth_date"]
            if birth_date >= datetime.date.today():
                raise forms.ValidationError(_(u"Data de nascimento maior ou igual a data atual."))

        if "terms" not in self.cleaned_data or not self.cleaned_data["terms"]:
            raise forms.ValidationError(_(u"É obrigatório ler e concordar com os termos de uso para continuar."))

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

        #Creating default settings
        tintzSettings = TintzSettings()

        tintzSettings.email_follow = True
        tintzSettings.email_publication = True
        tintzSettings.email_post = True
        tintzSettings.user = new_user
        tintzSettings.save()

        return new_user.username, new_user.password, new_user.email # required for authenticate()


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
        raise forms.ValidationError(_(u"Este email já está associado com uma conta."))

    def save(self):
        #self.user.message_set.create(message=ugettext(u"Confirmação enviada para %(email)s") % {'email': self.cleaned_data["email"]})
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
                raise forms.ValidationError(_(u"Senhas não conferem."))

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
                raise forms.ValidationError(_(u"Senhas não conferem."))

        return self.cleaned_data["password2"]

    def save(self):
        self.user.set_password(self.cleaned_data["password1"])
        self.user.save()
        #self.user.message_set.create(message=ugettext(u"Senhada criada com sucesso."))


class ResetPasswordForm(forms.Form):

    email = forms.EmailField(label=_("Email"), required=True, widget=forms.TextInput(attrs={'size':'60'}))

    def clean_email(self):
        if EmailAddress.objects.filter(email__iexact=self.cleaned_data["email"], verified=True).count() == 0:
            raise forms.ValidationError(_("Email não verificado para a conta"))

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

