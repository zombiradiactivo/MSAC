from cx_Freeze import setup, Executable

base = None

executables = [
    Executable("Main_Main_V0.09.py", base=base, targetName="MSAC.exe")
]

setup(
    name="MSAC",
    options={"build_exe": {"include_files": [], "packages": []}},
    version="0.9",
    description="GUI for start Apache, FilezillaFTP, Minecraft Servers ",
    executables=executables
)
