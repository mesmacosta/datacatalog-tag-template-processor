import unittest
from unittest import mock

from datacatalog_tag_template_processor import datacatalog_tag_template_processor_cli


class DatacatalogTagTemplateProcessorCLITest(unittest.TestCase):

    def test_parse_args_invalid_subcommand_should_raise_system_exit(self):
        self.assertRaises(
            SystemExit,
            datacatalog_tag_template_processor_cli.DatacatalogTagTemplateProcessorCLI._parse_args,
            ['invalid-subcommand'])

    def test_run_no_args_should_raise_attribute_error(self):
        self.assertRaises(
            AttributeError,
            datacatalog_tag_template_processor_cli.DatacatalogTagTemplateProcessorCLI.run, None)

    @mock.patch('datacatalog_tag_template_processor.datacatalog_tag_template_processor_cli.'
                'tag_template_datasource_processor.'
                'TagTemplateDatasourceProcessor')
    def test_run_create_tag_templates_should_call_tag_template_creator(
        self, mock_tag_template_datasource_processor):  # noqa: E125

        datacatalog_tag_template_processor_cli.DatacatalogTagTemplateProcessorCLI.run(
            ['tag-templates', 'create', '--csv-file', 'test.csv'])

        tag_template_datasource_processor = mock_tag_template_datasource_processor.return_value
        tag_template_datasource_processor.create_tag_templates_from_csv.assert_called_once()
        tag_template_datasource_processor.create_tag_templates_from_csv.assert_called_with(
            file_path='test.csv')

    @mock.patch('datacatalog_tag_template_processor.datacatalog_tag_template_processor_cli.'
                'tag_template_datasource_processor.'
                'TagTemplateDatasourceProcessor')
    def test_run_delete_tag_templates_should_call_correct_method(
        self, mock_tag_template_datasource_processor):  # noqa: E125

        datacatalog_tag_template_processor_cli.DatacatalogTagTemplateProcessorCLI.run(
            ['tag-templates', 'delete', '--csv-file', 'test.csv'])

        tag_template_datasource_processor = mock_tag_template_datasource_processor.return_value
        tag_template_datasource_processor.delete_tag_templates_from_csv.assert_called_once()
        tag_template_datasource_processor.delete_tag_templates_from_csv.assert_called_with(
            file_path='test.csv')

    @mock.patch(
        'datacatalog_tag_template_processor.datacatalog_tag_template_processor_cli.'
        'DatacatalogTagTemplateProcessorCLI')
    def test_main_should_call_cli_run(self, mock_cli):
        datacatalog_tag_template_processor_cli.main()
        mock_cli.run.assert_called_once()
