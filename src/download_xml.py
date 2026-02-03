#!/usr/bin/env python3

import requests
import os
import time

import dsn_util

filename = 'dsn.xml'

dsn_util.fetch_xml(filename)
