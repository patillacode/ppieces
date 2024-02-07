from ppieces.utils.commands import (
    create_virtual_environment,
    initial_commit,
    initialize_git_repository,
    install_precommit_hooks,
    setup_autoenv,
)
from ppieces.utils.copy import (
    copy_main_file,
    copy_makefile,
    copy_precommit_config,
    copy_ruff_config,
)


def setup_project(
    project_path,
    options,
    username,
):
    options_mapping = {
        "virtual_env": create_virtual_environment,
        "git": initialize_git_repository,
        "autoenv": setup_autoenv,
        "ruff": copy_ruff_config,
        "pre_commit": copy_precommit_config,
        "makefile": copy_makefile,
    }

    copy_main_file(project_path)

    # we need to pop the pip_tools option from the options dict
    # because it's not a function that we can call directly
    # pip_tools is a flag that we need to pass for the virtual_env and makefile options
    pip_tools = options.pop("pip_tools")

    for option, value in options.items():
        if value:
            if option == "git":
                options_mapping[option](project_path, username)
            elif option == "virtual_env" or option == "makefile":
                options_mapping[option](project_path, pip_tools)
            else:
                options_mapping[option](project_path)


def finalize_project(project_path, git, pre_commit):
    if pre_commit:
        install_precommit_hooks(project_path)

    # this should be the last step since we are making the initial commit
    # AFTER all the template files are copied to the new project folder
    if git:
        initial_commit(project_path)
