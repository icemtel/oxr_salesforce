from setuptools import setup, find_packages

# Read dependencies from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="oxr_salesforce",
    packages=find_packages(),
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    install_requires=requirements
)
