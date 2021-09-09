import setuptools

setuptools.setup(
    name="confTester",
    version="0.1",
    author="Georg Alberding",
    author_email="galberding@uni-bielefeld.de",
    description="Package for extracting compile parameters from c source code in order to search for conditional compilation.",
    # long_description="The following major components are planned: Module Search, Configuration Builde, Automatic Tester, Visualizer (Results), CLI",
    # long_description_content_type="text/markdown",
    install_requires=[
        'PyYAML',
        'tqdm',
        'overrides',
        'pandas'
    ],
    # requires="https://github.com/pypa/sampleproject",
    # project_urls={
        # "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    # },
    classifiers=[
        "Programming Language :: Python :: 3.9",
        # "License :: OSI Approved :: MIT License",
        # "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(exclude=("test*", "sim*", "doc*", "examples*")),
    # python_requires=">=3.7",
    package_dir={"": "src"},
    include_package_data=True,
    extras_require=dict(
        test=['testfixtures'],
    ),
    test_suite="tests"
)
