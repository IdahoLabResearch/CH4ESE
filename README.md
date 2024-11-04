# Conversion Helper 4 Easy Serialization of EXI
## What is CH4ESE
CH4ESE is an EXI conversion tool developed in Python3 that utilizes the open-source
[EXIficient](https://github.com/EXIficient/exificient) implementation of the W3C EXI
format specification. CH4ESE can be used to translate to and from EXI format using the
command line with input data or using the web server for live translation.
CH4ESE was inspired by [V2Gdecoder](https://github.com/FlUxIuS/V2Gdecoder).


### Features:
- [ ] Encoding XML into EXI Messages
- [ ] Decoding EXI Messages into XML
- [ ] Schema-Informed Grammar Creation
- [ ] Multithreaded local web server for handling large sets of data
- [ ] Multi-Schema Conversation Support through Custom Profiles
- [ ] Data Handling and Storage

## Installing Dependencies
- [ ] pip install -r requirements.txt

## How To Use
```
usage: python3 main.py [-h] [-i <Path to input file> | -s <EXI/XML string>] [-o <Output file>] (-e | -d | -w) -profile <Profile Name> [-p port_number] [-v]

This tool is used to perform EXI conversions

options:
  -h, --help            show this help message and exit

Input Options:
  -i <Path to input file>
                        Path to the input file
  -s <EXI/XML string>   A string input

Output Options:
  Defaults to console output

  -o <Output file>      Path to the output file

Mode Options:
  -e                    Toggle XML encoding mode
  -d                    Toggle EXI decoding mode
  -w                    Enable the web server

Configuration Options:
  -profile <Profile Name>
                        Name of the schema profile
  -p port_number        Port for the webserver to run on. Default: 8080
  -v                    Verbose mode
```

### Profile Creation
Profiles can be added to the profiles.py file. The user-defined profiles inform the converter what schemas will be used during the conversation.

A profile must define the following:
- [ ] Profile Name
- [ ] Relative Path to the Schema Folder
- [ ] Schema File Names
- [ ] Unique Message Signatures
- [ ] The default signature indicates a back-up schema

Profile Example: 
```
"din": {                                            # The unique name to reference the profile

        "Folder": "schemas_din",                    # The relative file path to the folder containing
                                                    # the schema files. Depending on the origin of execution
                                                    # this may need to be changed. Ex: ch4ese/schemas_din
        "Files": {
            "V2G_CI_MsgDef.xsd": {                  # The name of the schema file.

                "Grammar": None,                    # The Grammar key will be filled with the grammar
                                                    # dynamically generated at run time using the schema.

                "Signature": "V2G_Message"          # The signature is a unique string found in the XML
                                                    # message that can be used to relate it the correct 
                                                    # schema.
            },
            "V2G_CI_AppProtocol.xsd": {
                "Grammar": None,
                "Signature": "supportedAppProtocol"
            },
            "xmldsig-core-schema.xsd": {
                "Grammar": None,
                "Signature": "default"
            }
        }
    },
```

### Decoding EXI
```
python3 main.py -d -profile iso_15118 -s 8000dbab9371d3234b71d1b981899189d191818991d26b9b3a232b30020000000001d75726e3a69736f3a31353131383a323a323031333a4d73674465660040000080880

<?xml version="1.0" encoding="UTF-8"?><ns4:supportedAppProtocolReq xmlns:ns4="urn:iso:15118:2:2010:AppProtocol" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ns3="http://www.w3.org/2001/XMLSchema"><AppProtocol><ProtocolNamespace>urn:din:70121:2012:MsgDef</ProtocolNamespace><VersionNumberMajor>2</VersionNumberMajor><VersionNumberMinor>0</VersionNumberMinor><SchemaID>0</SchemaID><Priority>1</Priority></AppProtocol><AppProtocol><ProtocolNamespace>urn:iso:15118:2:2013:MsgDef</ProtocolNamespace><VersionNumberMajor>2</VersionNumberMajor><VersionNumberMinor>0</VersionNumberMinor><SchemaID>1</SchemaID><Priority>2</Priority></AppProtocol></ns4:supportedAppProtocolReq>
```

### Encoding XML
```
python3 main.py -e -profile iso_15118 -s '<?xml version="1.0" encoding="UTF-8"?><ns4:supportedAppProtocolReq xmlns:ns4="urn:iso:15118:2:2010:AppProtocol" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ns3="http://www.w3.org/2001/XMLSchema"><AppProtocol><ProtocolNamespace>urn:din:70121:2012:MsgDef</ProtocolNamespace><VersionNumberMajor>2</VersionNumberMajor><VersionNumberMinor>0</VersionNumberMinor><SchemaID>0</SchemaID><Priority>1</Priority></AppProtocol><AppProtocol><ProtocolNamespace>urn:iso:15118:2:2013:MsgDef</ProtocolNamespace><VersionNumberMajor>2</VersionNumberMajor><VersionNumberMinor>0</VersionNumberMinor><SchemaID>1</SchemaID><Priority>2</Priority></AppProtocol></ns4:supportedAppProtocolReq>'

8000dbab9371d3234b71d1b981899189d191818991d26b9b3a232b30020000000001d75726e3a69736f3a31353131383a323a323031333a4d73674465660040000080880
```

### Web Server
#### Server
```
python3 main.py -w -profile din -p 8081
```

#### Client
```
import requests

r = requests.post(url="http://localhost:8081", headers={"Format": "EXI"}, data="EXI_Message")

print(r.text) # XML Result
```

### Verbose Mode
Verbose Mode can be enabled for detailed feedback related to the process state and performance.
```
CH4ESE Logger - INFO - =============================New Request=============================
CH4ESE Logger - INFO - Client Message: 80a0032eae4dc74c8d2dc746e606264627464606264749ae6ce88cacc18ac648ebe9acae6e6c2cecb503a432b0b232b94038eae4dc74c8d2dc746e606264627464606264749ae6ce90cac2c8cae414a6cae6e6d2dedc92898218181502a137b23cc034eae4dc74c8d2dc746e606264627464606264749ae6ce84dec8f220a6cae6e6d2dedca6cae8eae0a4cae3603a2ab21a1a4a2624606060608c606e8c608660606c84628610

CH4ESE Logger - INFO - Server Response: <?xml version="1.0" encoding="UTF-8"?><ns9:V2G_Message xmlns:ns9="urn:din:70121:2012:MsgDef" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ns3="http://www.w3.org/2001/XMLSchema" xmlns:ns4="http://www.w3.org/2000/09/xmldsig#" xmlns:ns5="urn:iso:15118:2:2013:MsgBody" xmlns:ns6="urn:iso:15118:2:2013:MsgDataTypes" xmlns:ns7="urn:iso:15118:2:2013:MsgDef" xmlns:ns8="urn:iso:15118:2:2013:MsgHeader"><ns9:Header><ns10:SessionID xmlns:ns10="urn:din:70121:2012:MsgHeader">00</ns10:SessionID></ns9:Header><ns9:Body><ns11:SessionSetupReq xmlns:ns11="urn:din:70121:2012:MsgBody"><ns11:EVCCID>0000F07F0C006B1C</ns11:EVCCID></ns11:SessionSetupReq></ns9:Body></ns9:V2G_Message>

CH4ESE Logger - INFO - Client Address: 127.0.0.1:46958
CH4ESE Logger - INFO - Conversion Time: 0.0541386604309082
CH4ESE Logger - INFO - =============================End Request=============================
```
