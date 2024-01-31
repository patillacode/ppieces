#!/bin/bash

setup_autoenv() {
    project_path=$1

    # check if the project_path is given and is an existing directory
    if [[ -z $project_path ]]; then
        echo "Please provide a project path"
        exit 1
    elif [[ ! -d $project_path ]]; then
        echo "The project path provided is not a directory"
        exit 1
    fi

    echo "echo \"󰚩  loading venv automatically 󰚩\"" > $project_path/.autoenv.sh
    echo -e "source ${project_path}/venv/bin/activate" >> $project_path/.autoenv.sh
    echo "echo \"󰚩  deactivating venv automatically 󰚩\"" > $project_path/.autoenv_leave.sh
    echo -e "if type deactivate >/dev/null 2>&1; then\\n  deactivate\\nfi" >> $project_path/.autoenv_leave.sh
    echo ".autoenv.sh" >> $project_path/.gitignore
    echo ".autoenv_leave.sh" >> $project_path/.gitignore
}

# get the first argument passed to the script as the project_path and call setup_autoenv
project_path=$1
setup_autoenv $project_path
