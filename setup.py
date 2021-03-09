import os

def run_setup():
    # fixes warning https://github.com/pypa/setuptools/issues/2230
    from setuptools import setup, find_packages

    setup(
        name="slack_tasks_notifications",
        maintainer="Piotr Piątyszek",
        maintainer_email="piotrp@wektor.xyz",
        author="Piotr Piątyszek",
        author_email="piotrp@wektor.xyz",
        version='0.1.0',
        install_requires=[
            'setuptools',
            'slack-webhook'
        ],
        packages=find_packages(include=["slack_tasks_notifications"]),
        python_requires='>=3.6',
        include_package_data=True
    )

if __name__ == "__main__":
    run_setup()
