import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="distend_hanzuo",
    version="1.0.0",
    author="Hanwen Zuo",
    author_email="HanwenZuo1@gmail.com",
    description="Distend - targeted word list generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/not_sponsored/distend",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'': ['rules.conf']},
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["distend=distend.cli:main"]},
)
