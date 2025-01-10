release: python3 manage.py migrate && python3 manage.py collectstatic --no-input
web: gunicorn threat_detection_project.wsgi --timeout 60 --log-file -

