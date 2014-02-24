OTP22 Log Bot
=============

This Python-based IRC channel bot logs channel content to a local file. 
It also provides a few simple log review and user statistic commands.

        usage: otp22logbot.py [-h] [-c [CHANNEL]] [-i [INIT]] [-n [NICK]]
          [-o [OUTPUT]] [-p [PORT]] [-r [REALNAME]] [-s [SERVER]]
          [-u [USERNAME]]

        optional arguments:
          -h, --help
            show this help message and exit
          -c [CHANNEL], --channel [CHANNEL]
            IRC channel to join. Default "otp22"
          -i [INIT], --init [INIT]
            Specify initialization/configuration file for logbot
          -n [NICK], --nick [NICK]
            IRC nick name. Default "otp22logbot"
          -o [OUTPUT], --output [OUTPUT]
            Output log filename. Default "otp22logbot.log"
          -p [PORT], --port [PORT]
            IRC port to use. Default 6667
          -r [REALNAME], --realname [REALNAME]
            IRC real name. Default "otp22logbot"
          -s [SERVER], --server [SERVER]
            IRC server to connect to. Default "irc.freenode.net"
          -u [USERNAME], --username [USERNAME]
            IRC user name. Default "otp22logbot"
