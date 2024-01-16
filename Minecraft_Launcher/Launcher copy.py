import minecraft_launcher_lib
import subprocess
import sys

# Get latest version
latest_version = minecraft_launcher_lib.utils.get_latest_version()["release"]

# Get Minecraft directory
minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()

# Make sure, the latest version of Minecraft is installed
minecraft_launcher_lib.install.install_minecraft_version(latest_version, minecraft_directory)


login_data = "zombiradiactivo"

# Get Minecraft command
options = {
    "username": login_data["name"],
}
minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(latest_version, minecraft_directory, options)

# Start Minecraft
subprocess.run(minecraft_command)