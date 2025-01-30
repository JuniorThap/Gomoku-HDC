from setuptools import setup, find_packages

setup(
    name="GomokuHD",  # Package name
    version="0.1.0",  # Initial release version
    author="Thapanawat Suriyaroj",
    author_email="Thapanawatsuriyaroj@gmail.com",  # Replace with your email
    description="A deep learning-based Gomoku AI using hyperdimensional computing",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/JuniorThap/Gomoku-HDC",  # Replace with your repository
    license="Apache License 2.0",
    packages=find_packages(where="src"),  # Detect packages in 'src' directory
    package_dir={"": "src"},  # Define package location
    install_requires=[
        "torch==2.5.1+cu124",
        "torch-hd==5.7.1",
        "torchaudio==2.5.1+cu124",
        "torchvision==0.20.1+cu124"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
