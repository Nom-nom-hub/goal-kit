from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="goal-dev-spec",
    version="0.1.0",
    author="Goal-Dev-Spec Team",
    author_email="example@example.com",
    description="A goal-driven development specification system using YAML",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/goal-dev-spec",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.10",
    install_requires=[
        "typer>=0.9.0",
        "rich>=13.0.0",
        "pyyaml>=6.0",
        "jsonschema>=4.17.3",
        "platformdirs>=3.5.0",
    ],
    entry_points={
        "console_scripts": [
            "goal=goal_cli:main",
        ],
    },
)