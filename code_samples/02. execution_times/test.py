import json


def main(event, context):

    if event.get('function', 'after') == 'before':
        return before()
    else:
        return after()


def before():

    return json.dumps({'function': 'before'})


def garbage_function():
    print("hello world")
    print("hello world")
    .
    .
    .
    print("hello world")

def after():
    import boto3
    import datetime
    import hashlib
    import csv
    import string
    import gzip
    import zipfile
    import tarfile
    import io
    import os
    import argparse
    import asyncio
    import ssl

    return json.dumps({'function': 'after'})