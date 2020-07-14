import setuptools

with open('README.md', 'r') as readme:
    long_description = readme.read()

setuptools.setup(
    name='push_swap_gui',
    version='1.1',
    author='Ilya Kashnitskiy',
    author_email='elijahkash.code@gmail.com',
    description='Implementation of push-swap (42-school project) on python with GUI.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/elijahkash/push_swap_gui',
    packages=setuptools.find_packages(),
	license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
	install_requires=[
    	'pyttk>=0.3.2',
		'colour>=0.1.5'
	],
	entry_points={
		'console_scripts': [
			'push_swap_gui = push_swap_gui.__main__:main',
		]
	},
	keywords='42 push_swap push-swap'
)
