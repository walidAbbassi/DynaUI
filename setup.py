from setuptools import setup

setup(
    name="DynaUI",
    version="1.1.4",
    description="A framework to increase the scalability and flexibility of wxPython",
    url="https://github.com/yadizhou/DynaUI",
    author="Yadi Zhou",
    author_email="yadizhou90@gmail.com",
    license="GPL-3.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications :: GTK",
        "Environment :: MacOS X :: Cocoa",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: User Interfaces",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="GUI UI wxPython user-interface",
    packages=["DynaUI", "DynaUI.controls", "DynaUI.demo"],
    package_data={
        "DynaUI.demo": ["*.png", "*.jpg"],
    },
    install_requires=["wxpython"],
    zip_safe=False,
)
