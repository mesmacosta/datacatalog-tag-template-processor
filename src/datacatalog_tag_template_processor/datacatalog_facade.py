import re

from google.cloud import datacatalog
from google.cloud import datacatalog_v1beta1


class DataCatalogFacade:
    """Data Catalog API communication facade."""

    def __init__(self):
        # Initialize the API client.
        self.__datacatalog = datacatalog.DataCatalogClient()

    def create_tag_template(self, project_id, location_id, tag_template_id, tag_template):
        return self.__datacatalog.create_tag_template(
            parent=datacatalog.DataCatalogClient.location_path(project_id, location_id),
            tag_template_id=tag_template_id,
            tag_template=tag_template)

    def delete_tag_template(self, name):
        self.__datacatalog.delete_tag_template(name=name, force=True)

    # Currently we don't have a list method, so we are using search which is not exhaustive,
    # and might not return some entries.
    def search_tag_templates(self, project_ids):
        scope = datacatalog_v1beta1.types.SearchCatalogRequest.Scope()

        scope.include_project_ids.extend(project_ids.split(','))

        query = 'type=TAG_TEMPLATE'

        results_iterator = self.__datacatalog.search_catalog(scope=scope,
                                                             query=query,
                                                             order_by='relevance',
                                                             page_size=1000)

        results = []
        for page in results_iterator.pages:
            results.extend(page)

        return results

    @classmethod
    def extract_resources_from_template(cls, tag_template_name):
        re_match = re.match(
            r'^projects[/]([_a-zA-Z-\d]+)[/]locations[/]'
            r'([a-zA-Z-\d]+)[/]tagTemplates[/]([@a-zA-Z-_\d]+)$', tag_template_name)

        if re_match:
            project_id, location_id, tag_template_id, = re_match.groups()
            return project_id, location_id, tag_template_id
