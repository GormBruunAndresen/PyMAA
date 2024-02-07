from setuptools import setup, find_packages

setup(name='PyMAA',
      version='0.1.8',
      description='A Python library for Modeling All Alternatives',
      url='https://github.com/LukasBNordentoft/PyMAA_LBN',
      download_url = 'https://github.com/LukasBNordentoft/PyMAA/archive/refs/tags/v0.1.8.tar.gz',
      author='Tim Pedersen',
      author_email='timtoernes@gmail.com',
      maintainer = 'Lukas B. Nordentoft',
      maintainer_email = 'lukasBnordentoft@gmail.com',
      license='MIT',
      packages=find_packages(),
      keywords = ['Modelling To Generate Alterantives',
                  'Modeling All Alternatives',
                  'Near-optimal space'],
      install_requires=['numpy>=1.22',
                        'pypsa>=0.21',
                        'matplotlib',
                        # 'gurobi>=9.5',
                        'pandas',
                        'pyyaml',
                        'chaospy>=3.3',
                        'scipy',
                        'dask>=2022.12',
                        'polytope',
                        'seaborn',
                        'dask-jobqueue>=0.8'],
      zip_safe=False)
