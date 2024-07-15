#!/usr/bin/python3

""" this is the wsgi entry point for the application """

from web.app import app as application

if __name__ == '__main__':
    application.run()
