"""
CH4ESE - Conversion Helper 4 Easy Serialization of EXI
Copyright 2024, Battelle Energy Alliance, LLC

This module handles the conversions between EXI and XML. A majority of the functions
called here are defined in connection/EXIficient.jar and invoked via the Py4J gateway

The repository for the .jar file is included in the README.md
"""

import sys
import log


def encode_xml(message: str, profile, gateway):
    """Identifies the correct grammar and converts from EXI to XML"""
    for schema in profile["Files"].values():
        if schema["Signature"] in message:
            gram = schema["Grammar"]
            break
        elif schema["Signature"] == "default":
            gram = schema["Grammar"]
            break

    # creates an EXI Factory
    exi_factory_helper = gateway.jvm.com.siemens.ct.exi.core.helpers.DefaultEXIFactory.newInstance()
    exi_factory_helper.setGrammars(gram)
    exi_result = gateway.jvm.com.siemens.ct.exi.main.api.sax.EXIResult(exi_factory_helper)

    out_byte_stream = gateway.jvm.java.io.ByteArrayOutputStream()
    results_stream = exi_result.setOutputStream(out_byte_stream)
    xml_reader = gateway.jvm.org.xml.sax.helpers.XMLReaderFactory.createXMLReader()
    xml_reader.setContentHandler(exi_result.getHandler())

    try:
        # converts the XML to an EXI message
        read_string = gateway.jvm.java.io.StringReader(message)
        input_stream = gateway.jvm.org.xml.sax.InputSource(read_string)
        xml_reader.parse(input_stream)

        result_bytes = out_byte_stream.toByteArray()
        result_final = result_bytes.hex()
        return result_final
    except:
        log.logger.error("Provided profile is not compatible with the provided XML.")
        sys.exit()


def decode_exi(message, profile, gateway):
    """Brute force decodes the message with the profile's schemas"""
    for schema in profile["Files"]:
        result = decoder(message, profile["Files"][schema]["Grammar"], gateway)
        if result != -1:
            return result
    log.logger.error("No schemas in the provided profile are compatible with the EXI message.")
    sys.exit()


def decoder(message: bytearray, grammar, gateway):
    """Attempts to decode the message with the provided grammar"""
    # creates EXI Factory and provides it with the custom grammar
    exi_factory_helper = gateway.jvm.com.siemens.ct.exi.core.helpers.DefaultEXIFactory.newInstance()
    exi_factory_helper.setGrammars(grammar)
    exi_source = gateway.jvm.com.siemens.ct.exi.main.api.sax.EXISource(exi_factory_helper)

    byte_stream = gateway.jvm.java.io.ByteArrayInputStream(message)
    exi_source.setInputSource(gateway.jvm.org.xml.sax.InputSource(byte_stream))
    out_byte_stream = gateway.jvm.java.io.ByteArrayOutputStream()
    results_stream = gateway.jvm.javax.xml.transform.stream.StreamResult(out_byte_stream)

    # creates a transformer factory, this will be used to transform the EXI into XML
    transform = gateway.jvm.javax.xml.transform.TransformerFactory.newInstance()
    transformer = transform.newTransformer()

    try:
        # decodes the EXI message into XML format
        transformer.transform(exi_source, results_stream)
        final_result = out_byte_stream.toByteArray()

        return final_result.decode("utf-8")
    except:
        return -1
