"""Tests for examples from the STJ specification document.

This module contains tests for all JSON examples provided in the STJ specification.
Each test validates that the example from the spec is valid according to stjlib.

Spec sections covered:
- Root Structure (#root-structure)
  - Basic structure
  - Invalid root structures
- Metadata Section (#metadata-section)
  - Basic metadata
  - Languages metadata
  - Source metadata
- Transcript Section (#transcript-section)
  - Speakers
  - Segments
  - Styles
- Word Timing (#word-timing)
  - Complete mode
  - Partial mode
  - Text alignment
- Time Format (#time-format)
  - Valid time values
  - Invalid time values
- Extensions (#extensions)
  - Custom extensions
  - Format-specific extensions
- Format Comparisons
  - SRT examples
  - WebVTT examples
  - TTML examples
- Empty Value Validation (#empty-value-validation)
  - Array validation
  - Object validation
  - String validation
- Language Code Validation (#language-code-validation)
  - ISO 639-1 codes
  - ISO 639-3 codes
  - Code consistency
- Reserved Namespace Examples (#reserved-namespaces)
  - Reserved namespace protection
  - Custom namespace usage
"""

import pytest
from stjlib import StandardTranscriptionJSON

# Root Structure Examples
def test_basic_stj_structure():
    """Tests the basic STJ structure example.
    
    Reference: spec/latest/stj-specification.md#root-structure
    """
    stj_data = {
        "stj": {
            "version": "0.6.0",
            "transcript": { 
                "segments": [
                    {"text": "Hello world"}
                ]
            }
        }
    }
    
    stj = StandardTranscriptionJSON.from_dict(stj_data)
    validation_issues = stj.validate(raise_exception=False)
    assert not validation_issues

def test_invalid_root_structures():
    """Tests the invalid root structure examples.
    
    Reference: spec/latest/stj-specification.md#examples-of-invalid-root-structures
    """
    # Missing mandatory fields
    with pytest.raises(Exception):
        StandardTranscriptionJSON.from_dict({"stj": {}})
    
    # Missing transcript
    with pytest.raises(Exception):
        StandardTranscriptionJSON.from_dict({
            "stj": {
                "version": "0.6.0"
            }
        })
    
    # Missing stj root object
    with pytest.raises(Exception):
        StandardTranscriptionJSON.from_dict({
            "version": "0.6.0",
            "transcript": {}
        })

def test_metadata_example():
    """Tests the metadata section example.
    
    Reference: spec/latest/stj-specification.md#metadata-section
    """
    stj_data = {
        "stj": {
            "version": "0.6.0",
            "metadata": {
                "transcriber": {
                    "name": "YAWT",
                    "version": "0.6.0"
                },
                "created_at": "2024-10-27T12:00:00Z"
            },
            "transcript": {
                "segments": [{"text": "Hello"}]
            }
        }
    }
    
    stj = StandardTranscriptionJSON.from_dict(stj_data)
    validation_issues = stj.validate(raise_exception=False)
    assert not validation_issues

def test_languages_metadata_example():
    """Tests the languages metadata example.
    
    Reference: spec/latest/stj-specification.md#metadata-section
    """
    stj_data = {
        "stj": {
            "version": "0.6.0",
            "metadata": {
                "transcriber": {
                    "name": "YAWT",
                    "version": "0.4.0"
                },
                "created_at": "2024-10-20T12:00:00Z",
                "source": {
                    "uri": "https://example.com/multilingual_media.mp4",
                    "duration": 3600.5,
                    "languages": ["en", "es"]
                },
                "languages": ["fr"],
                "confidence_threshold": 0.6,
                "extensions": {
                    "project_info": {
                        "project": "International Conference",
                        "client": "Global Events Inc."
                    }
                }
            },
            "transcript": {
                "segments": [{"text": "Hello"}]
            }
        }
    }
    
    stj = StandardTranscriptionJSON.from_dict(stj_data)
    validation_issues = stj.validate(raise_exception=False)
    assert not validation_issues

