Generate the sql scripts
`
python gensql.py
`

Execute the sql scripts
`
psql -h <host:port> -U <username> -P <password> -d <database_name> -a -f CREATE_TABLES.sql
psql -h <host:port> -U <username> -P <password> -d <database_name> -a -f INSERT_TABLES.sql
`

Remove the relations (and the data)
`
psql -h <host:port> -U <username> -P <password> -d <database_name> -a -f DROP_TABLES.sql
`

Generate the database diagrams
`
java -jar schemaspy-6.0.0.jar -t pgsql -db epm -host localhost -u postgres -p '123456' -o ./schemaspy -dp postgresql-42.2.5.jar -s public -noads
`

To view the generated diagrams open the index.html in ./schemaspy with a web browser (e.g. firefox schemaspy/index.html)
