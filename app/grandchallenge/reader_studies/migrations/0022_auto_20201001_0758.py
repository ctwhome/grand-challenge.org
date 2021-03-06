# Generated by Django 3.1.1 on 2020-10-01 07:58

from django.db import migrations, models

import grandchallenge.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ("reader_studies", "0021_readerstudy_allow_show_all_annotations"),
    ]

    operations = [
        migrations.AlterField(
            model_name="answer",
            name="answer",
            field=models.JSONField(
                null=True,
                validators=[
                    grandchallenge.core.validators.JSONSchemaValidator(
                        schema={
                            "$schema": "http://json-schema.org/draft-07/schema#",
                            "anyOf": [
                                {"$ref": "#/definitions/null"},
                                {"$ref": "#/definitions/STXT"},
                                {"$ref": "#/definitions/MTXT"},
                                {"$ref": "#/definitions/BOOL"},
                                {"$ref": "#/definitions/HEAD"},
                                {"$ref": "#/definitions/2DBB"},
                                {"$ref": "#/definitions/DIST"},
                                {"$ref": "#/definitions/MDIS"},
                                {"$ref": "#/definitions/POIN"},
                                {"$ref": "#/definitions/MPOI"},
                                {"$ref": "#/definitions/POLY"},
                                {"$ref": "#/definitions/MPOL"},
                                {"$ref": "#/definitions/CHOI"},
                                {"$ref": "#/definitions/MCHO"},
                                {"$ref": "#/definitions/MCHD"},
                            ],
                            "definitions": {
                                "2DBB": {
                                    "properties": {
                                        "corners": {
                                            "items": {
                                                "items": {"type": "number"},
                                                "maxItems": 3,
                                                "minItems": 3,
                                                "type": "array",
                                            },
                                            "maxItems": 4,
                                            "minItems": 4,
                                            "type": "array",
                                        },
                                        "name": {"type": "string"},
                                        "type": {"enum": ["2D bounding box"]},
                                    },
                                    "required": ["version", "type", "corners"],
                                    "type": "object",
                                },
                                "BOOL": {"type": "boolean"},
                                "CHOI": {"type": "number"},
                                "DIST": {
                                    "properties": {
                                        "end": {
                                            "items": {"type": "number"},
                                            "maxItems": 3,
                                            "minItems": 3,
                                            "type": "array",
                                        },
                                        "name": {"type": "string"},
                                        "start": {
                                            "items": {"type": "number"},
                                            "maxItems": 3,
                                            "minItems": 3,
                                            "type": "array",
                                        },
                                        "type": {
                                            "enum": ["Distance measurement"]
                                        },
                                    },
                                    "required": [
                                        "version",
                                        "type",
                                        "start",
                                        "end",
                                    ],
                                    "type": "object",
                                },
                                "HEAD": {"type": "null"},
                                "MCHD": {
                                    "items": {"type": "number"},
                                    "type": "array",
                                },
                                "MCHO": {
                                    "items": {"type": "number"},
                                    "type": "array",
                                },
                                "MDIS": {
                                    "properties": {
                                        "lines": {
                                            "items": {
                                                "allOf": [
                                                    {
                                                        "$ref": "#/definitions/line-object"
                                                    }
                                                ]
                                            },
                                            "type": "array",
                                        },
                                        "name": {"type": "string"},
                                        "type": {
                                            "enum": [
                                                "Multiple distance measurements"
                                            ]
                                        },
                                    },
                                    "required": ["version", "type", "lines"],
                                    "type": "object",
                                },
                                "MPOI": {
                                    "properties": {
                                        "name": {"type": "string"},
                                        "points": {
                                            "items": {
                                                "allOf": [
                                                    {
                                                        "$ref": "#/definitions/point-object"
                                                    }
                                                ]
                                            },
                                            "type": "array",
                                        },
                                        "type": {"enum": ["Multiple points"]},
                                    },
                                    "required": ["version", "type", "points"],
                                    "type": "object",
                                },
                                "MPOL": {
                                    "properties": {
                                        "name": {"type": "string"},
                                        "polygons": {
                                            "items": {
                                                "$ref": "#/definitions/polygon-object"
                                            },
                                            "type": "array",
                                        },
                                        "type": {
                                            "enum": ["Multiple polygons"]
                                        },
                                    },
                                    "required": [
                                        "type",
                                        "version",
                                        "polygons",
                                    ],
                                    "type": "object",
                                },
                                "MTXT": {"type": "string"},
                                "POIN": {
                                    "properties": {
                                        "name": {"type": "string"},
                                        "point": {
                                            "items": {"type": "number"},
                                            "maxItems": 3,
                                            "minItems": 3,
                                            "type": "array",
                                        },
                                        "type": {"enum": ["Point"]},
                                    },
                                    "required": ["version", "type", "point"],
                                    "type": "object",
                                },
                                "POLY": {
                                    "properties": {
                                        "groups": {
                                            "items": {"type": "string"},
                                            "type": "array",
                                        },
                                        "name": {"type": "string"},
                                        "path_points": {
                                            "items": {
                                                "items": {"type": "number"},
                                                "maxItems": 3,
                                                "minItems": 3,
                                                "type": "array",
                                            },
                                            "type": "array",
                                        },
                                        "seed_point": {
                                            "items": {"type": "number"},
                                            "maxItems": 3,
                                            "minItems": 3,
                                            "type": "array",
                                        },
                                        "sub_type": {"type": "string"},
                                    },
                                    "required": [
                                        "name",
                                        "seed_point",
                                        "path_points",
                                        "sub_type",
                                        "groups",
                                        "version",
                                    ],
                                    "type": "object",
                                },
                                "STXT": {"type": "string"},
                                "line-object": {
                                    "properties": {
                                        "end": {
                                            "items": {"type": "number"},
                                            "maxItems": 3,
                                            "minItems": 3,
                                            "type": "array",
                                        },
                                        "name": {"type": "string"},
                                        "start": {
                                            "items": {"type": "number"},
                                            "maxItems": 3,
                                            "minItems": 3,
                                            "type": "array",
                                        },
                                    },
                                    "required": ["start", "end"],
                                    "type": "object",
                                },
                                "null": {"type": "null"},
                                "point-object": {
                                    "properties": {
                                        "name": {"type": "string"},
                                        "point": {
                                            "items": {"type": "number"},
                                            "maxItems": 3,
                                            "minItems": 3,
                                            "type": "array",
                                        },
                                    },
                                    "required": ["point"],
                                    "type": "object",
                                },
                                "polygon-object": {
                                    "properties": {
                                        "groups": {
                                            "items": {"type": "string"},
                                            "type": "array",
                                        },
                                        "name": {"type": "string"},
                                        "path_points": {
                                            "items": {
                                                "items": {"type": "number"},
                                                "maxItems": 3,
                                                "minItems": 3,
                                                "type": "array",
                                            },
                                            "type": "array",
                                        },
                                        "seed_point": {
                                            "items": {"type": "number"},
                                            "maxItems": 3,
                                            "minItems": 3,
                                            "type": "array",
                                        },
                                        "sub_type": {"type": "string"},
                                    },
                                    "required": [
                                        "name",
                                        "seed_point",
                                        "path_points",
                                        "sub_type",
                                        "groups",
                                    ],
                                    "type": "object",
                                },
                            },
                            "properties": {
                                "version": {
                                    "additionalProperties": {"type": "number"},
                                    "required": ["major", "minor"],
                                    "type": "object",
                                }
                            },
                        }
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="historicalanswer",
            name="answer",
            field=models.JSONField(
                null=True,
                validators=[
                    grandchallenge.core.validators.JSONSchemaValidator(
                        schema={
                            "$schema": "http://json-schema.org/draft-07/schema#",
                            "anyOf": [
                                {"$ref": "#/definitions/null"},
                                {"$ref": "#/definitions/STXT"},
                                {"$ref": "#/definitions/MTXT"},
                                {"$ref": "#/definitions/BOOL"},
                                {"$ref": "#/definitions/HEAD"},
                                {"$ref": "#/definitions/2DBB"},
                                {"$ref": "#/definitions/DIST"},
                                {"$ref": "#/definitions/MDIS"},
                                {"$ref": "#/definitions/POIN"},
                                {"$ref": "#/definitions/MPOI"},
                                {"$ref": "#/definitions/POLY"},
                                {"$ref": "#/definitions/MPOL"},
                                {"$ref": "#/definitions/CHOI"},
                                {"$ref": "#/definitions/MCHO"},
                                {"$ref": "#/definitions/MCHD"},
                            ],
                            "definitions": {
                                "2DBB": {
                                    "properties": {
                                        "corners": {
                                            "items": {
                                                "items": {"type": "number"},
                                                "maxItems": 3,
                                                "minItems": 3,
                                                "type": "array",
                                            },
                                            "maxItems": 4,
                                            "minItems": 4,
                                            "type": "array",
                                        },
                                        "name": {"type": "string"},
                                        "type": {"enum": ["2D bounding box"]},
                                    },
                                    "required": ["version", "type", "corners"],
                                    "type": "object",
                                },
                                "BOOL": {"type": "boolean"},
                                "CHOI": {"type": "number"},
                                "DIST": {
                                    "properties": {
                                        "end": {
                                            "items": {"type": "number"},
                                            "maxItems": 3,
                                            "minItems": 3,
                                            "type": "array",
                                        },
                                        "name": {"type": "string"},
                                        "start": {
                                            "items": {"type": "number"},
                                            "maxItems": 3,
                                            "minItems": 3,
                                            "type": "array",
                                        },
                                        "type": {
                                            "enum": ["Distance measurement"]
                                        },
                                    },
                                    "required": [
                                        "version",
                                        "type",
                                        "start",
                                        "end",
                                    ],
                                    "type": "object",
                                },
                                "HEAD": {"type": "null"},
                                "MCHD": {
                                    "items": {"type": "number"},
                                    "type": "array",
                                },
                                "MCHO": {
                                    "items": {"type": "number"},
                                    "type": "array",
                                },
                                "MDIS": {
                                    "properties": {
                                        "lines": {
                                            "items": {
                                                "allOf": [
                                                    {
                                                        "$ref": "#/definitions/line-object"
                                                    }
                                                ]
                                            },
                                            "type": "array",
                                        },
                                        "name": {"type": "string"},
                                        "type": {
                                            "enum": [
                                                "Multiple distance measurements"
                                            ]
                                        },
                                    },
                                    "required": ["version", "type", "lines"],
                                    "type": "object",
                                },
                                "MPOI": {
                                    "properties": {
                                        "name": {"type": "string"},
                                        "points": {
                                            "items": {
                                                "allOf": [
                                                    {
                                                        "$ref": "#/definitions/point-object"
                                                    }
                                                ]
                                            },
                                            "type": "array",
                                        },
                                        "type": {"enum": ["Multiple points"]},
                                    },
                                    "required": ["version", "type", "points"],
                                    "type": "object",
                                },
                                "MPOL": {
                                    "properties": {
                                        "name": {"type": "string"},
                                        "polygons": {
                                            "items": {
                                                "$ref": "#/definitions/polygon-object"
                                            },
                                            "type": "array",
                                        },
                                        "type": {
                                            "enum": ["Multiple polygons"]
                                        },
                                    },
                                    "required": [
                                        "type",
                                        "version",
                                        "polygons",
                                    ],
                                    "type": "object",
                                },
                                "MTXT": {"type": "string"},
                                "POIN": {
                                    "properties": {
                                        "name": {"type": "string"},
                                        "point": {
                                            "items": {"type": "number"},
                                            "maxItems": 3,
                                            "minItems": 3,
                                            "type": "array",
                                        },
                                        "type": {"enum": ["Point"]},
                                    },
                                    "required": ["version", "type", "point"],
                                    "type": "object",
                                },
                                "POLY": {
                                    "properties": {
                                        "groups": {
                                            "items": {"type": "string"},
                                            "type": "array",
                                        },
                                        "name": {"type": "string"},
                                        "path_points": {
                                            "items": {
                                                "items": {"type": "number"},
                                                "maxItems": 3,
                                                "minItems": 3,
                                                "type": "array",
                                            },
                                            "type": "array",
                                        },
                                        "seed_point": {
                                            "items": {"type": "number"},
                                            "maxItems": 3,
                                            "minItems": 3,
                                            "type": "array",
                                        },
                                        "sub_type": {"type": "string"},
                                    },
                                    "required": [
                                        "name",
                                        "seed_point",
                                        "path_points",
                                        "sub_type",
                                        "groups",
                                        "version",
                                    ],
                                    "type": "object",
                                },
                                "STXT": {"type": "string"},
                                "line-object": {
                                    "properties": {
                                        "end": {
                                            "items": {"type": "number"},
                                            "maxItems": 3,
                                            "minItems": 3,
                                            "type": "array",
                                        },
                                        "name": {"type": "string"},
                                        "start": {
                                            "items": {"type": "number"},
                                            "maxItems": 3,
                                            "minItems": 3,
                                            "type": "array",
                                        },
                                    },
                                    "required": ["start", "end"],
                                    "type": "object",
                                },
                                "null": {"type": "null"},
                                "point-object": {
                                    "properties": {
                                        "name": {"type": "string"},
                                        "point": {
                                            "items": {"type": "number"},
                                            "maxItems": 3,
                                            "minItems": 3,
                                            "type": "array",
                                        },
                                    },
                                    "required": ["point"],
                                    "type": "object",
                                },
                                "polygon-object": {
                                    "properties": {
                                        "groups": {
                                            "items": {"type": "string"},
                                            "type": "array",
                                        },
                                        "name": {"type": "string"},
                                        "path_points": {
                                            "items": {
                                                "items": {"type": "number"},
                                                "maxItems": 3,
                                                "minItems": 3,
                                                "type": "array",
                                            },
                                            "type": "array",
                                        },
                                        "seed_point": {
                                            "items": {"type": "number"},
                                            "maxItems": 3,
                                            "minItems": 3,
                                            "type": "array",
                                        },
                                        "sub_type": {"type": "string"},
                                    },
                                    "required": [
                                        "name",
                                        "seed_point",
                                        "path_points",
                                        "sub_type",
                                        "groups",
                                    ],
                                    "type": "object",
                                },
                            },
                            "properties": {
                                "version": {
                                    "additionalProperties": {"type": "number"},
                                    "required": ["major", "minor"],
                                    "type": "object",
                                }
                            },
                        }
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="readerstudy",
            name="case_text",
            field=models.JSONField(
                blank=True,
                default=dict,
                validators=[
                    grandchallenge.core.validators.JSONSchemaValidator(
                        schema={
                            "additionalProperties": {"type": "string"},
                            "properties": {},
                            "type": "object",
                        }
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="readerstudy",
            name="hanging_list",
            field=models.JSONField(
                blank=True,
                default=list,
                validators=[
                    grandchallenge.core.validators.JSONSchemaValidator(
                        schema={
                            "$schema": "http://json-schema.org/draft-06/schema#",
                            "definitions": {},
                            "items": {
                                "$id": "#/items",
                                "additionalProperties": False,
                                "properties": {
                                    "main": {
                                        "$id": "#/items/properties/main",
                                        "default": "",
                                        "examples": ["im1.mhd"],
                                        "pattern": "^(.*)$",
                                        "title": "The Main Schema",
                                        "type": "string",
                                    },
                                    "main-overlay": {
                                        "$id": "#/items/properties/main-overlay",
                                        "default": "",
                                        "examples": ["im1-overlay.mhd"],
                                        "pattern": "^(.*)$",
                                        "title": "The Main Overlay Schema",
                                        "type": "string",
                                    },
                                    "secondary": {
                                        "$id": "#/items/properties/secondary",
                                        "default": "",
                                        "examples": ["im2.mhd"],
                                        "pattern": "^(.*)$",
                                        "title": "The Secondary Schema",
                                        "type": "string",
                                    },
                                    "secondary-overlay": {
                                        "$id": "#/items/properties/secondary-overlay",
                                        "default": "",
                                        "examples": ["im2-overlay.mhd"],
                                        "pattern": "^(.*)$",
                                        "title": "The Secondary Overlay Schema",
                                        "type": "string",
                                    },
                                },
                                "required": ["main"],
                                "title": "The Items Schema",
                                "type": "object",
                            },
                            "title": "The Hanging List Schema",
                            "type": "array",
                        }
                    )
                ],
            ),
        ),
    ]
