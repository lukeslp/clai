from setuptools import setup, find_packages

setup(
    name="clai",
    version="0.1.0",
    description="A natural-language to shell/Python CLI assistant using local Ollama models.",
    author="Luke Steuber",
    author_email="luke@actuallyusefulai.com",
    url="https://actuallyusefulai.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "colorama",
        "rich",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "clai=clai.clai:main",
        ],
    },
    python_requires=">=3.7",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 