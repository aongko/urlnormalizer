from setuptools import setup, find_packages

setup(
	name='urlnormalizer',
	version='0.2.0',
	url='http://github.com/kafji/urlnormalizer',
	license="MIT License",
	author='Kafji',
	author_email='kafjiam@gmail.com',
	packages=find_packages(exclude=['tests*']),
	classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
	],
)
