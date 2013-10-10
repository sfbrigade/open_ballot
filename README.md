open_ballot
===========

An educational tool around ballot measures

Requirements:
django==1.5.1
django-extensions==1.1.1
psycopg2==2.5.1
south==0.8.1

This should eventually make its way into a pip freeze file, but this should do for now.  Let me know/add to the above if I overlooked any packages - I had most installed already.

Postgres settings, for now, should be username/password as postgres/postgres (at the database level, not unix password)

Once you have postgresql 9.2 installed (good luck), run the following:

On a Mac, the easiest way to install Postgres is using Postgres.app from http://postgresapp.com/.

./manage.py syncdb
./manage.py migrate open_ballot

To generate schemas:
	install graphviz, libgraphviz-dev (apt-get for ubuntu, mac users, sorry)
	pip install pygraphviz
	./manage.py graph_models open_ballot -o schema.png
