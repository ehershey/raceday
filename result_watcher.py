#!/usr/bin/python
import argparse
import ConfigParser
from email.mime.text import MIMEText
import mechanize
import os
import os.path
import simplejson
import smtplib
import sys

RCFILE = os.environ['HOME'] + '/.nanowatcherrc'

CONFIGFILE = "result_watcher.json"

config = simplejson.load(open(CONFIGFILE))

print "mongo host is %s" % config['mongo_host']
exit


config = ConfigParser.ConfigParser(defaults = { "notify-email-from": "", "notify-email-to": ''})
config.read(RCFILE)

# to allow dynamic home substitution in values - i.e.  
# file = %(HOME)s/Dropbox/PlainText/Nano/text.txt
#
config.set('nanowatcher', 'HOME', os.environ['HOME'])

parser = argparse.ArgumentParser(description='Update nanowrimo word count.')

parser.add_argument('--novel-file', help='File containing novel content.', required = False)
parser.add_argument('--username', help='nanowrimo username.', required = False)
parser.add_argument('--password', help='nanowrimo password.', required = False)
parser.add_argument('--notify-email-from', help='Email address to send update notification from.', required = False)
parser.add_argument('--notify-email-to', help='Email address to send update notification to.', required = False)

args = parser.parse_args()

novel_file = args.novel_file or config.get("nanowatcher","novel-file")
username = args.username or config.get("nanowatcher","username")
password = args.password or config.get("nanowatcher","password")
notify_email_from = args.notify_email_from or config.get("nanowatcher","notify-email-from") or ""
notify_email_to = args.notify_email_to or config.get("nanowatcher","notify-email-to") or ""

novel_dir = os.path.dirname(novel_file)

print "monitoring %s" % novel_file

# log in to nanowrimo site
#

print "running br = mechanize.Browser()"
br = mechanize.Browser()

print "running br.open(\"http://www.nanowrimo.org/user\")"
br.open("http://www.nanowrimo.org/user")
print "running assert br.viewing_html()"
assert br.viewing_html()

print "running br.select_form(nr=0)"
br.select_form(nr=0)

print "running br.form.set_value(name=\"name\",value=username)"
br.form.set_value(name="name",value=username)

print "running br.form.set_value(name='pass',value=password)"
br.form.set_value(name='pass',value=password)

print "running br.submit()"
br.submit()
print "running assert br.viewing_html()"
assert br.viewing_html()

print "running assert br.title().index(username)== 0"
assert br.title().index(username) == 0

def process_update():
  try:
    textf = open(novel_file, 'r')
  except IOError:
    print 'Cannot open file %s for reading' % novel_file
    sys.exit(0)
  words = 0
  for line in textf:
    tempwords = line.split(None)
    # word total count
    words += len(tempwords)

  print "running br.select_form(nr=0)"
  br.select_form(nr=0)

  print "running br.form.controls[0].value = \"%d\" " % words
  br.form.controls[0].value = "%d" % words
  print "running br.submit()"
  br.submit()

  print "running assert br.viewing_html()"
  assert br.viewing_html()

  if notify_email_from and notify_email_to:
    # Create a text/plain message
    msg = MIMEText('EOM')
  
    msg['Subject'] = 'Updated Nanowrimo word count to: %d' % words
    msg['From'] = notify_email_from
    msg['To'] = notify_email_to
  
    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP("localhost")
    s.sendmail(notify_email_from, [notify_email_to], msg.as_string())
    s.quit()
  
  



handler = EventHandler()

wdd = wm.add_watch(novel_dir, mask)
notifier.loop()





