#!/usr/bin/expect -f
# ------------------------------------------------------------------------------
# Author: Stratos Giouldasis <giouldasis.stratos@gmail.com>
#
# Made with ❤ in Athens, Greece
#
# Script does:
# 1. Export Database to file
# 2. Secure copy file to remote server
# 3. Scan backups directory and remove backups > max allowed
#
# Configuration: Make sure {config}.tcl exists and is configured.
# Defaults can be found in configuration/config.example.tcl
# ------------------------------------------------------------------------------
set SCRIPTPATH [ dict get [ info frame 0 ] file ]
set PROJECTPATH [file dirname $SCRIPTPATH]

source $PROJECTPATH/lib/init.tcl

# ------------------------------------------------------------------------------
# RUN PG_DUMP AND SAVE TO $FILE
# ------------------------------------------------------------------------------
set MSG "\nExporting to file..."
puts "[clr 6 $MSG]"

# spawn $PGPWD pg_dump -Fc -x -h $PGHOST -U $PGUSER -n $PGSCHEMA -v $PGDBNAME -f $TMPPATH/$FILE
# if {$PGPASSWORD != ""} {
#   expect {
#     -re ".*es.*o.*" {
#       exp_send "yes\r"..,.
#       exp_continue
#     }
#     -re ".*sword.*" {
#       exp_send "$PGPASSWORD\r"
#     }
#   }
# }
# interact

# interact 

# ------------------------------------------------------------------------------
# MOVE FILE TO SERVER USING SCP
# ------------------------------------------------------------------------------

set MSG "\nBacking up to remote server..."
puts "[clr 6 $MSG]"

eval exec ssh -oStrictHostKeyChecking=no -oCheckHostIP=no $SERVERSSH "mkdir -p $DESTINATION"
interact
eval exec scp "$TMPPATH/$FILE" "$SERVERSSH:$DESTINATION/$FILE"
interact

