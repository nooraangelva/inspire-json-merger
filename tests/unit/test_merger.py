from __future__ import absolute_import, division, print_function

from operator import itemgetter

from mock import patch

from inspire_json_merger.api import merge

from utils import assert_ordered_conflicts, validate_subschema

from inspire_json_merger.config import (
    PublisherOnPublisherOperations,
    PublisherOnArxivOperations,
    ArxivOnArxivOperations,
    ArxivOnPublisherOperations,
    ErratumOnPublisherOperations
)


@patch(
    "inspire_json_merger.api.get_configuration",
    return_value=PublisherOnPublisherOperations,
)
def test_merging_same_documents_publisher_on_publisher(fake_get_config):
    root = {
        "documents": [
            {
                "key": "pdf1.pdf",
                "description": "paper",
                "source": "arXiv",
                "fulltext": True,
                "url": "http://example.com/files/1234-1234-1234-1234/pdf1.pdf",
            },
            {
                "key": "pdf.tex",
                "description": "latex version",
                "source": "arXiv",
                "url": "http://example.com/files/1234-1234-1234-1234/pdf.tex",
            },
        ]
    }
    head = root
    update = root
    expected_merged = update
    expected_conflict = []
    merged, conflict = merge(root, head, update)
    assert merged == expected_merged
    assert_ordered_conflicts(conflict, expected_conflict)
    validate_subschema(merged)


@patch(
    "inspire_json_merger.api.get_configuration", return_value=PublisherOnArxivOperations
)
def test_merging_same_documents_publisher_on_arxiv(fake_get_config):
    root = {
        "documents": [
            {
                "key": "pdf1.pdf",
                "description": "paper",
                "source": "arXiv",
                "fulltext": True,
                "url": "http://example.com/files/1234-1234-1234-1234/pdf1.pdf",
            },
            {
                "key": "pdf.tex",
                "description": "latex version",
                "source": "arXiv",
                "url": "http://example.com/files/1234-1234-1234-1234/pdf.tex",
            },
        ]
    }
    head = root
    update = root
    expected_merged = update
    expected_conflict = []
    merged, conflict = merge(root, head, update)
    assert merged == expected_merged
    assert_ordered_conflicts(conflict, expected_conflict)
    validate_subschema(merged)


@patch("inspire_json_merger.api.get_configuration", return_value=ArxivOnArxivOperations)
def test_merging_same_documents_arxiv_on_arxiv(fake_get_config):
    root = {
        "documents": [
            {
                "key": "pdf1.pdf",
                "description": "paper",
                "source": "arXiv",
                "fulltext": True,
                "url": "http://example.com/files/1234-1234-1234-1234/pdf1.pdf",
            },
            {
                "key": "pdf.tex",
                "description": "latex version",
                "source": "arXiv",
                "url": "http://example.com/files/1234-1234-1234-1234/pdf.tex",
            },
        ]
    }
    head = root
    update = root
    expected_merged = head
    expected_conflict = []
    merged, conflict = merge(root, head, update)
    assert merged == expected_merged
    assert_ordered_conflicts(conflict, expected_conflict)
    validate_subschema(merged)


@patch(
    "inspire_json_merger.api.get_configuration", return_value=ArxivOnPublisherOperations
)
def test_merging_same_documents_arxiv_on_publisher(fake_get_config):
    root = {
        "documents": [
            {
                "key": "pdf1.pdf",
                "description": "paper",
                "source": "arXiv",
                "fulltext": True,
                "url": "http://example.com/files/1234-1234-1234-1234/pdf1.pdf",
            },
            {
                "key": "pdf.tex",
                "description": "latex version",
                "source": "arXiv",
                "url": "http://example.com/files/1234-1234-1234-1234/pdf.tex",
            },
        ]
    }
    head = root
    update = root
    expected_merged = update
    expected_conflict = []
    merged, conflict = merge(root, head, update)
    assert merged == expected_merged
    assert_ordered_conflicts(conflict, expected_conflict)
    validate_subschema(merged)


