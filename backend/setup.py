from setuptools import setup, find_packages

setup(
    name="orchestralink",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "python-dotenv",
        "sqlalchemy",
        "Flask",
        "psycopg2-binary",
        "paho-mqtt",
        "numpy"
    ],
    description="Smart Manufacturing AI Platform.",
    author="Radek",
    author_email="Silethalo@lol.com",
)
