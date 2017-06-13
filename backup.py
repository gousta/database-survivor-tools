#!/usr/bin/env python
import os
import time
import json
import sys

TMP = 'tmp';
scriptPath = os.path.dirname(os.path.realpath(__file__))
tmpPath = "%s/%s" % (scriptPath, TMP)
config = json.load(open("%s/config.json" % (scriptPath)))

datetime = time.strftime('%Y%m%d%H%M')

# CLEAN TMP DIRECTORY
os.popen("rm -f %s/*" % (tmpPath))

# EXPORT TO FILE
if config["db"]["type"] == "postgres":
    filename = "%s.%s.%s.dump" % (config["db"]["database"], config["db"]["schema"], datetime)
    pwd = 'PGPASSWORD="%s"' % config["db"]["password"]
    os.popen("%s pg_dump -Fc -x -h %s -U %s -n %s -v %s -f %s/%s" % (pwd, config["db"]["host"], config["db"]["user"], config["db"]["schema"], config["db"]["database"], tmpPath, filename))
elif config["db"]["type"] == "mysql":
    filename = "%s.%s.sql" % (config["db"]["database"], datetime)
    os.popen("mysqldump --host=%s --user=%s --password=\"%s\" %s > %s/%s" % (config["db"]["host"], config["db"]["user"], config["db"]["password"], config["db"]["database"], tmpPath, filename))
else:
    print("Configuration database type is not supported. Supported values are `postgres` and `mysql`")
    sys.exit()


print("Exported latest database dump in: %s/%s" % (TMP, filename))

# CREATE DESTINATION PATH
print("Organizing destination")
os.popen("ssh -oStrictHostKeyChecking=no -oCheckHostIP=no %s mkdir -p %s" % (config["backup"]["ssh"], config["backup"]["destination"]))

# MOVE/UPLOAD FILE TO DESTINATION PATH
os.popen("scp %s/%s %s:%s/%s" % (tmpPath, filename, config["backup"]["ssh"], config["backup"]["destination"], filename))
print("Saved backup in: %s/%s" % (config["backup"]["destination"], filename))

# CLEAN BACKUPS OLDER THAN MAX (HISTORY)
os.popen("ssh -oStrictHostKeyChecking=no -oCheckHostIP=no %s \"cd %s; ls -tp | grep -v '/$' | tail -n +%d | xargs -I {} rm -- {}\"" % (config["backup"]["ssh"], config["backup"]["destination"], config["backup"]["max"] + 1))

print("Backup complete!")