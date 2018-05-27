#!/usr/bin/env python
from distutils.core import setup


setup(
    name='django-inventor',
    version='0.1.0',
    description='Directory listing Django app',
    long_description=open('README.md').read(),
    author='Pragmatic Mates',
    author_email='info@pragmaticmates.com',
    maintainer='Pragmatic Mates',
    maintainer_email='info@pragmaticmates.com',
    url='https://github.com/PragmaticMates/django-inventor',
    packages=[
        'inventor',
        #'inventor.templatetags'
    ],
    include_package_data=True,
    # install_requires=('django-filter', 'django', 'python-pragmatic', 'django-pragmatic'),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Development Status :: 3 - Alpha'
    ],
    license='GNU General Public License (GPL)',
    keywords="django directory listing catalog map",
)
