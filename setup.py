from setuptools import setup  # type: ignore

def readme():
      with open('README.md') as f:
            return f.read()

def read_version():
      with open('dup/VERSION') as f:
            version_data = f.read().splitlines()
            return version_data[0]

setup(name='dup',
      version=read_version(),
      description='Detect (and delete) duplicate files',
      long_description=readme(),
      packages=['dup'],
      entry_points = {
            'console_scripts': ['dup=dup.command_line:main'],
      },
      classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Programming Language :: Python :: 3',
      ],
      url='https://github.com/PJSoftware/detect-duplicates',
      author='Peter Jones',
      author_email='pjsoftware@petesplace.id.au',
      include_package_data=True,
      zip_safe=False)
