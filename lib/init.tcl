# ------------------------------------------------------------------------------
# FUNCTIONS
# ------------------------------------------------------------------------------

proc clr {foreground text} {
  return [exec tput setaf $foreground]$text[exec tput sgr0]
}

# ------------------------------------------------------------------------------
# LOAD CONFIGURATION FILE
# ------------------------------------------------------------------------------
set CONFIGFILENAME $argv
set CONFIGPATH "$PROJECTPATH/configuration/$CONFIGFILENAME.conf.tcl"

if {$CONFIGFILENAME == ""} {
  set MSG "Configuration parameter is missing.\nCorrect usage: ./command {config}"
  puts "[clr 1 $MSG]"
  exit 0
}

if {[file exists $CONFIGPATH] == 1} {
  set MSG "Configuration Loaded: $CONFIGPATH"
  puts "[clr 6 $MSG]"
  source $CONFIGPATH
} else {
  set MSG "Failed to read configuration file: $CONFIGPATH"
  puts "[clr 1 $MSG]"
  exit 0
}

# ------------------------------------------------------------------------------
# INITIALIZATIONS
# ------------------------------------------------------------------------------

set TMPPATH "$PROJECTPATH/tmp"
set SSHPROMPT ":|#|\\\$"
set DATETIMESTAMP [timestamp -format %d%m%Y%H%M]
set PGPWD "PGPASSWORD=\"$PGPASSWORD\""

set FILE "$CONFIGFILENAME.$PGDBNAME.$PGSCHEMA.$DATETIMESTAMP.dump"

set MSG "File: $FILE"
puts "[clr 6 $MSG]"

set MSG "Cleaning tmp folder: $TMPPATH"
puts "[clr 3 $MSG]"
exec ls -l 
# spawn rm -rf $TMPPATH/*
