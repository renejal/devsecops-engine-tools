import yaml
import subprocess
from engine_sast.engine_iac.src.domain.model.gateways.tool_gateway import ToolGateway
from engine_sast.engine_iac.src.infrastructure.driven_adapters.checkovTool.CheckovConfig import CheckovConfig


class CheckovTool(ToolGateway):
    CHECKOV_PACKAGE = "checkov"
    CHECKOV_CONFIG_FILE = "checkov_config.yaml"

    def __init__(self, checkov_config: CheckovConfig):
        self.checkov_config = checkov_config

    def create_config_file(self):
        with open(
            self.checkov_config.path_config_file + self.checkov_config.config_file_name + self.CHECKOV_CONFIG_FILE, "w"
        ) as file:
            yaml.dump(self.checkov_config.dict_confg_file, file)
            file.close()

    def run_tool(self):
        cmd = [
            "checkov",
            "--config-file",
            self.checkov_config.path_config_file + self.checkov_config.config_file_name + self.CHECKOV_CONFIG_FILE,
        ]
        result = subprocess.run(
            cmd,
            capture_output=True,
            shell=True,
        )
        return result.stdout.decode()
