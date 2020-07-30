import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
     name='readysignal',
     version='0.1',
     author="Jess Brown",
     author_email="jess.brown@rxa.io",
     description="The API for readysignal.com",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/rxa-io/readysignal",
     packages=setuptools.find_packages(),
     classifiers=[],
     install_requires=required,
     # [
     #     "Programming Language :: Python :: 3.6.8",
     # ],
)