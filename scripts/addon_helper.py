import os
import sys
import re
import time
import zipfile
import shutil
import bpy


def zip_addon(addon):
    bpy_module = re.sub(".py", "", os.path.basename(os.path.realpath(addon)))
    zfile = os.path.realpath(bpy_module + ".zip")

    print("Zipping addon - {0}".format(bpy_module))

    zf = zipfile.ZipFile(zfile, "w")
    if os.path.isdir(addon):
        for dirname, subdirs, files in os.walk(addon):
            zf.write(dirname)
            for filename in files:
                zf.write(os.path.join(dirname, filename))
    else:
        zf.write(addon)
    zf.close()
    return (bpy_module, zfile)


def copy_addon(bpy_module, zfile):
    print("Copying addon - {0}".format(bpy_module))

    if (2, 80, 0) < bpy.app.version:
        bpy.ops.preferences.addon_install(overwrite=True, filepath=zfile)
        bpy.ops.preferences.addon_enable(module=bpy_module)
    else:
        bpy.ops.wm.addon_install(overwrite=True, filepath=zfile)
        bpy.ops.wm.addon_enable(module=bpy_module)


def cleanup(addon, bpy_module):
    print("Cleaning up - {}".format(bpy_module))
    if (2, 80, 0) < bpy.app.version:
        bpy.ops.preferences.addon_disable(module=bpy_module)
        
        # addon_remove does not work correctly in CLI
        # bpy.ops.preferences.addon_remove(module=bpy_module)
        addon_dirs = bpy.utils.script_paths(subdir="addons")
        addon = os.path.join(addon_dirs[-1], addon)
        if os.path.isdir(addon):
            time.sleep(0.1)  # give some time for the disable to take effect
            shutil.rmtree(addon)
        else:
            os.remove(addon)
    else:
        bpy.ops.wm.addon_disable(module=bpy_module)

        # addon_remove does not work correctly in CLI
        # bpy.ops.wm.addon_remove(bpy_module=bpy_module)
        addon_dirs = bpy.utils.script_paths(subdir="addons")
        addon = os.path.join(addon_dirs[-1], addon)
        if os.path.isdir(addon):
            time.sleep(0.1)  # give some time for the disable to take effect
            shutil.rmtree(addon)
        else:
            os.remove(addon)


def get_version(bpy_module):
    mod = sys.modules[bpy_module]
    return mod.bl_info.get("version", (-1, -1, -1))
