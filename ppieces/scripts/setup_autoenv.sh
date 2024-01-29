#!/bin/zsh

setup_autoenv() {
    project_path=$1
    echo "echo \"󰚩  loading venv automatically 󰚩\"" > $project_path/.autoenv.sh
    echo -n "source ${project_path}/venv/bin/activate" >> $project_path/.autoenv.sh
    echo "echo \"󰚩  deactivating venv automatically 󰚩\"" > $project_path/.autoenv_leave.sh
    echo -n "if type deactivate >/dev/null 2>&1; then\n  deactivate\nfi" >> $project_path/.autoenv_leave.sh
    echo ".autoenv.sh" >> $project_path/.gitignore
    echo ".autoenv_leave.sh" >> $project_path/.gitignore
}

# get the first argument passed to the script as the project_path and call setup_autoenv
project_path=$1
setup_autoenv $project_path
