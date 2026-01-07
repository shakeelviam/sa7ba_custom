#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="sa7ba_custom",
    version="1.0.0",
    description="SA7BA Custom App - Guest Checkout & Area-Based Delivery Charges",
    author="SA7BA Development Team",
    author_email="dev@sa7ba.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[],
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
