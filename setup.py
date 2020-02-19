import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="42_push-swap",
    version="1.0",
    author="Ilya Kashnitskiy",
    author_email="elijahkash.code@gmail.com",
    description="Implementation of push-swap (42-school project) on python with vizualisation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/elijahkash/42_push-swap",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
	install_requires=[
    	'pyttk>=0.1.5',
		'colour>=0.3.2'
	]
)