def test_real_record_merge_regression_1_authors_mismatch_on_update():
    root = {
        "$schema": "https://inspirehep.net/schemas/records/hep.json",
        "_collections": ["Literature"],
        "authors": [
            {"full_name": "Elliott"},
            {"full_name": "Chris"},
            {"full_name": "Gwilliam"},
            {"full_name": "Owen"},
        ],
        "titles": [
            {
                "source": "arXiv",
                "title": "Spontaneous symmetry breaking: a view from derived "
                "geometry",
            }
        ],
    }

    head = {
        "$schema": "https://inspirehep.net/schemas/records/hep.json",
        "_collections": ["Literature"],
        "authors": [
            {
                "affiliations": [
                    {
                        "record": {
                            "$ref": "https://inspirehep.net/api/institutions/945696"
                        },
                        "value": "UMass Amherst",
                    },
                    {
                        "record": {
                            "$ref": "https://inspirehep.net/api/institutions/1272963"
                        },
                        "value": "UMASS, Amherst, Dept. Math. Stat.",
                    },
                ],
                "emails": ["celliott@math.umass.edu"],
                "full_name": "Elliott",
                "ids": [{"schema": "INSPIRE BAI", "value": "Elliott.1"}],
                "signature_block": "ELAT",
                "uuid": "65aa01c7-99ec-4c35-ac6b-bbc667a4343e",
            },
            {
                "full_name": "Chris",
                "ids": [{"schema": "INSPIRE BAI", "value": "Chris.1"}],
                "signature_block": "CHR",
                "uuid": "36b3a255-f8f2-46a6-bfae-9e9d00335434",
            },
            {
                "affiliations": [
                    {
                        "record": {
                            "$ref": "https://inspirehep.net/api/institutions/945696"
                        },
                        "value": "UMass Amherst",
                    },
                    {
                        "record": {
                            "$ref": "https://inspirehep.net/api/institutions/1272963"
                        },
                        "value": "UMASS, Amherst, Dept. Math. Stat.",
                    },
                ],
                "emails": ["gwilliam@math.umass.edu"],
                "full_name": "Gwilliam",
                "ids": [{"schema": "INSPIRE BAI", "value": "Gwilliam.1"}],
                "signature_block": "GWALAN",
                "uuid": "66f5722f-e649-4438-a7f5-d01247371f22",
            },
            {
                "full_name": "Owen",
                "ids": [{"schema": "INSPIRE BAI", "value": "Owen.1"}],
                "signature_block": "OWAN",
                "uuid": "27de5ee5-d21a-47b2-b22c-fd44231128f9",
            },
        ],
        "titles": [
            {
                "source": "arXiv",
                "title": "Spontaneous symmetry breaking: a view from derived "
                "geometry",
            }
        ],
    }

    update = {
        "$schema": "https://inspirehep.net/schemas/records/hep.json",
        "_collections": ["Literature"],
        "authors": [{"full_name": "Elliott, Chris"}, {"full_name": "Gwilliam, Owen"}],
        "titles": [
            {
                "source": "arXiv",
                "title": "Spontaneous symmetry breaking: a view from derived "
                "geometry",
            }
        ],
    }
    expected_merged = dict(head)

    expected_conflicts = [
        {
            "path": "/authors/3",
            "op": "replace",
            "value": {"full_name": "Gwilliam, Owen"},
            "$type": "SET_FIELD",
        },
        {
            "path": "/authors/2",
            "op": "replace",
            "value": {"full_name": "Gwilliam, Owen"},
            "$type": "SET_FIELD",
        },
        {
            "path": "/authors/0",
            "op": "replace",
            "value": {"full_name": "Elliott, Chris"},
            "$type": "SET_FIELD",
        },
        {
            "path": "/authors/1",
            "op": "replace",
            "value": {"full_name": "Elliott, Chris"},
            "$type": "SET_FIELD",
        },
    ]

    merged, conflict = merge(root, head, update)
    assert merged == expected_merged
    assert sorted(conflict, key=itemgetter("path")) == sorted(
        expected_conflicts, key=itemgetter("path")
    )


