#!/usr/bin/env python
import os
import json
import subprocess

TMP = 'tmp';
scriptPath = os.path.dirname(os.path.realpath(__file__))
tmpPath = "%s/%s" % (scriptPath, TMP)
config = json.load(open("%s/config.json" % (scriptPath)))

# CLEAN TMP DIRECTORY
os.popen("rm -f %s/*" % (tmpPath))

filename = os.popen("ssh -oStrictHostKeyChecking=no -oCheckHostIP=no %s \"ls %s | sort -V | tail -n 1\"" % (config["backup"]["ssh"], config["backup"]["destination"])).read()
filename = filename.strip()

print("Downloading backup file: %s/%s" % (config["backup"]["destination"], filename))

if filename:
    os.popen("scp %s:%s/%s %s/%s" % (config["backup"]["ssh"], config["backup"]["destination"], filename, tmpPath, filename))
    print("Downloaded")


print("Restoring from backup")

if config["db"]["type"] == "postgres":
    pwd = 'PGPASSWORD="%s"' % config["db"]["password"]
    os.popen("%s pg_restore -c --schema=%s -h %s -U %s -d %s %s/%s" % (pwd, config["db"]["schema"], config["db"]["host"], config["db"]["user"], config["db"]["database"], tmpPath, filename))
elif config["db"]["type"] == "mysql":
    os.popen("mysqldump --opt --protocol=TCP --host=%s --user=%s --password=%s %s > %s/%s" % (config["db"]["host"], config["db"]["user"], config["db"]["password"], config["db"]["database"], tmpPath, filename))
else:
    print("Configuration database type is not supported. Supported values are `postgres` and `mysql`")
    sys.exit()

print("Restore complete!")

