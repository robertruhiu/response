from fabric.api import local


def prep():
    local('pip freeze > requirements-temp.txt')
    with open('requirements-temp.txt', 'r') as f:
        content = f.read()
        final_requirements = content.replace('pkg-resources==0.0.0', '')
        with open('requirements.txt', 'w+') as x:
            x.write(final_requirements)
    local('rm requirements-temp.txt')
    local('python manage.py collectstatic --no-input')


def test():
    local('python manage.py test --failfast --exclude=WIP --exclude=skip --keepdb')


def dev_migrate():
    local('heroku run python manage.py migrate --app=codeln-dev')


def prod_migrate():
    local('heroku run python manage.py migrate --app=codeln-v1')


def dev_shell():
    local('heroku run python manage.py shell --app=codeln-dev')


def prod_shell():
    local('heroku run python manage.py shell --app=codeln-v1')


def prod_logs():
    local('heroku logs -t --app=codeln-v1')


def dev_logs():
    local('heroku logs -t --app=codeln-dev')


def all():
    prep()
    merge()


def merge():
    local('git push')
    local('git checkout master')
    local('git merge dev')
    local('git push')
    local('git checkout dev')
