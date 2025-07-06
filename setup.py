"""
Setup script for Spotify Analysis Sleep Apnea Project.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="spotify-analysis-sleep-apnea",
    version="1.0.0",
    author="Spotify Analysis Team",
    author_email="your-email@example.com",
    description="Advanced music listening pattern analysis for sleep apnea research",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/spotify-analysis-sleep-apnea",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "isort>=5.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "spotify-analysis=spotify_analysis.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="spotify, music, analysis, sleep, data-science, streaming",
    project_urls={
        "Bug Reports": "https://github.com/your-username/spotify-analysis-sleep-apnea/issues",
        "Source": "https://github.com/your-username/spotify-analysis-sleep-apnea",
        "Documentation": "https://github.com/your-username/spotify-analysis-sleep-apnea#readme",
    },
) 