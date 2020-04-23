from setuptools import setup, find_packages  # type: ignore


setup(
    name='banal',
    version='1.0.0',
    description='Commons of banal micro-functions for Python.',
    long_description='',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='utilities commons functions',
    author='Friedrich Lindenberg',
    author_email='friedrich@pudo.org',
    url='http://github.com/pudo/banal',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'test']),
    namespace_packages=[],
    package_data={},
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    install_requires=[],
    tests_require=[
        'nose',
        'mypy',
        'coverage',
        'wheel'
    ],
    entry_points={}
)
