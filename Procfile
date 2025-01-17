release: python3 manage.py makemigrations && python3 manage.py migrate
web: gunicorn threat_detection_project.wsgi --timeout 60 --log-file -

