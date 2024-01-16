from cx_Freeze import setup, Executable

base = None

executables = [
    Executable("Main_Main_V0.05 compilar.py", base=base, targetName="Test.exe")
]

setup(
    name="Test",
    options={"build_exe": {"include_files": [], "packages": []}},
    version="0.2",
    description="Test 1",
    executables=executables
)