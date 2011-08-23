#!/usr/bin/env python

from distutils.core import setup

setup( name = "nanotest",
       version = "1.1.1",
       description = "Tiny testing toolkit (for Python)",
       author = "Shawn Boyette",
       author_email = "shawn@firepear.net",
       url = "https://github.com/firepear/nanotest-py",
       py_modules=["nanotest"],
       scripts=['bin/nanotest'] )
