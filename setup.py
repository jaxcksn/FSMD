import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FSMD",
    version="1.0.2",
    author="Jaxcksn",
    author_email="admin@texansim.com",
    description="A CLI tool for creating an FSM diagram.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPLv3",
    url="https://github.com/jaxcksn/FSMD",
    entry_points={"console_scripts": ["FSMD=FSMD:run"]},
    project_urls={
        "Bug Tracker": "https://github.com/jaxcksn/FSMD/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    install_requires=[
        "graphviz ==0.20.1",
        "PyYAML ==6.0.1",
        "Requests ==2.31.0",
        "rich ==13.5.3",
        "typer ==0.9.0",
        "typing_extensions ==4.8.0",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">3.7",
)