# Speakers Examples
def test_speakers_example():
    """Tests the speakers example.
    
    Reference: spec/latest/stj-specification.md#speakers
    """
    stj_data = {
        "stj": {
            "version": "0.6.0",
            "transcript": {
                "speakers": [
                    {"id": "Speaker1", "name": "Dr. Smith"},
                    {"id": "Speaker2", "name": "Señora García"},
                    {"id": "Speaker3", "name": "Monsieur Dupont"},
                    {"id": "Speaker4"}  # Anonymous speaker
                ],
                "segments": [{"text": "Hello"}]
            }
        }
    }
    
    stj = StandardTranscriptionJSON.from_dict(stj_data)
    validation_issues = stj.validate(raise_exception=False)
    assert not validation_issues

# Segments Examples
def test_segments_example():
    """Tests the segments example with different word timing modes.
    
    Reference: spec/latest/stj-specification.md#segments
    """
    stj_data = {
        "stj": {
            "version": "0.6.0",
            "transcript": {
                "speakers": [
                    {"id": "Speaker1", "name": "Speaker One"},
                    {"id": "Speaker2", "name": "Speaker Two"},
                    {"id": "Speaker3", "name": "Speaker Three"}
                ],
                "segments": [
                    {
                        "start": 0.0,
                        "end": 5.0,
                        "text": "Bonjour tout le monde.",
                        "speaker_id": "Speaker1",
                        "confidence": 0.95,
                        "language": "fr",
                        "word_timing_mode": "complete",
                        "words": [
                            {"start": 0.0, "end": 1.0, "text": "Bonjour"},
                            {"start": 1.0, "end": 2.0, "text": "tout"},
                            {"start": 2.0, "end": 3.0, "text": "le"},
                            {"start": 3.0, "end": 4.0, "text": "monde."}
                        ]
                    },
                    {
                        "start": 5.1,
                        "end": 10.0,
                        "text": "Gracias por estar aquí hoy.",
                        "speaker_id": "Speaker2",
                        "confidence": 0.93,
                        "language": "es",
                        "word_timing_mode": "partial",
                        "words": [
                            {"start": 5.1, "end": 5.5, "text": "Gracias"}
                        ]
                    },
                    {
                        "start": 10.1,
                        "end": 10.1,
                        "is_zero_duration": True,
                        "text": "[Applause]",
                        "speaker_id": "Speaker3",
                        "confidence": 0.92,
                        "language": "en"
                    }
                ]
            }
        }
    }
    
    stj = StandardTranscriptionJSON.from_dict(stj_data)
    validation_issues = stj.validate(raise_exception=False)
    assert not validation_issues

def test_multilingual_example():
    """Tests the multilingual transcription example.
    
    Reference: spec/latest/stj-specification.md#example-scenario-translated-transcription
    """
    stj_data = {
        "stj": {
            "version": "0.6.0",
            "metadata": {
                "transcriber": {
                    "name": "YAWT",
                    "version": "0.4.0"
                },
                "created_at": "2024-10-20T12:00:00Z",
                "source": {
                    "uri": "https://example.com/event.mp4",
                    "duration": 5400.0,
                    "languages": ["en", "es"]
                },
                "languages": ["fr", "de"]
            },
            "transcript": {
                "speakers": [
                    {"id": "Speaker1", "name": "French Translator"},
                    {"id": "Speaker2", "name": "German Translator"}
                ],
                "segments": [
                    {
                        "start": 0.0,
                        "end": 5.0,
                        "text": "Bonjour à tous.",
                        "speaker_id": "Speaker1",
                        "confidence": 0.95,
                        "language": "fr"
                    },
                    {
                        "start": 5.1,
                        "end": 10.0,
                        "text": "Willkommen alle zusammen.",
                        "speaker_id": "Speaker2",
                        "confidence": 0.94,
                        "language": "de"
                    }
                ]
            }
        }
    }
    
    stj = StandardTranscriptionJSON.from_dict(stj_data)
    validation_issues = stj.validate(raise_exception=False)
    assert not validation_issues

