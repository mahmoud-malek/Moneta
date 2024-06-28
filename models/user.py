#!/usr/bin/python3

""" this is a uesr module that defines a uesr class """

from models import base
import models


class User(BaseModel):
    """ the uesr class """

    def __init__(self, *args, **kwargs):
        """ constractor method to initialize the user object """
        super().__init__(args, kwargs)
