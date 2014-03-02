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
#. @version 0.0.4a

import argparse, datetime, os, socket, sys

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

def filesend( handle, data ):
  if (app_data['debug'] == True):
    sysprint('=WRITING=>['+data+']\n')
  handle.write(str(data))

def socksend( socket, data ):
  if (app_data['debug'] == True):
    sysprint('=SENDING=>['+data+']\n')
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
  'timeformat': '%H:%M:%S',
  'version': '0.0.4'
}
sockbuffer = "";

sysprint('otp22logbot.py '+app_data['version']+app_data['phase']+' by L0j1k\n')
sysprint('[+] started at '+datetime.datetime.now().strftime(app_data['timeformat']+'\n'))
if (app_args.init != False):
  sysprint('[+] using configuration file: '+app_args.init.name+'\n')
sysprint('[+] using output logfile '+app_args.output.name+'\n')
sysprint('[+] using server '+app_args.server+' on port '+str(app_args.port)+'\n')
sysprint('[+] using timestamp format '+app_data['timeformat']+'\n')

sock = socket.socket()
sock.connect((app_args.server, app_args.port))

## @todo accept a server password
#if (app_args.password != False):
#  sock.send(bytes('PASS '+app_args.password+'\r\n'), 'utf-8')
socksend(sock, 'NICK '+app_args.nick)
socksend(sock, 'USER '+app_args.user+' '+app_args.server+' default :'+app_args.real)
socksend(sock, 'JOIN #'+app_args.channel)
socksend(sock, 'PRIVMSG '+app_data['overlord']+' :Greetings, overlord. I am for you.')
socksend(sock, 'PRIVMSG #'+app_args.channel+' :I am a logbot and I am ready! Use ".help" for help.')

## @debug
# ==>outgoing private message
#:sendak.freenode.net 401 otp22logbot L0j1k: :No such nick/channel
# ==>inbound channel traffic
#:L0j1k!~default@unaffiliated/l0j1k PRIVMSG #ircugm :hello
#:L0j1k!~default@unaffiliated/l0j1k PRIVMSG #ircugm :foo bar
# ==>inbound private message
#:L0j1k!~default@unaffiliated/l0j1k PRIVMSG otp22logbot :hello
#:L0j1k!~default@unaffiliated/l0j1k PRIVMSG otp22logbot :little bunny foo foo
last_message = ''
this_message = ''
users = {}

while app_data['kill'] == False:
  this_time = datetime.datetime.now().strftime(app_data['timeformat'])
  sock_buffer = sock.recv(1024).decode('utf-8')
  sendbuffer = ""
  ## @debug1
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
    if (len(message_header) > 0):
      this_channel = str(message_header[2])
      this_requester = str(message_header[0].split('!')[0])
    ## @task handle regular messages to the channel
    last_message = this_message
    this_message = '<'+this_time+'> '+this_requester+' ('+this_channel+'): '+message[2]
    users[this_requester] = {
      'channel': this_channel,
      'message': message[2],
      'seen': this_time
    }
    filesend(app_args.output, this_message)
    if (len(message_body) > 3):
      continue
    this_command = False
    this_parameter = False
    this_modifier = False
    if (len(message_body) > 0):
      this_command = str(message_body[0])
    if (len(message_body) > 1):
      this_parameter = str(message_body[1])
    if (len(message_body) > 2):
      this_modifier = str(message_body[2])
    ## @debug1
    sysprint('cmd['+this_command+'] param['+this_parameter+'] mod['+this_modifier+'] req['+this_requester+']\n')
    if (this_command == '.flush'):
      socksend(sock, 'PRIVMSG '+this_channel+' :Flushing and rotating logfiles...')
    elif (this_command == '.help'):
      if (this_parameter == False):
        send_message = 'Available commands (use .help <command> for more help): flush, help, kill, last, user, version'
      elif (this_parameter == 'flush'):
        send_message = ".flush: flush and rotate logfiles"
      elif (this_parameter == 'help'):
        send_message = ".help <command>: lists help for a specific command"
      elif (this_parameter == 'kill'):
        send_message = ".kill: attempts to kill this bot (good luck)"
      elif (this_parameter == 'last'):
        send_message = ".last [user]: displays last message received. if [user] is specified, displays last message sent by user"
      elif (this_parameter == 'user'):
        send_message = ".user [user]: displays information about user. if unspecified, defaults to command requester"
      elif (this_parameter == 'version'):
        send_message = ".version: displays version information"
      socksend(sock, 'PRIVMSG '+this_channel+' :'+send_message)
    elif (this_command == '.last'):
      socksend(sock, 'PRIVMSG '+this_channel+' :'+last_message)
    elif (this_command == '.user'):
      socksend(sock, 'PRIVMSG '+this_channel+' :user')
    elif (this_command == '.version'):
      socksend(sock, 'PRIVMSG '+this_channel)+' :'+app_data['version']+app_data['phase']+' by '+app_data['overlord'])
    elif (this_requester != app_args.channel):
      if (this_command == '.kill'):
        if (this_parameter == app_args.kill):
          if (this_modifier == 'now'):
            app_data['kill'] = True
          socksend(sock, 'PRIVMSG '+this_requester+' :With urgency, my lord. Dying at your request.')
          socksend(sock, 'PRIVMSG '+this_channel+' :Goodbye!')
          socksend(sock, 'QUIT :killed by '+this_requester)

end_message = '[+] CONNECTION STOPPED ... dying at '+datetime.datetime.now().strftime(app_data['timeformat']+'\n')
filesend(app_args.output, end_message)
sysprint(end_message)
app_args.output.close()
