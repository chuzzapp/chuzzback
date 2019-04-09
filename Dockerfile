
FROM skygeario/py-skygear:v1.5.0

COPY requirements.txt /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app