@patch(
    "inspire_json_merger.api.get_configuration", return_value=PublisherOnArxivOperations
)
def test_merging_acquisition_source_publisher_on_arxiv(fake_get_config):
    root = {
        "acquisition_source": {
            "datetime": "2021-05-11T02:35:43.387350",
            "method": "hepcrawl",
            "source": "arXiv",
            "submission_number": "c8a0e3e0b20011eb8d930a580a6402c0"
        }
    }
    head = {
        "acquisition_source": {
            "datetime": "2021-05-11T02:35:43.387350",
            "method": "hepcrawl",
            "source": "arXiv",
            "submission_number": "c8a0e3e0b20011eb8d930a580a6402c0"
        }
    }
    update = {
        "acquisition_source": {
            "datetime": "2021-05-12T02:35:43.387350",
            "method": "beard",
            "source": "other source",
            "submission_number": "c8a0e3e0b20011eb8d930a580a6402c1"
        }
    }
    expected_merged = update
    expected_conflict = []
    merged, conflict = merge(root, head, update)
    assert merged == expected_merged
    assert_ordered_conflicts(conflict, expected_conflict)
    validate_subschema(merged)


@patch(
    "inspire_json_merger.api.get_configuration", return_value=PublisherOnArxivOperations
)
def test_merging_cleans_acquisition_source_for_publisher_on_arxiv(fake_get_config):
    root = {
        "acquisition_source": {
            "datetime": "2021-05-11T02:35:43.387350",
            "method": "hepcrawl",
            "source": "desy",
            "submission_number": "c8a0e3e0b20011eb8d930a580a6402c0"
        }
    }
    head = {
        "acquisition_source": {
            "datetime": "2021-05-11T02:35:43.387350",
            "method": "hepcrawl",
            "source": "arXiv",
            "submission_number": "c8a0e3e0b20011eb8d930a580a6402c0"
        }
    }
    update = {
        "acquisition_source": {
            "datetime": "2021-05-12T02:35:43.387350",
            "method": "hepcrawl",
            "source": "desy",
            "submission_number": "c8a0e3e0b20011eb8d930a580a6402c1"
        }
    }

    merged, conflict = merge(root, head, update)
    assert merged['acquisition_source']['source'] == 'desy'


@patch(
    "inspire_json_merger.api.get_configuration", return_value=PublisherOnPublisherOperations
)
def test_merging_cleans_acquisition_source_for_publisher_on_publisher(fake_get_config):
    root = {
        "acquisition_source": {
            "datetime": "2021-05-11T02:35:43.387350",
            "method": "hepcrawl",
            "source": "desy",
            "submission_number": "c8a0e3e0b20011eb8d930a580a6402c0"
        }
    }
    head = {
        "acquisition_source": {
            "datetime": "2021-05-11T02:35:43.387350",
            "method": "hepcrawl",
            "source": "elsevier",
            "submission_number": "c8a0e3e0b20011eb8d930a580a6402c0"
        }
    }
    update = {
        "acquisition_source": {
            "datetime": "2021-05-12T02:35:43.387350",
            "method": "hepcrawl",
            "source": "desy",
            "submission_number": "c8a0e3e0b20011eb8d930a580a6402c1"
        }
    }

    merged, conflict = merge(root, head, update)
    assert merged['acquisition_source']['source'] == 'desy'


