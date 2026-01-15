#!/bin/bash
# Check if we booted with the "gpu_mode=intel" flag
if grep -q "gpu_mode=intel" /proc/cmdline; then
   echo "env = AQ_DRM_DEVICES,/dev/dri/card0:/dev/dri/card1
env =LIBVA_DRIVER_NAME,iHD
env =VK_DRIVER_FILES,/usr/share/vulkan/icd.d/intel_icd.x86_64.json
env =__GLX_VENDOR_LIBRARY_NAME,mesa

" > ~/.config/hypr/hyprland-intel.conf
else
  echo "" > ~/.config/hypr/hyprland-intel.conf
fi
  