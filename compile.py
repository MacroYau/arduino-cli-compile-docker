import datetime
import os
import subprocess
import sys
import yaml


def compile_sketch(spec):
    sketch = None
    board = None

    if "sketch" not in spec:
        print("Sketch file not specified, unable to compile")
        sys.exit(1)
    else:
        sketch = spec["sketch"]

    if "target" not in spec:
        print("Compilation target not specified, unable to compile")
        sys.exit(1)
    else:
        if "board" not in spec["target"]:
            print("Target board type not specified, unable to compile")
            sys.exit(1)
        else:
            board = spec["target"]["board"]
            print(f"Compiling {sketch} for board type {board}")
        if "url" in spec["target"]:
            _add_arduino_core_package_index(spec["target"]["url"])
        if "core" in spec["target"]:
            (core_name, core_version) = _parse_version(spec["target"]["core"])
            core_name_version = f"{core_name} v{core_version}" if core_version is not None else f"{core_name} (latest)"
            print(f"Installing core {core_name_version}... ", end="")
            success = _install_arduino_core(core_name, core_version)
            print("Done!" if success else "Failed!")
            if not success:
                sys.exit(1)

    if "libraries" in spec:
        for lib in spec["libraries"]:
            (lib_name, lib_version) = _parse_version(lib)
            lib_name_version = f"{lib_name} v{lib_version}" if lib_version is not None else f"{lib_name} (latest)"
            print(f"Installing library {lib_name_version}... ", end="")
            success = _install_arduino_lib(lib_name, lib_version)
            print("Done!" if success else "Failed!")
            if not success:
                sys.exit(1)

    output_path = sketch.split(".")[0]
    if "version" in spec:
        output_path += "_v" + spec["version"].replace(".", "_")
    build_date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path += "_" + build_date + "Z"
    output_path += ".bin"
    print(f"Sketch will be compiled to {output_path}...")

    success = _compile_arduino_sketch(sketch, board, output_path)
    print("Compilation completed!" if success else "Compilation failed!")


def _parse_version(line):
    if "==" in line:
        (name, version) = line.split("==", 1)
    else:
        (name, version) = (line.strip(), None)
    return (name, version)


def _add_arduino_core_package_index(url):
    return _run_shell_command(["arduino-cli", "core", "update-index", "--additional-urls", url])


def _install_arduino_core(name, version=None):
    core = f"{name}@{version}" if version is not None else name
    return _run_shell_command(["arduino-cli", "core", "install", core])


def _install_arduino_lib(name, version=None):
    lib = f"{name}@{version}" if version is not None else name
    return _run_shell_command(["arduino-cli", "lib", "install", lib])


def _compile_arduino_sketch(sketch_path, board, output_path):
    os.makedirs("dist/", exist_ok=True)
    return _run_shell_command(["arduino-cli", "compile",
                               "-b", board,
                               "-o", f"dist/{output_path}",
                               sketch_path], stdout=True)


def _run_shell_command(arguments, stdout=False, stderr=True):
    process = subprocess.run(arguments, check=True, capture_output=True)
    if stdout and len(process.stdout) > 0:
        print("> %s" % process.stdout.decode("utf-8"))
    if stderr and len(process.stderr) > 0:
        print("ERROR > %s" % process.stderr.decode("utf-8"))
    return (process.returncode == 0)


if __name__ == "__main__":
    try:
        f = open("project.yaml", "r")
        spec = yaml.safe_load(f)
        compile_sketch(spec)
        sys.exit(0)
    except IOError as e:
        print("Specification file project.yaml not found")
        sys.exit(1)
    except yaml.YAMLError as e:
        print("Something wrong with the syntax of project.yaml: %s" % e)
        sys.exit(1)
