#!/bin/bash
pip3 install -r requirements.txt
uvicorn mainapp.main:app --reload
