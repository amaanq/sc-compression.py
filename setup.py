import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sc-compression.py",
    version="0.0.2",
    author="AQ",
    license='GPLv3+',
    description="A python package for decompressing Supercell game assets.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amaanq/sc-compression.py",
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
        "Operating System :: OS Independent",
    ],
    package_dir={"": "sc_compression"},
    packages=setuptools.find_packages(where="sc_compression"),
    python_requires=">=3.6",
)
