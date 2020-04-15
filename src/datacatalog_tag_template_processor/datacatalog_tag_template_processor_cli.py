import argparse
import logging
import sys

from datacatalog_tag_template_processor import tag_template_datasource_processor


class DatacatalogTagTemplateProcessorCLI:

    @classmethod
    def run(cls, argv):
        cls.__setup_logging()

        args = cls._parse_args(argv)
        args.func(args)

    @classmethod
    def __setup_logging(cls):
        logging.basicConfig(level=logging.INFO)

    @classmethod
    def _parse_args(cls, argv):
        parser = argparse.ArgumentParser(description=__doc__,
                                         formatter_class=argparse.RawDescriptionHelpFormatter)

        subparsers = parser.add_subparsers()

        cls.add_tag_templates_cmd(subparsers)

        return parser.parse_args(argv)

    @classmethod
    def add_tag_templates_cmd(cls, subparsers):
        tag_templates_parser = subparsers.add_parser("tag-templates",
                                                     help="Tag Templates commands")

        tag_templates_subparsers = tag_templates_parser.add_subparsers()

        cls.add_create_tag_templates_cmd(tag_templates_subparsers)

        cls.add_delete_tag_templates_cmd(tag_templates_subparsers)

    @classmethod
    def add_delete_tag_templates_cmd(cls, subparsers):
        delete_tag_templates_parser = subparsers.add_parser('delete',
                                                            help='Delete Tag Templates from CSV')
        delete_tag_templates_parser.add_argument('--csv-file',
                                                 help='CSV file with Tag Templates information',
                                                 required=True)
        delete_tag_templates_parser.set_defaults(func=cls.__delete_tag_templates)

    @classmethod
    def add_create_tag_templates_cmd(cls, subparsers):
        create_tag_templates_parser = subparsers.add_parser('create',
                                                            help='Create Tag Templates from CSV')
        create_tag_templates_parser.add_argument('--csv-file',
                                                 help='CSV file with Tag Templates information',
                                                 required=True)
        create_tag_templates_parser.set_defaults(func=cls.__create_tag_templates)

    @classmethod
    def __create_tag_templates(cls, args):
        tag_template_datasource_processor.TagTemplateDatasourceProcessor(
        ).create_tag_templates_from_csv(file_path=args.csv_file)

    @classmethod
    def __delete_tag_templates(cls, args):
        tag_template_datasource_processor.TagTemplateDatasourceProcessor(
        ).delete_tag_templates_from_csv(file_path=args.csv_file)


def main():
    argv = sys.argv
    DatacatalogTagTemplateProcessorCLI.run(argv[1:] if len(argv) > 0 else argv)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
