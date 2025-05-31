from setuptools import setup, find_packages

setup(
    name="finance-telegram-api",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "python-telegram-bot",
        "google-auth-oauthlib",
        "google-auth-httplib2",
        "google-api-python-client",
        "python-dotenv"
    ],
) 