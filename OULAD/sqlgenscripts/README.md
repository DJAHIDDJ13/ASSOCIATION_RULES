Generate the sql scripts

`
python gensql.py
`

Execute the sql scripts

`
psql -h <host:port> -U <username> -P <password> -d <database_name> -a -f CREATE_TABLES.sql
psql -h <host:port> -U <username> -P <password> -d <database_name> -a -f INSERT_DATA_students.sql
psql -h <host:port> -U <username> -P <password> -d <database_name> -a -f INSERT_DATA_courses.sql
psql -h <host:port> -U <username> -P <password> -d <database_name> -a -f INSERT_DATA_assessments.sql
psql -h <host:port> -U <username> -P <password> -d <database_name> -a -f INSERT_DATA_vle.sql
psql -h <host:port> -U <username> -P <password> -d <database_name> -a -f INSERT_DATA_studentInfo.sql
psql -h <host:port> -U <username> -P <password> -d <database_name> -a -f INSERT_DATA_studentAssessment.sql
psql -h <host:port> -U <username> -P <password> -d <database_name> -a -f INSERT_DATA_studentRegistration.sql
psql -h <host:port> -U <username> -P <password> -d <database_name> -a -f INSERT_DATA_studentVle.sql
psql -h <host:port> -U <username> -P <password> -d <database_name> -a -f INSERT_DATA_studentVle_1.sql
psql -h <host:port> -U <username> -P <password> -d <database_name> -a -f INSERT_DATA_studentVle_2.sql
psql -h <host:port> -U <username> -P <password> -d <database_name> -a -f INSERT_DATA_studentVle_3.sql
psql -h <host:port> -U <username> -P <password> -d <database_name> -a -f INSERT_DATA_studentVle_4.sql
psql -h <host:port> -U <username> -P <password> -d <database_name> -a -f INSERT_DATA_studentVle_5.sql
psql -h <host:port> -U <username> -P <password> -d <database_name> -a -f INSERT_DATA_studentVle_6.sql
psql -h <host:port> -U <username> -P <password> -d <database_name> -a -f INSERT_DATA_studentVle_7.sql
psql -h <host:port> -U <username> -P <password> -d <database_name> -a -f INSERT_DATA_studentVle_8.sql
psql -h <host:port> -U <username> -P <password> -d <database_name> -a -f INSERT_DATA_studentVle_9.sql
psql -h <host:port> -U <username> -P <password> -d <database_name> -a -f INSERT_DATA_studentVle_10.sql
`

Remove the relations (and the data)

`
psql -h <host:port> -U <username> -P <password> -d <database_name> -a -f DROP_TABLES.sql
`

Generate the database diagrams

`
java -jar ../../schemaspy-6.0.0.jar -t pgsql -db oulad -host <host ip> -u <username> -p <password> -o ./schemaspy -dp ../../postgresql-42.2.5.jar -s public -noads
`

To view the generated diagrams open the index.html in ./schemaspy with a web browser (e.g. firefox schemaspy/index.html)

