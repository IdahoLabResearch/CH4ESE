""""
CH4ESE - Conversion Helper 4 Easy Serialization of EXI
Copyright 2024, Battelle Energy Alliance, LLC
"""

import pathlib

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
        "Folder": pathlib.Path(__file__).parent.parent / "schemas_din",
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
        "Folder": pathlib.Path(__file__).parent.parent / "schemas_din",
        "Files": {
            "V2G_CI_AppProtocol.xsd": {
                "Grammar": None,
                "Signature": "supportedAppProtocol"
            }
        }
    },
    "din_msg":
    {
        "Folder": pathlib.Path(__file__).parent.parent / "schemas_din",
        "Files": {
            "V2G_CI_MsgDef.xsd": {
                "Grammar": None,
                "Signature": "V2G_Message"
            }
        }
    },

    "iso-2":{
        "Folder": pathlib.Path(__file__).parent.parent / "schemas_iso-2",
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
