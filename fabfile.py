from fabric.api import local


def up():
    local("python manage.py runserver")

def load():
    local("python manage.py loaddata mileage_data.json")

def dump():
    local("python manage.py dumpdata --format=json --indent=4 howmanymiles"
        " > howmanymiles/fixtures/mileage_data.json")

def test():
    local("python manage.py test howmanymiles")

def sync():
    local("python manage.py syncdb")

def add():
    local("python manage.py add_mileage_multiplier")

def db():
    local("python manage.py syncdb")

def sh():
    local("python manage.py shell")
