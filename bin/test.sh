#!/bin/sh

nosetests --with-coverage --cover-erase --cover-html --cover-html-dir=cover --cover-package=app $1 $2


