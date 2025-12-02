import streamlit as st
import time
from pymongo import MongoClient
import os

MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)

# Banco para currículos
db_curriculos = client["curriculos"]
curriculos = db_curriculos["curriculos"]

# Banco para vagas
db_vagas = client["vagas"]
vagas = db_vagas["vagas"]