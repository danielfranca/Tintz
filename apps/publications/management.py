# -*- coding: iso-8859-1 -*-
from django.conf import settings
from django.db.models import signals
from django.utils.translation import ugettext_noop as _

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification

    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type("publication_follow_post", _(u"Nova Publica��o"), _(u"uma nova publica��o foi criada por um autor que voc� segue"), default=2, to_follow=True)
        notification.create_notice_type("publication_post_comment", _(u"Novo Coment�rio em suas Publica��es"), _(u"um coment�rio foi adicionado em uma de suas publica��es"), default=2)

    signals.post_syncdb.connect(create_notice_types, sender=notification)
else:
    print "Skipping creation of NoticeTypes as notification app not found"
