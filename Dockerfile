FROM library/python:alpine
ADD . /app
ENTRYPOINT ["python", "/app/unity_nunit_printer.py"] 