# Style Examples
def test_style_examples():
    """Tests the style examples from the spec.
    
    Reference: spec/latest/stj-specification.md#examples-1
    """
    stj_data = {
        "stj": {
            "version": "0.6.0",
            "transcript": {
                "styles": [
                    {
                        "id": "speaker_1",
                        "text": {
                            "color": "#2E4053",
                            "bold": True,
                            "size": "110%"
                        }
                    },
                    {
                        "id": "caption_style",
                        "text": {
                            "color": "#FFFFFF",
                            "background": "#000000"
                        },
                        "display": {
                            "align": "center",
                            "vertical": "bottom",
                            "position": {
                                "x": "50%",
                                "y": "90%"
                            }
                        }
                    },
                    {
                        "id": "advanced_style",
                        "text": {
                            "color": "#FFFFFF"
                        },
                        "extensions": {
                            "custom_ssa": {
                                "effect": "karaoke",
                                "outline": 2,
                                "shadow": 1
                            }
                        }
                    }
                ],
                "segments": [{"text": "Hello"}]
            }
        }
    }
    
    stj = StandardTranscriptionJSON.from_dict(stj_data)
    validation_issues = stj.validate(raise_exception=False)
    assert not validation_issues

def test_word_text_alignment_examples():
    """Tests the word text alignment examples from the spec.
    
    Reference: spec/latest/stj-specification.md#word-text-alignment
    """
    stj_data = {
        "stj": {
            "version": "0.6.0",
            "transcript": {
                "segments": [
                    {
                        "text": "Hello, world!",
                        "word_timing_mode": "complete",
                        "words": [
                            {"text": "Hello,", "start": 0.0, "end": 0.5},
                            {"text": "world!", "start": 0.6, "end": 1.0}
                        ]
                    },
                    {
                        "text": "Hello, wonderful world!",
                        "word_timing_mode": "partial",
                        "words": [
                            {"text": "Hello,", "start": 0.0, "end": 0.5},
                            {"text": "world!", "start": 1.0, "end": 1.5}
                        ]
                    },
                    {
                        "text": "\"Don't,\" she said, \"go there!\"",
                        "word_timing_mode": "partial",
                        "words": [
                            {"text": "\"Don't,\"", "start": 0.0, "end": 0.5},
                            {"text": "there!\"", "start": 1.0, "end": 1.5}
                        ]
                    }
                ]
            }
        }
    }
    
    stj = StandardTranscriptionJSON.from_dict(stj_data)
    validation_issues = stj.validate(raise_exception=False)
    assert not validation_issues

def test_extension_examples():
    """Tests the extension examples from the spec.
    
    Reference: spec/latest/stj-specification.md#extensions-field-requirements
    """
    stj_data = {
        "stj": {
            "version": "0.6.0",
            "transcript": {
                "segments": [
                    {
                        "text": "Hello",
                        "extensions": {
                            "myapp": {
                                "custom_field": "value",
                                "analysis_data": {
                                    "property": "value"
                                }
                            }
                        }
                    },
                    {
                        "text": "World",
                        "extensions": {
                            "custom_webvtt": {
                                "line": "auto",
                                "position": "50%"
                            }
                        }
                    }
                ]
            }
        }
    }
    
    stj = StandardTranscriptionJSON.from_dict(stj_data)
    validation_issues = stj.validate(raise_exception=False)
    assert not validation_issues

