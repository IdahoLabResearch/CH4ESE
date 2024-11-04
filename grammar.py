""""
CH4ESE - Conversion Helper 4 Easy Serialization of EXI
Copyright 2024, Battelle Energy Alliance, LLC
"""

from os.path import abspath, isfile
import sys
import log


def create_grammar(factory, schema_profile: dict):
    """Creates the grammars utilizing the user-defined profile and the grammar factory"""
    paths = []
    folder = schema_profile["Folder"]
    for file in schema_profile["Files"]:
        paths.append(abspath(f"{folder}/{file}"))
    for path in paths:
        if isfile(path):
            try:
                schema_profile["Files"][path.split("/")[-1]]["Grammar"] = factory.createGrammars(path)
                log.logger.info(f"Grammar created from: {path}")
            except:
                log.logger.error(f"Grammar cannot be created from provided schema file: {path}")
        else:
            log.logger.error(f"Invalid File Path: {path}")
            sys.exit(f"Bad Profile: Ensure the relative path is correct -> 'folder': {schema_profile['Folder']}")

    return schema_profile
