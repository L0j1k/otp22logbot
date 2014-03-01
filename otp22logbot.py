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
#. @version 0.0.2a

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

def socksend( socket, data ):
  if (app_data['debug'] == True):
    sysprint('=>['+data+']')
  socket.send(bytes(data+'\r\n', 'utf-8'))

def sysprint( data ):
  sys.stdout.write(data)
  sys.stdout.flush()

## @todo stub
def process_command( command ):
  sysprint(command)

command_exit = False
app_data = {
  'debug': True,
  'kill': False,
  'overlord': 'L0j1k',
  'phase': 'a',
  'version': '0.0.2'
}
sockbuffer = "";

sysprint('otp22logbot.py '+app_data['version']+app_data['phase']+' by L0j1k\n')
if (app_args.init != False):
  sysprint('[+] using configuration file: '+str(app_args.init.name)+'\n')
sysprint('[+] using output logfile '+str(app_args.output.name)+'\n')
sysprint('[+] using server '+str(app_args.server)+' on port '+str(app_args.port)+'\n')

sock = socket.socket()
sock.connect((app_args.server, app_args.port))

## @todo accept a server password
#if (app_args.password != False):
#  sock.send(bytes('PASS '+app_args.password+'\r\n'), 'utf-8')
socksend(sock, 'NICK '+app_args.nick)
socksend(sock, 'USER '+app_args.user+' '+app_args.server+' default :'+app_args.real)
socksend(sock, 'JOIN #'+app_args.channel)
socksend(sock, 'PRIVMSG '+app_data['overlord']+' :Greetings, overlord. I am for you.')
socksend(sock, 'PRIVMSG #'+app_args.channel+' :I am a logbot and I am ready!')

## @debug
# ==>outgoing private message
#:sendak.freenode.net 401 otp22logbot L0j1k: :No such nick/channel
# ==>inbound channel traffic
#:L0j1k!~default@unaffiliated/l0j1k PRIVMSG #ircugm :hello
#:L0j1k!~default@unaffiliated/l0j1k PRIVMSG #ircugm :foo bar
# ==>inbound private message
#:L0j1k!~default@unaffiliated/l0j1k PRIVMSG otp22logbot :hello
#:L0j1k!~default@unaffiliated/l0j1k PRIVMSG otp22logbot :little bunny foo foo

while app_data['kill'] == False:
  sock_buffer = sock.recv(1024).decode('utf-8')
  sendbuffer = ""
  sysprint(sock_buffer)
  if (sock_buffer.find('PING') != -1):
    socksend(sock, 'PONG '+sock_buffer.split()[1]+'\n')
  if (sock_buffer.find('PRIVMSG') != -1):
    ## @debug1
    sysprint('handling shit...\n')
    ## @task handle input lengths. do not parse input of varied lengths.
    message = sock_buffer.split(':')
    ## @debug1
    sysprint('len(msg)['+str(len(message))+']\n')
    if (len(message) != 3):
      continue
    else:
      message_header = message[1].strip().split(' ')
      message_body = message[2].strip().split(' ')
    ## @debug2
    print(message_header)
    print(message_body)
    if (len(message_body) == 0):
      continue
    elif (len(message_body) > 3):
      continue
    this_command = False
    this_parameter = False
    this_modifier = False
    if (len(message_body) > 0):
      this_command = message_body[0]
    if (len(message_body) > 1):
      this_parameter = message_body[1]
    if (len(message_body) > 2):
      this_modifier = message_body[2]
    if (len(message_header) > 0):
      this_channel = message_header[2]
      this_requester = message_header[0].split('!')[0]
    else:
      continue
    ## @debug1
    sysprint('cmd['+str(this_command)+'] param['+str(this_parameter)+'] mod['+str(this_modifier)+'] req['+str(this_requester)+']\n')
    if (this_command == '.help'):
      this_help = "Eat me. There's your help!"
      socksend(sock, 'PRIVMSG '+str(this_channel)+' :'+this_help)
    if (this_command == '.last'):
      socksend(sock, 'PRIVMSG '+str(this_channel)+' :')
    if (this_command == '.version'):
      socksend(sock, 'PRIVMSG '+str(this_channel)+' :'+app_data['version']+app_data['phase']+' by '+app_data['overlord'])
    if (this_requester != app_args.channel):
      if (this_command == '.kill'):
        if (this_parameter == 'killme'):
          if (this_modifier == 'now'):
            app_data['kill'] = True
          socksend(sock, 'PRIVMSG '+str(this_requester)+' :With urgency, my lord. Dying at your request.')
          socksend(sock, 'QUIT :killed by '+str(this_requester))
