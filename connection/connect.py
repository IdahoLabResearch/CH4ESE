
""""
CH4ESE - Conversion Helper 4 Easy Serialization of EXI
Copyright 2024, Battelle Energy Alliance, LLC
"""

from os.path import abspath, dirname
import sys
from py4j.java_gateway import JavaGateway
import log


def create_gateway():
    """Creates the Py4J Gateway and establishes the grammar factory to test the connection"""
    path = dirname(abspath(__file__))
    try:
        file_path = path + "/EXIficient.jar"
        gateway = JavaGateway.launch_gateway(classpath=file_path)
        grammar_factory = gateway.jvm.com.siemens.ct.exi.grammars.GrammarFactory.newInstance()
        log.logger.info("JVM Connected and Grammar Factory connected.")
        return gateway, grammar_factory
    except:
        log.logger.critical("Failed to connect to JVM.")
        sys.exit("Py4J Failure")
