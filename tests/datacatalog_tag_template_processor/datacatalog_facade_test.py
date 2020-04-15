import unittest
from unittest import mock

from datacatalog_tag_template_processor import datacatalog_facade


class DataCatalogFacadeTest(unittest.TestCase):

    @mock.patch(
        'datacatalog_tag_template_processor.datacatalog_facade.datacatalog.DataCatalogClient')
    def setUp(self, mock_datacatalog_client):
        self.__datacatalog_facade = datacatalog_facade.DataCatalogFacade()
        # Shortcut for the object assigned to self.__datacatalog_facade.__datacatalog
        self.__datacatalog_client = mock_datacatalog_client.return_value

    def test_constructor_should_set_instance_attributes(self):
        self.assertIsNotNone(self.__datacatalog_facade.__dict__['_DataCatalogFacade__datacatalog'])

    def test_create_tag_template_should_succeed(self):
        self.__datacatalog_facade.create_tag_template('test-project', 'location-id',
                                                      'tag_template_id', {})

        datacatalog = self.__datacatalog_client
        self.assertEqual(1, datacatalog.create_tag_template.call_count)

    def test_delete_tag_template_should_succeed(self):
        self.__datacatalog_facade.delete_tag_template('tag_template_name')

        datacatalog = self.__datacatalog_client
        self.assertEqual(1, datacatalog.delete_tag_template.call_count)

    def test_search_tag_templates_should_return_values(self):
        result_iterator = MockedObject()

        entry = MockedObject()
        entry.name = 'template_1'

        entry_2 = MockedObject()
        entry_2.name = 'template_2'

        expected_return_value = [entry, entry_2]

        # simulates two pages
        result_iterator.pages = [[entry], [entry_2]]

        datacatalog = self.__datacatalog_client
        datacatalog.search_catalog.return_value = result_iterator

        return_value = self.__datacatalog_facade.search_tag_templates('my-project1,my-project2')

        self.assertEqual(1, datacatalog.search_catalog.call_count)
        self.assertEqual(expected_return_value, return_value)

    def test_extract_resources_from_template_should_return_values(self):
        resource_name = 'projects/my-project/locations/us-central1/tagTemplates/my-template'

        project_id, location_id, tag_template_id = \
            self.__datacatalog_facade.extract_resources_from_template(resource_name)

        self.assertEqual('my-project', project_id)
        self.assertEqual('us-central1', location_id)
        self.assertEqual('my-template', tag_template_id)


class MockedObject(object):

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]
