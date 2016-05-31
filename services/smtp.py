#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = 'Jan-Piet Mens <jpmens()gmail.com>'
__copyright__ = 'Copyright 2014 Jan-Piet Mens'
__license__   = """Eclipse Public License - v 1.0 (http://www.eclipse.org/legal/epl-v10.html)"""

import smtplib
from email.mime.text import MIMEText

def plugin(srv, item):
    """Send a message to SMTP recipient(s)."""

    srv.logging.debug("*** MODULE=%s: service=%s, target=%s", __file__, item.service, item.target)

    smtp_addresses = item.addrs

    server      = item.config['server']
    sender      = item.config['sender']
    starttls    = item.config['starttls']
    username    = item.config['username']
    password    = item.config['password']

    msg = MIMEText(item.message)
    msg['Subject']      = item.get('title', "%s notification" % (srv.SCRIPTNAME))
    msg['To']           = ", ".join(smtp_addresses)
    msg['From']         = sender
    msg['X-Mailer']     = srv.SCRIPTNAME

    if not smtp_addresses:
        srv.logging.warn("Skipped sending SMTP notification to %s, "
                         "no addresses configured" % (item.target))
        return False

    try:
        srv.logging.debug("Sending SMTP notification to %s, addresses: %s" % (item.target, smtp_addresses))
        server = smtplib.SMTP(server)
        server.set_debuglevel(0)
        server.ehlo()
        if starttls:
            server.starttls()
        if username:
            server.login(username, password)
        server.sendmail(sender, smtp_addresses, msg.as_string())
        server.quit()
        srv.logging.debug("Successfully sent SMTP notification")
    except Exception, e:
        srv.logging.warn("Error sending notification to SMTP recipient %s, addresses: %s. "
                         "Exception: %s" % (item.target, smtp_addresses, str(e)))
        return False

    return True
