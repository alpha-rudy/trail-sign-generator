#!/usr/bin/env python3

import os
import subprocess
from gooey import Gooey, GooeyParser

@Gooey(
    program_name="TSG Docker Runner",
    menu=[{
        'name': 'Help',
        'items': [{
            'type': 'AboutDialog',
            'menuTitle': 'About',
            'name': 'TSG Docker Runner',
            'description': 'A small GUI to run the TSG Docker image.',
            'version': '1.0',
        }]
    }]
)
def main():
    parser = GooeyParser(description="Run Docker with the TSG container")

    # Positional arguments
    parser.add_argument(
        "PWD",
        metavar="Working Directory ($PWD)",
        help="Select the working directory you want to mount into the container",
        widget="DirChooser",
    )

    parser.add_argument(
        "TRAIL_DIR",
        metavar="Trail Directory ($TRAIL_DIR)",
        help="Select the subdirectory (relative to the Working Directory) that contains the YAML file",
        widget="DirChooser",
    )

    parser.add_argument(
        "YAML_CONFIG",
        metavar="YAML Config ($YAML_CONFIG)",
        help="Select the YAML configuration file (inside the Trail Directory)",
        widget="FileChooser",
    )

    # Optional arguments
    parser.add_argument(
        "--docker_image",
        metavar="Docker Image",
        help="Docker image name to use",
        default="rudychung/tsg",
        required=False,
    )

    parser.add_argument(
        "--term",
        metavar="TERM Environment Variable",
        help="TERM environment variable for Docker container",
        default="xterm",
        required=False,
    )

    args = parser.parse_args()

    # Build up the Docker run command
    # The container will see /home/builder/workdir as the mount from $PWD
    # We combine the relative directory + yaml file for the final argument
    inside_yaml_path = os.path.join("/home/builder/workdir",
                                    os.path.relpath(args.TRAIL_DIR, args.PWD),
                                    os.path.basename(args.YAML_CONFIG))

    command = [
        "docker", "run",
        "--rm",
        "--user", "builder",
        "-v", f"{args.PWD}:/home/builder/workdir",
        "-e", f"TERM={args.term}",
        args.docker_image,
        inside_yaml_path
    ]

    print("Executing command:")
    print(" ".join(command))

    # Run the command
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