@patch(
    "inspire_json_merger.api.get_configuration", return_value=ArxivOnPublisherOperations
)
def test_merging_cleans_acquisition_source_for_arxiv_on_publisher(fake_get_config):
    root = {
        "acquisition_source": {
            "datetime": "2021-05-11T02:35:43.387350",
            "method": "arXiv",
            "source": "arXiv",
            "submission_number": "c8a0e3e0b20011eb8d930a580a6402c0"
        }
    }
    head = {
        "acquisition_source": {
            "datetime": "2021-05-11T02:35:43.387350",
            "method": "hepcrawl",
            "source": "desy",
            "submission_number": "c8a0e3e0b20011eb8d930a580a6402c0"
        }
    }
    update = {
        "acquisition_source": {
            "datetime": "2021-05-12T02:35:43.387350",
            "method": "hepcrawl",
            "source": "arXiv",
            "submission_number": "c8a0e3e0b20011eb8d930a580a6402c1"
        }
    }

    merged, conflict = merge(root, head, update)
    assert merged['acquisition_source']['source'] == 'arXiv'


@patch(
    "inspire_json_merger.api.get_configuration", return_value=ArxivOnPublisherOperations
)
def test_merging_publication_info_for_arxiv_on_publisher(fake_get_config):
    root = {
        "publication_info": [
            {
                "year": 2021,
                "artid": "051701",
                "material": "publication",
                "journal_issue": "5",
                "journal_title": "root title",
                "journal_record": {
                    "$ref": "https://inspirehep.net/api/journals/1613970"
                },
                "journal_volume": "104",
            }
        ]
    }
    head = {
        "publication_info": [
            {
                "year": 2021,
                "artid": "051701",
                "material": "publication",
                "journal_issue": "5",
                "journal_title": "head title",
                "journal_record": {
                    "$ref": "https://inspirehep.net/api/journals/1613970"
                },
                "journal_volume": "104",
            }
        ]
    }
    update = {
        "publication_info": [
            {
                "year": 2021,
                "artid": "051701",
                "material": "publication",
                "journal_issue": "5",
                "journal_title": "update title",
                "journal_record": {
                    "$ref": "https://inspirehep.net/api/journals/1613970"
                },
                "journal_volume": "104",
            }
        ]
    }

    merged, conflict = merge(root, head, update)
    assert len(merged['publication_info']) == 1
    assert merged['publication_info'][0]['journal_title'] == 'head title'


@patch(
    "inspire_json_merger.api.get_configuration",
    return_value=ErratumOnPublisherOperations,
)
def test_merging_erratum(fake_get_config):
    root = {
        "publication_info": [
            {
                "year": 2021,
                "artid": "051701",
                "material": "publication",
                "journal_issue": "5",
                "journal_title": "root title",
                "journal_record": {
                    "$ref": "https://inspirehep.net/api/journals/1613970"
                },
                "journal_volume": "104",
            }
        ]
    }
    head = {
        "authors": [{"full_name": "Test, Chris"}],
        "dois": [
            {
                "value": "10.1016/j.newast.2021.101676",
                "source": "Elsevier B.V.",
                "material": "publication",
            }
        ],
        "publication_info": [
            {
                "year": 2021,
                "artid": "051701",
                "material": "publication",
                "journal_issue": "5",
                "journal_title": "head title",
                "journal_record": {
                    "$ref": "https://inspirehep.net/api/journals/1613970"
                },
                "journal_volume": "104",
            }
        ],
        "references": [
            {
                "reference": {
                    "label": "Capozziello and Laurentis, 2011",
                    "authors": [
                        {"full_name": "Laurentis, M.D.", "inspire_role": "author"}
                    ],
                    "publication_info": {
                        "year": 2011,
                        "page_start": "167",
                        "journal_title": "Phys.Rept.",
                        "journal_volume": "509"
                    },
                },
            }
        ],
    }
    update = {
        "authors": [{"full_name": "Elliott, Chris"}, {"full_name": "Gwilliam, Owen"}],
        "dois": [
            {
                "value": "10.1016/j.newast.2021.101678",
                "source": "Elsevier B.V.",
                "material": "publication",
            }
        ],
        "publication_info": [
            {
                "year": 2022,
                "artid": "051703",
                "material": "publication",
                "journal_issue": "10",
                "journal_title": "head title",
                "journal_record": {
                    "$ref": "https://inspirehep.net/api/journals/1613970"
                },
                "journal_volume": "105",
            }
        ],
        "references": [
            {
                "record": {"$ref": "https://inspirehep.net/api/literature/581605"},
                "reference": {
                    "curated": True,
                    "label": "Capozziello, 2002",
                    "authors": [
                        {"full_name": "Capozziello, S.", "inspire_role": "author"}
                    ],
                    "publication_info": {
                        "year": 2002,
                        "page_start": "483",
                        "journal_title": "Int.J.Mod.Phys.D",
                        "journal_record": {
                            "$ref": "https://inspirehep.net/api/journals/1613976"
                        },
                        "journal_volume": "11",
                    },
                },
            }
        ],
    }

    merged, conflict = merge(root, head, update)
    assert len(merged["publication_info"]) == 2
    assert len(merged["dois"]) == 2
    assert len(merged['references']) == 1
    assert len(conflict) == 1  # author delete