def test_uri_format_examples():
    """Tests the URI format examples from the spec.
    
    Reference: spec/latest/stj-specification.md#uri-format-requirements
    """
    stj_data = {
        "stj": {
            "version": "0.6.0",
            "metadata": {
                "source": {
                    "uri": "http://example.com/media/video.mp4"
                }
            },
            "transcript": {
                "segments": [{"text": "Hello"}]
            }
        }
    }
    
    stj = StandardTranscriptionJSON.from_dict(stj_data)
    validation_issues = stj.validate(raise_exception=False)
    assert not validation_issues

    # Test other URI examples
    valid_uris = [
        "https://example.com/media/audio.mp3",
        "file:///C:/Media/video.mp4",
        "file:///home/user/media/audio.mp3",
        "s3://bucket-name/path/to/object"
    ]
    
    for uri in valid_uris:
        stj_data["stj"]["metadata"]["source"]["uri"] = uri
        stj = StandardTranscriptionJSON.from_dict(stj_data)
        validation_issues = stj.validate(raise_exception=False)
        assert not validation_issues

def test_complex_multilingual_example():
    """Tests the complex multilingual example from the spec.
    
    Reference: spec/latest/stj-specification.md#example-scenario-translated-transcription
    """
    stj_data = {
        "stj": {
            "version": "0.6.0",
            "metadata": {
                "transcriber": {
                    "name": "YAWT",
                    "version": "0.4.0"
                },
                "created_at": "2024-10-19T15:30:00Z",
                "source": {
                    "uri": "https://example.com/funny_conference.mp4",
                    "duration": 1800.0,
                    "languages": ["en", "es", "de"]
                },
                "languages": ["en", "es", "de"],
                "confidence_threshold": 0.6,
                "additional_info": {
                    "project": "Annual Humor Conference",
                    "client": "LaughCorp International"
                }
            },
            "transcript": {
                "speakers": [
                    {
                        "id": "Speaker1",
                        "name": "Dr. Chuckles",
                        "additional_info": {
                            "role": "Keynote Speaker"
                        }
                    },
                    {
                        "id": "Speaker2",
                        "name": "Ms. Giggles",
                        "additional_info": {
                            "role": "Panelist"
                        }
                    },
                    {
                        "id": "Speaker3",
                        "name": "Herr Lachen",
                        "additional_info": {
                            "role": "Guest Speaker"
                        }
                    }
                ],
                "styles": [
                    {
                        "id": "Style1",
                        "formatting": {
                            "bold": True,
                            "italic": False,
                            "underline": False,
                            "color": "#FF5733",
                            "background_color": "#000000"
                        },
                        "positioning": {
                            "align": "center",
                            "line": "auto",
                            "position": "50%",
                            "size": "100%"
                        }
                    }
                ],
                "segments": [
                    {
                        "start": 0.0,
                        "end": 5.0,
                        "text": "Ladies and gentlemen, welcome to the Annual Humor Conference!",
                        "speaker_id": "Speaker1",
                        "confidence": 0.98,
                        "language": "en",
                        "style_id": "Style1",
                        "words": [
                            {"start": 0.0, "end": 0.5, "text": "Ladies", "confidence": 0.99},
                            {"start": 0.5, "end": 0.7, "text": "and", "confidence": 0.98},
                            {"start": 0.7, "end": 1.2, "text": "gentlemen,", "confidence": 0.97},
                            {"start": 1.3, "end": 2.0, "text": "welcome", "confidence": 0.99},
                            {"start": 2.1, "end": 2.3, "text": "to", "confidence": 0.98},
                            {"start": 2.3, "end": 2.5, "text": "the", "confidence": 0.98},
                            {"start": 2.6, "end": 3.5, "text": "Annual", "confidence": 0.97},
                            {"start": 3.6, "end": 5.0, "text": "Humor Conference!", "confidence": 0.96}
                        ]
                    },
                    {
                        "start": 12.1,
                        "end": 17.0,
                        "text": "¡Y ahora, un poco de humor en español!",
                        "speaker_id": "Speaker2",
                        "confidence": 0.94,
                        "language": "es"
                    },
                    {
                        "start": 22.1,
                        "end": 27.0,
                        "text": "Und jetzt etwas auf Deutsch!",
                        "speaker_id": "Speaker3",
                        "confidence": 0.92,
                        "language": "de"
                    }
                ]
            }
        }
    }
    
    stj = StandardTranscriptionJSON.from_dict(stj_data)
    validation_issues = stj.validate(raise_exception=False)
    assert not validation_issues

