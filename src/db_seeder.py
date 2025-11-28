# src/db_seeder.py
import pandas as pd
from pymongo import MongoClient
import streamlit as st

# Configuração (idealmente leia do secrets, mas para script avulso pode hardcodar ou usar input)
# ATENÇÃO: Use isso apenas para inicializar o banco
MONGO_URI = "mongodb+srv://..." # Coloque sua URI aqui temporariamente
DB_NAME = "labbd_db"

def seed_database():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    
    # 1. Popular Usuários
    if db.users.count_documents({}) == 0:
        print("Populando usuários...")
        users = [
            {"username": "admin", "password": "123", "role": "admin", "name": "Administrador"},
            {"username": "empresa", "password": "123", "role": "employer", "name": "Tech Solutions Inc."},
            {"username": "candidato", "password": "123", "role": "candidate", "name": "João Silva"}
        ]
        db.users.insert_many(users)
    
    # 2. Popular Vagas (lendo do CSV original se tiver, ou dados mockados)
    if db.vagas.count_documents({}) == 0:
        print("Populando vagas...")
        try:
            df_vagas = pd.read_csv("data/vagas.csv", sep=';')
            db.vagas.insert_many(df_vagas.to_dict('records'))
        except Exception as e:
            print(f"Não foi possível ler vagas.csv: {e}")

    # 3. Popular Currículos
    if db.curriculos.count_documents({}) == 0:
        print("Populando currículos...")
        try:
            df_cv = pd.read_csv("data/curriculos.csv", sep=';')
            db.curriculos.insert_many(df_cv.to_dict('records'))
        except Exception as e:
            print(f"Não foi possível ler curriculos.csv: {e}")
            
    print("Banco de dados inicializado com sucesso!")

if __name__ == "__main__":
    seed_database()