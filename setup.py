from setuptools import setup  # type: ignore

with open("README.md") as f:
    long_description = f.read()


setup(
    name="banal",
    version="1.0.5",
    description="Commons of banal micro-functions for Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="utilities commons functions",
    author="Friedrich Lindenberg",
    author_email="friedrich@pudo.org",
    url="http://github.com/pudo/banal",
    license="MIT",
    namespace_packages=[],
    package_data={"banal": ["py.typed"]},
    packages=["banal"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    extras_require={
        "dev": [
            "mypy",
            "wheel",
        ]
    },
)
