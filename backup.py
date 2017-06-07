#!/usr/bin/env python
import os
import time
import json

TMP = 'tmp';

scriptPath = os.path.dirname(os.path.realpath(__file__))
tmpPath = "%s/%s" % (scriptPath, TMP)
config = json.load(open("%s/config.json" % (scriptPath)))

datetime = time.strftime('%Y%m%d%H%M')
filename = "%s.%s.%s.dump" % (config["pg"]["database"], config["pg"]["schema"], datetime)

# CLEAN TMP DIRECTORY
os.popen("rm -f %s/*.dump" % (tmpPath))
print("Cleaned tmp directory")

# EXPORT TO FILE
os.popen("pg_dump -Fc -x -h %s -U %s -n %s -v %s -f %s/%s" % (config["pg"]["host"], config["pg"]["user"], config["pg"]["schema"], config["pg"]["database"], tmpPath, filename))
print("Exported latest database dump in: %s/%s" % (TMP, filename))

# CREATE DESTINATION PATH
print("Organizing destination")
os.popen("ssh -oStrictHostKeyChecking=no -oCheckHostIP=no %s mkdir -p %s" % (config["backup"]["ssh"], config["backup"]["destination"]))

# MOVE/UPLOAD FILE TO DESTINATION PATH
print("Pushing to: %s" % (config["backup"]["destination"]))
os.popen("scp %s/%s %s:%s/%s" % (tmpPath, filename, config["backup"]["ssh"], config["backup"]["destination"], filename))
print("Saved backup in: %s/%s" % (config["backup"]["destination"], filename))

# CREATE DESTINATION PATH
os.popen("ssh -oStrictHostKeyChecking=no -oCheckHostIP=no %s \"cd %s; ls -tp | grep -v '/$' | tail -n +%d | xargs -I {} rm -- {}\"" % (config["backup"]["ssh"], config["backup"]["destination"], config["backup"]["history"] + 1))
print("Performed cleanup")

print("Backup complete!")