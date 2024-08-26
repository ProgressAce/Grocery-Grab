# Application's entry point
from app import create_app
from os import environ


ENV = environ.get('ENV')
app = create_app(ENV)

if __name__ == '__main__':
    app.run()
