import setuptools

setuptools.setup(
    name="confTester",
    version="0.1",
    author="Georg Alberding",
    author_email="galberding@uni-bielefeld.de",
    description=
    "Package utilizing conditional compilation to test the AMiRo-OS and AMiRo-Apps project.",
    install_requires=['PyYAML', 'tqdm', 'overrides', 'pandas'],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        # "License :: OSI Approved :: MIT License",
        # "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(
        exclude=("test*", "sim*", "doc*", "examples*")
    ),
    # python_requires=">=3.7",
    package_dir={"": "src"},
    include_package_data=True,
    extras_require=dict(test=['testfixtures'], ),
    test_suite="tests"
)
