import subprocess
import os

from devsecops_engine_tools.engine_sast.engine_secret.src.domain.model.gateway.tool_gateway import ToolGateway


class TrufflehogRun(ToolGateway):
    def __init__(self, trufflehog_path: str):
        self.trufflehog_path = trufflehog_path
    
    def create_exclude_file(self):
        path = os.environ.get('AGENT_WORKFOLDER')
        command = (
            f'echo .git >> {path}/excludedPath.txt'
        )
        subprocess.run(command, shell=True, check=True) 
        
    def run_tool(self, exclude_path):
        repository = os.environ.get('SYSTEM_DEFAULTWORKINGDIRECTORY')
        exclude_path = os.environ.get('AGENT_WORKFOLDER') + "/excludedPath.txt"
        command = (
            f"trufflehog filesystem {repository} --json --exclude-paths {exclude_path} --no-verification"
        )
        print(command)
        result = subprocess.run(command, capture_output=True, shell=True)
        output = result.stdout.strip()
        error = result.stderr.strip()
        # print(output)
        # print("ERROR")
        # print(error)
        # TODO revisar el stderr para manejo de excepciones.
        return output