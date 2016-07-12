from setuptools import setup


setup(
    name='drone-marathon',
    version='0.2',
    description="Mesos Marathon plugin for Drone.",
    url="https://github.com/expansioncap/drone-marathon",
    maintainer="Drone Contributors",
    maintainer_email="support@drone.io",
    packages=["drone_marathon"],
    scripts=["bin/drone-marathon"],
    install_requires=[],
)
