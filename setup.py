"""Setup configuration for graphml-to-falkordb package."""

from setuptools import setup, find_packages

setup(
    name="graphml-to-falkordb",
    version="0.1.0",
    description="Migrate GraphML files to FalkorDB",
    author="Your Name",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "networkx>=2.6",
        "falkordb>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "graphml-to-falkordb=graphml_to_falkordb.cli:main",
        ],
    },
)
