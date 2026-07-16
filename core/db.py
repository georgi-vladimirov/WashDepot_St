import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


@st.cache_resource
def get_database_url() -> str:
    c = st.secrets["connections"]["postgresql"]
    return (
        f"{c['dialect']}+{c['driver']}://"
        f"{c['username']}:{c['password']}@{c['host']}:{c['port']}/{c['database']}"
    )

engine = create_engine(get_database_url(), pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False)

class Base(DeclarativeBase):
    pass

def get_session():
    return SessionLocal()
