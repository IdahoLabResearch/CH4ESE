""""
CH4ESE - Conversion Helper 4 Easy Serialization of EXI
Copyright 2024, Battelle Energy Alliance, LLC
"""

# Profile folder paths may need to be customized depending on execution location
# Profile Template:
"""
"template_name" :{
    "Folder": "<Path To Folder>",
    "Files": {
        "<File Name>": {
            "Grammar": None,
            "Signature": "<Unique Schema String> or default"
        }
    }
}
"""

profiles = {
    "din": {
        "Folder": "schemas_din",
        "Files": {
            "V2G_CI_AppProtocol.xsd": {
                "Grammar": None,
                "Signature": "supportedAppProtocol"
            },
            "V2G_CI_MsgDef.xsd": {
                "Grammar": None,
                "Signature": "V2G_Message"
            },
            "xmldsig-core-schema.xsd": {
                "Grammar": None,
                "Signature": "default"
            }
        }
    },
    "din_proto":
    {
        "Folder": "schemas_din",
        "Files": {
            "V2G_CI_AppProtocol.xsd": {
                "Grammar": None,
                "Signature": "supportedAppProtocol"
            }
        }
    },
    "din_msg":
    {
        "Folder": "schemas_din",
        "Files": {
            "V2G_CI_MsgDef.xsd": {
                "Grammar": None,
                "Signature": "V2G_Message"
            }
        }
    },

    "iso_15118":{
        "Folder": "schemas_iso",
        "Files":{
            "V2G_CI_MsgDef.xsd": {
                "Grammar": None,
                "Signature": "V2G_Message"
            },
            "V2G_CI_AppProtocol.xsd": {
                "Grammar": None,
                "Signature": "supportedAppProtocol"
            },
            "xmldsig-core-schema.xsd":{
                "Grammar": None,
                "Signature": "default"
            }
        }
    }
}
