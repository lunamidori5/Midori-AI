import subprocess
import time

# Define the paths to the three folders:
windows_path = "windows"
winxlinux_temp_path = "winxlinux_temp"
server1_path = "server1"

def sync_folder(source, destination):
    """Syncs a source folder to a destination folder using rsync."""
    rsync_command = [
        "rsync",
        "-a",  # archive mode: preserves permissions, timestamps, etc.
        "-v",  # verbose output
        "-h",
        "-z",
        "--delete",  # delete files in destination that are not in source
        source + "/",  # trailing slash ensures directory contents are synced
        destination
    ]
    subprocess.run(rsync_command)

while True:
    # Sync "windows" to "winxlinux_temp"
    sync_folder(windows_path, winxlinux_temp_path)

    # Sync "server1" to "winxlinux_temp"
    sync_folder(server1_path, winxlinux_temp_path)

    time.sleep(2)  # Wait for 2 seconds before syncing again