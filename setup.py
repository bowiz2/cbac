from setuptools import setup

setup(name='cbac',
      version='0.1',
      description='Command Block Array Circuit Synthesiser',
      url='http://github.com/Nicodemes/cbac',
      author='Nicodemes Decho',
      author_email='sasha@paticon.com',
      license='MIT',
      packages=['cbac', 'cbac.core', 'cbac.core.blockspace', 'cbac.core.command_shell', 'cbac.core.compound',
                'cbac.core.mcentity', 'cbac.mctest', 'cbac.resources', 'cbac.resources.schematics', 'cbac.schematics',
                'cbac.std_logic', 'cbac.std_unit', 'cbac.unit'],
      zip_safe=False,
      package_data={'': ['*.schematic']})
