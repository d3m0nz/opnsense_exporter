from setuptools import setup, find_packages

setup(
    name='opnsense_exporter',
    version='0.1.dev0',
    url='https://github.com/d3m0nz/opnsense_exporter',
    author='dr1s',
    license='MIT',
    description='Export opnsense metrics for prometheus',
    install_requires=["Flask"],["Requests"],
    packages=find_packages(),
    include_package_data = True,
    entry_points={'console_scripts': ['opnsense_exporter=opnsense_exporter.opnsense_exporter:main']},
)