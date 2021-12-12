from setuptools import setup, find_packages

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name = 'bpz-udict',
    version = '0.0.1',
    author = 'Brian Zohorsky',
    author_email = 'brianpzohorsky@gmail.com',
    license = 'MIT License',
    description = 'Fetches information from https://www.urbandictionary.com/',
    url = 'git@gitlab.com:bzohorsky/coding-projects/web-scraping/udict.git',
    py_modules = ['udict'],
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3.8',
    classifiers=[
        'Programing Language :: Python :: 3.8',
        'Operating System :: OS Indepenent',
    ],
    entry_points = {
        "console_scripts":[
            "udict = src.__main__:main"
        ]
    },
)
