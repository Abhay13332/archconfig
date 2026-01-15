# First argument: any command
complete -c hyprrun \
    -n '__fish_use_subcommand' \
    -a '(__fish_complete_command)'

# Remaining arguments: delegate to that command
complete -c hyprrun \
    -n 'not __fish_use_subcommand' \
    -a '(__fish_complete_subcommand)'
