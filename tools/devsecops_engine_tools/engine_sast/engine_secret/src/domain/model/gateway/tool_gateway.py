from abc import ABCMeta, abstractmethod


class ToolGateway(metaclass=ABCMeta):
    @abstractmethod
    def run_tool(self) -> str:
        "remote config"
    
    @abstractmethod
    def create_exclude_file(self) -> str:
        "remote config"