def test_confidence_threshold_example():
    """Tests the confidence threshold example from the spec.
    
    Reference: spec/latest/stj-specification.md#representing-confidence
    """
    stj_data = {
        "stj": {
            "version": "0.6.0",
            "metadata": {
                "confidence_threshold": 0.8  # High confidence threshold
            },
            "transcript": {
                "segments": [
                    {
                        "text": "High confidence segment",
                        "confidence": 0.95,
                        "words": [
                            {"text": "High", "confidence": 0.98, "start": 0.0, "end": 0.5},
                            {"text": "confidence", "confidence": 0.96, "start": 0.6, "end": 1.2},
                            {"text": "segment", "confidence": 0.92, "start": 1.3, "end": 2.0}
                        ]
                    },
                    {
                        "text": "Lower confidence segment",
                        "confidence": 0.75,  # Below threshold
                        "words": [
                            {"text": "Lower", "confidence": 0.78, "start": 2.1, "end": 2.5},
                            {"text": "confidence", "confidence": 0.72, "start": 2.6, "end": 3.2},
                            {"text": "segment", "confidence": 0.75, "start": 3.3, "end": 4.0}
                        ]
                    }
                ]
            }
        }
    }
    
    stj = StandardTranscriptionJSON.from_dict(stj_data)
    validation_issues = stj.validate(raise_exception=False)
    assert not validation_issues

def test_srt_style_example():
    """Tests the SRT-style example from the spec.
    
    Reference: spec/latest/stj-specification.md#srt-subrip
    """
    stj_data = {
        "stj": {
            "version": "0.6.0",
            "transcript": {
                "segments": [
                    {
                        "start": 0.0,
                        "end": 2.0,
                        "text": "First subtitle"
                    },
                    {
                        "start": 2.1,
                        "end": 4.0,
                        "text": "Second subtitle\nwith line break"
                    }
                ]
            }
        }
    }
    
    stj = StandardTranscriptionJSON.from_dict(stj_data)
    validation_issues = stj.validate(raise_exception=False)
    assert not validation_issues

def test_webvtt_style_example():
    """Tests the WebVTT-style example from the spec.
    
    Reference: spec/latest/stj-specification.md#webvtt
    """
    stj_data = {
        "stj": {
            "version": "0.6.0",
            "transcript": {
                "styles": [
                    {
                        "id": "webvtt_style",
                        "text": {
                            "color": "#FFFFFF",
                            "background": "#000000"
                        },
                        "display": {
                            "align": "center",
                            "vertical": "bottom"
                        },
                        "extensions": {
                            "custom_webvtt": {
                                "line": "-2",
                                "position": "50%"
                            }
                        }
                    }
                ],
                "segments": [
                    {
                        "start": 0.0,
                        "end": 2.0,
                        "text": "Styled subtitle",
                        "style_id": "webvtt_style"
                    }
                ]
            }
        }
    }
    
    stj = StandardTranscriptionJSON.from_dict(stj_data)
    validation_issues = stj.validate(raise_exception=False)
    assert not validation_issues

def test_ttml_style_example():
    """Tests the TTML-style example from the spec.
    
    Reference: spec/latest/stj-specification.md#ttml-timed-text-markup-language
    """
    stj_data = {
        "stj": {
            "version": "0.6.0",
            "transcript": {
                "styles": [
                    {
                        "id": "ttml_style",
                        "text": {
                            "color": "#FFFFFF",
                            "background": "#000000",
                            "size": "120%"
                        },
                        "extensions": {
                            "custom_ttml": {
                                "fontFamily": "Arial",
                                "textOutline": "black 1px"
                            }
                        }
                    }
                ],
                "segments": [
                    {
                        "start": 0.0,
                        "end": 2.0,
                        "text": "TTML styled text",
                        "style_id": "ttml_style",
                        "language": "en"
                    }
                ]
            }
        }
    }
    
    stj = StandardTranscriptionJSON.from_dict(stj_data)
    validation_issues = stj.validate(raise_exception=False)
    assert not validation_issues

