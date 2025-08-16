from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="srilanka_lottery",
    version="0.1.2",
    author="Ishan Oshada",
    author_email="ic31908@gmail.com",
    description="Scrape Sri Lanka lottery results from NLB and DLB websites with this Python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ishanoshada/srilanka-lottery",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "beautifulsoup4>=4.11.0",
    ],
    keywords=[
        "lottery",
        "Sri Lanka lottery",
        "NLB",
        "DLB",
        "web scraping",
        "lottery results",
        "Python lottery scraper",
        "lottery data",
        "National Lottery Board",
        "Development Lottery Board",
        "lottery API",
        "data extraction"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ]
)