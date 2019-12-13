from unittest import TestSuite, TextTestRunner
import hashlib

def run(test):
    suite = TestSuite()
    suite.addTest(test)
    TextTestRunner().run(suite)

def hash256(str):
    '''sha256 두 번 반복'''
    return hashlib.sha256(hashlib.sha256(str).digest()).digest()