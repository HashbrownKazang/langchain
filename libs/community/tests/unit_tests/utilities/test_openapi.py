import unittest
from typing import TYPE_CHECKING
from unittest.mock import patch

import pytest

if TYPE_CHECKING:
    from openapi_pydantic import Info, Reference, Schema

from langchain_community.utilities.openapi import OpenAPISpec


class OpenAPISpecTestCase(unittest.TestCase):
    @pytest.mark.requires("openapi-pydantic")
    def setUp(self) -> None:
        self.instance = OpenAPISpec(info=Info(title="test", version="1.0.0"))

    @patch("langchain_community.utilities.openapi.OpenAPISpec.get_referenced_schema")
    @pytest.mark.requires("openapi-pydantic")
    def test_get_root_referenced_schema_with_obj_ref(self, mock_get_referenced_schema):  # type: ignore[no-untyped-def]
        address_schema = Schema()
        address_schema.properties = {
            "address": Reference(ref="#/components/schemas/Address")
        }

        address_ref_schema = Schema()
        address_ref_schema.properties = {
            "street": Schema(),
            "city": Schema(),
            "state": Schema(),
        }

        mock_get_referenced_schema.side_effect = [address_schema, address_ref_schema]
        ref = Reference(ref="#/components/schemas/Pet")
        result = self.instance._get_root_referenced_schema(ref)
        self.assertIsInstance(result.properties["address"], Schema)

    @patch("langchain_community.utilities.openapi.OpenAPISpec.get_referenced_schema")
    @pytest.mark.requires("openapi-pydantic")
    def test_get_root_referenced_schema_obj_arr_ref(self, mock_get_referenced_schema):  # type: ignore[no-untyped-def]
        hobby_schema = Schema()
        hobby_schema.properties = {"hobby": Reference(ref="#/components/schemas/Hobby")}

        hobby_ref_schema = Schema()
        hobby_ref_schema.properties = {"name": Schema()}

        mock_get_referenced_schema.side_effect = [hobby_schema, hobby_ref_schema]
        ref = Reference(ref="#/components/schemas/Pet")
        result = self.instance._get_root_referenced_schema(ref)
        self.assertIsInstance(result.properties["hobby"], Schema)


if __name__ == "__main__":
    unittest.main()
