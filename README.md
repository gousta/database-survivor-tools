# database-survivor-tools
Tools that automate your remote backup &amp; restoration of PostgreSQL/MySQL databases.

# dump the database in custom-format archive
```pg_dump -Fc mydb > db.dump```

# restore the database
```pg_restore -d newdb db.dump```