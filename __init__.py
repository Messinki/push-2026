from __future__ import absolute_import, print_function, unicode_literals
import Live
from .PushEmpty import PushEmpty

def create_instance(c_instance):
    u""" Creates and returns the PushEmpty script """
    return PushEmpty(c_instance)

