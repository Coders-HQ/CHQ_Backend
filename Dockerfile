FROM python:3
ENV PYTHONUNBUFFERED 1

# sets the working dir
WORKDIR /app/backend

ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    PIPENV_HIDE_EMOJIS=1

# copies the requirement.txt to workdir root and installs
COPY requirements.txt ./
RUN pip install -r requirements.txt


# copy everything in backend root into docker image
COPY . ./

# RUN python manage.py makemigrations users
# RUN python manage.py migrate 
