from fabric.api import local


def up():
    local("python manage.py runserver")

def dump():
    local("python manage.py dumpdata --format=json --indent=4 howmanymiles"
        " > howmanymiles/fixtures/initial_data.json")
