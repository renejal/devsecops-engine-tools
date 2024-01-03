import argparse
import sys
from devsecops_engine_tools.engine_core.src.domain.usecases.break_build import (
    BreakBuild,
)
from devsecops_engine_tools.engine_core.src.domain.usecases.handle_scan import (
    HandleScan,
)
from devsecops_engine_utilities.utils.printers import (
    Printers,
)


def get_inputs_from_cli(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("--remote_config_repo", type=str, required=True, help="")
    parser.add_argument(
        "--tool",
        choices=["engine_iac", "engine_dast", "engine_secret", "engine_dependencies","engine_container"],
        type=str,
        required=True,
        help="",
    )
    parser.add_argument(
        "--environment", choices=["dev", "qa", "pdn"], type=str, required=True, help=""
    )
    parser.add_argument(
        "--use_secrets_manager",
        choices=["true", "false"],
        type=str,
        required=False,
        help="",
    )
    parser.add_argument(
        "--use_vulnerability_management",
        choices=["true", "false"],
        type=str,
        required=False,
        help="",
    )
    parser.add_argument("--token_cmdb", required=False, help="")
    parser.add_argument("--token_vulnerability_management", required=False, help="")
    parser.add_argument("--scanner", required=False, help="")

    args = parser.parse_args()
    return {
        "remote_config_repo": args.remote_config_repo,
        "tool": args.tool,
        "scanner": args.scanner,
        "environment": args.environment,
        "use_secrets_manager": args.use_secrets_manager,
        "use_vulnerability_management": args.use_vulnerability_management,
        "token_cmdb": args.token_cmdb,
        "token_vulnerability_management": args.token_vulnerability_management,
    }


def init_engine_core(
    vulnerability_management_gateway: any,
    secrets_manager_gateway: any,
    devops_platform_gateway: any,
    print_table_gateway: any,
):
    Printers.print_logo_tool()
    args = get_inputs_from_cli(sys.argv[1:])
    instance = HandleScan(
        vulnerability_management_gateway,
        secrets_manager_gateway,
        devops_platform_gateway,
        dict_args=args,
    )
    findings_list, input_core = instance.process()
    BreakBuild(
        devops_platform_gateway,
        print_table_gateway,
        findings_list=findings_list,
        input_core=input_core,
    )
