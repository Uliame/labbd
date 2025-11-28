import streamlit as st
import pandas as pd
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import ObjectId

class DataManager:
    def __init__(self):
        # Inicializa a conexão pegando as credenciais dos segredos do Streamlit
        try:
            self.client = MongoClient(st.secrets["mongo"]["uri"])
            self.db_name = st.secrets["mongo"]["db_name"]
            self.db = self.client[self.db_name]
            
            # Coleções
            self.vagas = self.db.vagas
            self.curriculos = self.db.curriculos
            self.users = self.db.users
            
            # Verifica conexão (opcional, apenas para debug inicial)
            self.client.admin.command('ping')
        except Exception as e:
            st.error(f"Erro ao conectar ao MongoDB: {e}")

    def _to_df(self, cursor):
        """Helper para converter cursor do Mongo em DataFrame tratado"""
        lista_dados = list(cursor)
        if not lista_dados:
            return pd.DataFrame()
        
        df = pd.DataFrame(lista_dados)
        # Converter ObjectId para string para evitar erros no Streamlit
        if '_id' in df.columns:
            df['_id'] = df['_id'].astype(str)
        return df

    # --- VAGAS ---
    def get_vagas(self):
        """Retorna todas as vagas como DataFrame"""
        cursor = self.vagas.find()
        # Garante que as colunas essenciais existam mesmo se o banco estiver vazio
        df = self._to_df(cursor)
        if df.empty:
            return pd.DataFrame(columns=["titulo", "descricao", "cidade", "estado", "salario", "skills", "empresa", "lat", "lon"])
        return df

    def save_vaga(self, nova_vaga_dict):
        """Salva uma nova vaga no MongoDB"""
        # Adiciona timestamp ou status se necessário
        nova_vaga_dict['ativa'] = True
        self.vagas.insert_one(nova_vaga_dict)

    # --- CURRÍCULOS ---
    def get_curriculos(self):
        """Retorna todos os currículos como DataFrame"""
        cursor = self.curriculos.find()
        return self._to_df(cursor)

    def save_curriculo(self, novo_cv_dict):
        """Salva um novo currículo"""
        self.curriculos.insert_one(novo_cv_dict)
    
    # --- AUTH / USUÁRIOS ---
    def authenticate(self, username, password):
        """Verifica credenciais no banco de dados"""
        user = self.users.find_one({"username": username, "password": password})
        if user:
            # Retorna dados do usuário sem o ObjectId (convertido p/ string)
            user['_id'] = str(user['_id'])
            return user
        return None

    def create_user(self, user_dict):
        """Cria um novo usuário (se não existir)"""
        if self.users.find_one({"username": user_dict['username']}):
            return False # Usuário já existe
        self.users.insert_one(user_dict)
        return True