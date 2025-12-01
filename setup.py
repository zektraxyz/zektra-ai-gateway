"""Setup script for zektra-ai-gateway"""

from setuptools import setup, find_packages

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="zektra-ai-gateway",
    version="0.1.0",
    author="Zektra Team",
    description="AI Gateway with Crypto Payments - Connect to AI services using $ZEKTRA tokens",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zektraxyz/zektra-ai-gateway",
    packages=find_packages(exclude=["tests", "examples"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.31.0",
        "web3>=6.11.0",
        "eth-account>=0.9.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
        "typing-extensions>=4.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.11.0",
            "ruff>=0.1.6",
            "mypy>=1.7.0",
            "ipython>=8.17.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "zektra=zektra.cli:main",
        ],
    },
)