def test_extensibility_example():
    """Tests the extensibility example from the spec.
    
    Reference: spec/latest/stj-specification.md#extensibility-and-customization
    """
    stj_data = {
        "stj": {
            "version": "0.6.0",
            "metadata": {
                "extensions": {
                    "custom_app": {
                        "project_id": "12345",
                        "workflow": {
                            "stage": "review",
                            "assignee": "editor@example.com"
                        }
                    }
                }
            },
            "transcript": {
                "segments": [
                    {
                        "text": "Custom segment",
                        "extensions": {
                            "analysis": {
                                "sentiment": "positive",
                                "keywords": ["custom", "segment"],
                                "metrics": {
                                    "clarity": 0.95,
                                    "fluency": 0.88
                                }
                            }
                        }
                    }
                ]
            }
        }
    }
    
    stj = StandardTranscriptionJSON.from_dict(stj_data)
    validation_issues = stj.validate(raise_exception=False)
    assert not validation_issues

def test_reserved_namespace_examples():
    """Tests the reserved namespace examples from the spec.
    
    Reference: spec/latest/stj-specification.md#reserved-namespaces
    """
    # Test invalid use of reserved namespace
    stj_data = {
        "stj": {
            "version": "0.6.0",
            "transcript": {
                "segments": [
                    {
                        "text": "Test",
                        "extensions": {
                            "stj": {  # Reserved namespace
                                "custom": "value"
                            }
                        }
                    }
                ]
            }
        }
    }
    
    stj = StandardTranscriptionJSON.from_dict(stj_data)
    validation_issues = stj.validate(raise_exception=False)
    assert any("Reserved namespace" in issue.message for issue in validation_issues)

def test_empty_value_examples():
    """Tests the empty value examples from the spec.
    
    Reference: spec/latest/stj-specification.md#empty-value-constraints
    """
    # Test valid empty arrays
    stj_data = {
        "stj": {
            "version": "0.6.0",
            "transcript": {
                "speakers": [],  # Valid empty array - speakers attempted but none found
                "segments": [{"text": "Hello"}]  # Cannot be empty
            }
        }
    }

    stj = StandardTranscriptionJSON.from_dict(stj_data)
    validation_issues = stj.validate(raise_exception=False)
    assert not validation_issues

    # Test invalid empty arrays
    invalid_stj_data = {
        "stj": {
            "version": "0.6.0",
            "transcript": {
                "segments": []  # Invalid - segments cannot be empty
            }
        }
    }

    with pytest.raises(Exception):
        StandardTranscriptionJSON.from_dict(invalid_stj_data).validate()

def test_language_code_validation():
    """Tests the language code validation examples from the spec.
    
    Reference: spec/latest/stj-specification.md#language-codes
    """
    # Test valid language codes
    stj_data = {
        "stj": {
            "version": "0.6.0",
            "metadata": {
                "languages": ["en", "fr", "es"]  # Valid ISO 639-1 codes
            },
            "transcript": {
                "segments": [
                    {
                        "text": "Hello",
                        "language": "en"
                    },
                    {
                        "text": "Bonjour",
                        "language": "fr"
                    }
                ]
            }
        }
    }
    
    stj = StandardTranscriptionJSON.from_dict(stj_data)
    validation_issues = stj.validate(raise_exception=False)

    assert not validation_issues

    # Test invalid language codes
    invalid_stj = {
        "stj": {
            "version": "0.6.0",
            "metadata": {
                "languages": ["eng", "en"]  # Mixed ISO 639-1 and 639-3
            },
            "transcript": {
                "segments": [{"text": "Hello"}]
            }
        }
    }
    
    stj = StandardTranscriptionJSON.from_dict(invalid_stj)
    validation_issues = stj.validate(raise_exception=False)
    assert any("language code" in issue.message for issue in validation_issues)