@patch(
    "inspire_json_merger.api.get_configuration",
    return_value=ErratumOnPublisherOperations,
)
def test_merging_erratum_doesnt_remove_fields(fake_get_config):
    root = {
        "authors": [{"full_name": "Test, Chris"}],
        "dois": [
            {
                "value": "10.1016/j.newast.2021.101676",
                "source": "Elsevier B.V.",
                "material": "publication",
            }
        ],
        "publication_info": [
            {
                "year": 2021,
                "artid": "051701",
                "material": "publication",
                "journal_issue": "5",
                "journal_title": "head title",
                "journal_record": {
                    "$ref": "https://inspirehep.net/api/journals/1613970"
                },
                "journal_volume": "104",
            }
        ],
        "references": [
            {
                "reference": {
                    "label": "Capozziello and Laurentis, 2011",
                    "authors": [
                        {"full_name": "Laurentis, M.D.", "inspire_role": "author"}
                    ],
                    "publication_info": {
                        "year": 2011,
                        "page_start": "167",
                        "journal_title": "Phys.Rept.",
                        "journal_volume": "509"
                    },
                },
            }
        ],
        'inspire_categories': [{'term': 'Lattice'}]
    }
    head = {
        "authors": [{"full_name": "Test, Chris"}],
        "dois": [
            {
                "value": "10.1016/j.newast.2021.101676",
                "source": "Elsevier B.V.",
                "material": "publication",
            }
        ],
        "publication_info": [
            {
                "year": 2021,
                "artid": "051701",
                "material": "publication",
                "journal_issue": "5",
                "journal_title": "head title",
                "journal_record": {
                    "$ref": "https://inspirehep.net/api/journals/1613970"
                },
                "journal_volume": "104",
            }
        ],
        "references": [
            {
                "reference": {
                    "label": "Capozziello and Laurentis, 2011",
                    "authors": [
                        {"full_name": "Laurentis, M.D.", "inspire_role": "author"}
                    ],
                    "publication_info": {
                        "year": 2011,
                        "page_start": "167",
                        "journal_title": "Phys.Rept.",
                        "journal_volume": "509"
                    },
                },
            }
        ],
        'inspire_categories': [{'term': 'Lattice'}]
    }
    update = {
        "authors": [{"full_name": "Elliott, Chris"}, {"full_name": "Gwilliam, Owen"}],
        "dois": [
            {
                "value": "10.1016/j.newast.2021.101678",
                "source": "Elsevier B.V.",
                "material": "publication",
            }
        ]
    }

    merged, conflict = merge(root, head, update)
    assert 'publication_info' in merged
    assert 'authors' in merged
    assert 'references' in merged
    assert 'inspire_categories' in merged
    assert len(merged["dois"]) == 2
