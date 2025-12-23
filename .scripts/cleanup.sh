#!/usr/bin/env fish

set Target_dirs \
    ~/.config/variety/Downloaded \
    ~/.cache \
    ~/tmptasks/imgCache

# Clear entire cache directory
rm -rf $HOME/.cache/*

for TARGET_DIR in $Target_dirs
    # Safety check
    if not test -d $TARGET_DIR
        echo "Directory not found: $TARGET_DIR"
        continue
    end

    # Delete items older than 5 days
    find $TARGET_DIR -mindepth 1 -mtime +5 -exec rm -rf {} \;
end
echo "Cleanup completed."