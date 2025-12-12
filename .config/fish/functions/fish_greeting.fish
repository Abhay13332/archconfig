function fish_greeting
    echo -ne '\x1b[38;5;16m'  # Set colour to primary
    echo "          ___  _     _                 
         / _ \| |   | |                
        / /_\ \ |__ | |__   __ _ _   _ 
        |  _  | '_ \| '_ \ / _` | | | |
        | | | | |_) | | | | (_| | |_| |
        \_| |_/_.__/|_| |_|\__,_|\__, |
                                  __/ |
                                 |___/ "
    set_color normal
    fastfetch --key-padding-left 5
end
