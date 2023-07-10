import re
from devsecops_engine_utilities.defect_dojo.infraestructure.\
    driver_adapters.cmdb import CmdbRestConsumer
from devsecops_engine_utilities.defect_dojo.domain.\
    request_objects.import_scan import ImportScanRequest
from devsecops_engine_utilities.utils.\
    validation_error import ValidationError
from devsecops_engine_utilities.utils.\
    logger_info import MyLogger
from devsecops_engine_utilities.azuredevops.\
    infrastructure.azure_devops_api import AzureDevopsApi

logger = MyLogger.__call__().get_logger()


class CmdbUserCase:
    def __init__(self, rest_consumer_cmdb: CmdbRestConsumer,
                 utils_azure: AzureDevopsApi,
                 expression) -> None:

        self.__rc_cmdb = rest_consumer_cmdb
        self.__utils_azure = utils_azure
        self.__expression = expression

    def execute(self, request: ImportScanRequest) -> ImportScanRequest:
        # Connection config map
        connection = self.__utils_azure.get_azure_connection()
        product_type_name_map = self.__utils_azure.get_remote_json_config(
            connection=connection,
            repository_id=request.repository_id,
            remote_config_path=request.remote_config_path)

        # regular exprecion
        request.code_app = self.get_code_app(request.engagement_name)

        # connect cmdb
        product_data = self.__rc_cmdb.get_product_info(request.code_app)
        request.product_type_name = product_type_name_map.get(
            product_data.product_type_name, product_data.product_type_name
        )
        request.product_name = product_data.product_name
        request.tags = product_data.tag_product
        request.product_description = product_data.product_description

        return request

    def get_code_app(self, engagement_name: str):
        m = re.search(self.__expression,
                      engagement_name, re.IGNORECASE)
        if m is None:
            logger.error(f"Engagement name {engagement_name} not match")
            raise ValidationError("Engagement name not match")
        code_app = m.group(1)
        logger.debug(code_app)
        return code_app.lower()

