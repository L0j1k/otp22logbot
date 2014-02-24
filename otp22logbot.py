#!/usr/bin/python3

##
#. @project OTP22 Log Bot
#. This bot logs an IRC channel to a file. It also provides a small
#. number of additional features related to users and their content.
#. @file otp22logbot.py
#. This is the primary application driver file.
#. @author L0j1k
#. @contact L0j1k@L0j1k.com
#. @license BSD3
#. @version 0.0.1_pre-alpha

import argparse, os, socket, sys

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--channel',
  help='IRC channel to join. Default "otp22"',
  default='ircugm',
  nargs='?',
  type=str
)
parser.add_argument('-i', '--init',
  help='Specify initialization/configuration file for logbot',
  default=False,
  nargs='?',
  type=argparse.FileType('r')
)
parser.add_argument('-k', '--kill',
  help='Kill password to stop bot. Default "killme"',
  default='killme',
  nargs='?',
  type=str
)
parser.add_argument('-n', '--nick',
  help='IRC nick name. Default "otp22logbot"',
  default='otp22logbot',
  nargs='?',
  type=str
)
parser.add_argument('-o', '--output',
  help='Output log filename. Default "otp22logbot.log"',
  default='otp22logbot.log',
  nargs='?',
  type=argparse.FileType('w')
)
parser.add_argument('-p', '--port',
  help='IRC port to use. Default 6667',
  default=6667,
  nargs='?',
  type=int
)
parser.add_argument('-r', '--real',
  help='IRC real name. Default "otp22logbot"',
  default='otp22logbot',
  nargs='?',
  type=str
)
parser.add_argument('-s', '--server',
  help='IRC server to connect to. Default "irc.freenode.net"',
  default='irc.freenode.net',
  nargs='?',
  type=str
)
parser.add_argument('-u', '--user',
  help='IRC user name. Default "otp22logbot"',
  default='otp22logbot',
  nargs='?',
  type=str
)
app_args = parser.parse_args()

def sysprint( data ):
  sys.stdout.write(data)
  sys.stdout.flush()

## @todo stub
def process_command( command ):
  sysprint(command)

command_exit = False
app_data = {
  'kill': False,
  'overlord': 'L0j1k',
  'version': '0.0.1_prealpha'
}
sockbuffer = "";

##@debug
sysprint('==>['+str(app_data['overlord'])+']\n')

#while command_exit == False:
sysprint('otp22logbot.py '+app_data['version']+' by L0j1k\n')
if (app_args.init != False):
  sysprint('[+] using configuration file: '+str(app_args.init.name)+'\n')
sysprint('[+] using output logfile '+str(app_args.output.name)+'\n')
sysprint('[+] using server '+str(app_args.server)+' on port '+str(app_args.port)+'\n')

sock = socket.socket()
sock.connect((app_args.server, app_args.port))

## @todo accept a server password
#if (app_args.password != False):
#  sock.send(bytes('PASS '+app_args.password+'\r\n'), 'utf-8')
sock.send(bytes('NICK '+app_args.nick+'\r\n', 'utf-8'))
sock.send(bytes('USER '+app_args.user+' '+app_args.server+' default :'+app_args.real+'\r\n', 'utf-8'))
sock.send(bytes('JOIN #'+app_args.channel+'\r\n', 'utf-8'))
sock.send(bytes('PRIVMSG '+app_data['overlord']+': Greetings, overlord. I am for you.\r\n', 'utf-8'))

while app_data['kill'] == False:
  sock_buffer = sock.recv(1024).decode('utf-8')
  sysprint(sock_buffer)
  if (sock_buffer.find('PING') != -1):
    sock.send(bytes('PONG '+sock_buffer.split()[1]+'\n', 'utf-8'))
  if (sock_buffer.find('PRIVMSG') != -1):
    message = sock_buffer.split(':')
    message_header = message[1].split()
    message_body = message[2].split()
    this_command = message_body[0]
    this_extra = message_body[1]
    this_requester = message_header[1]
    if (this_command.find('@help') != -1):
      sock.send(bytes('PRIVMSG '+this_requester+': \n', 'utf-8'))
    if (this_command.find('@kill') != -1):
      if (this_extra == 'killme'):
        app_data['kill'] = True
        sock.send(bytes('PRIVMSG '+this_requester+': With urgency, my lord. Dying at your request.\n', 'utf-8'))
    if (this_command.find('@last') != -1):
      sock.send(bytes('PRIVMSG '+this_requester+': \n', 'utf-8'))
    if (this_command.find('@version') != -1):
      sock.send(bytes('PRIVMSG '+this_requester+': \n', 'utf-8'))
