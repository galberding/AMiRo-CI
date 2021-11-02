import setuptools


test_deps = [
    'pytest',
    'flake8',
    'pylint',
    'mypy',
]

extras = {
    'test': test_deps
}


setuptools.setup(
    name='AMiRo-CI',
    version='0.1',
    author='Georg Alberding',
    author_email='',
    description=
    'Package utilizing conditional compilation to test the AMiRo-OS and AMiRo-Apps project.',
    install_requires=['PyYAML', 'tqdm', 'overrides', 'pandas'],
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)'
    ],
    scripts=['src/amiroci/amiroCI'],
    python_requires=">=3.9",
    package_dir={"": "src"},
    packages=[
        'amiroci',
        'amiroci.tools',
        'amiroci.tools.config',
        'amiroci.tools.search',
        'amiroci.tools.search.search_result',
        'amiroci.model',
        'amiroci.model.argument',
        'amiroci.model.option',
        'amiroci.controller',
    ],
    tests_require=test_deps,
    extras_require=extras,
)
