import setuptools


def parse_requirements(filename):
    """Load requirements from a pip requirements file."""
    with open(filename) as f:
        reqs = (req.strip() for req in f.readlines() if req and not req.startswith("#"))
    return list(reqs)


install_requires = parse_requirements("requirements.txt")

setuptools.setup(
    name="bbva_assignment",
    version="0.1",
    author="Lorenzo Gorini",
    author_email="lorenzo.gorini.22@ucl.ac.uk",
    description="Assignment for Research Assistant Position",
    url="https://github.com/lorenz-gorini/bbva_assignment",
    license="MIT",
    install_requires=install_requires,
    packages=["bbva_assignment"],
    zip_safe=False,
)
