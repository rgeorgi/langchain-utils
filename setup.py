from setuptools import setup

setup(
    name='Lanchain Utils',
    packages=['langchain_utils'],
    install_requires=[
        'langchain',
        'chromadb'
    ],
    version='0.1'
)