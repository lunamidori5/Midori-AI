import subprocess
import time

# Define the paths to the three folders:
windows_path = "windows"
winxlinux_temp_path = "winxlinux_temp"
server1_path = "server1"

def pre_sync_folder(source, destination):
    """Syncs a source folder to a destination folder using rsync."""
    rsync_command = [
        "rsync",
        "-r",
        "-v",  # verbose output
        "-h",
        "-z",
        source + "/",  # trailing slash ensures directory contents are synced
        destination
    ]
    subprocess.run(rsync_command)

def sync_folder(source, destination):
    """Syncs a source folder to a destination folder using rsync."""
    rsync_command = [
        "rsync",
        "-r",
        "-v",  # verbose output
        "-h",
        "-z",
        "--delete",  # delete files in destination that are not in source
        source + "/",  # trailing slash ensures directory contents are synced
        destination
    ]
    subprocess.run(rsync_command)

pre_sync_folder(windows_path, server1_path)
pre_sync_folder(server1_path, windows_path)

while True:
    sync_folder(server1_path, windows_path)
    sync_folder(windows_path, server1_path)
    

    time.sleep(2)  # Wait for 2 seconds before syncing again