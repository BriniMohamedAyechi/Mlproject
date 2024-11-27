from setuptools import find_packages,setup
from typing import List

const="-e ."

def get_requirements(file_path:str)->List[str]:
    """
    Retunrs the list of requirements
    """
    requirements=[]
    with open (file_path) as file_obj:
        requirements=file_obj.readlines()
        [req.replace ("\n","")for req in requirements]

        if const in requirements:
            requirements.remove(const)
    return requirements

setup(
    name="MLproject",
    version="0.0.1",
    author="Brini",
    author_email="brini.mohamedayechi@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt")




)
