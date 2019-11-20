#!/usr/bin/env python3

"""
AUTHORs: Anand Kanani and Dax Mickelson
PURPOSE: This script helps in SDA PoV configuration (fast forwarding)
REQUIREMENTS: DNAC, ISE, and WLC need to be accessible.
HOW TO USE: `docker run --rm --name sdapov-fastforward dmickels/sdapov-fastforwardscripts:selfservelabs-latest`
"""

import os
import sys
import subprocess

# critical variables are in uppercase
GIT_REPO_URL = "https://github.com/daxm/sdapov.git"
GIT_BRANCH = "selfservelabs"
SCRIPT_WORK_DIR = "/usr/src/app/sdapov/docker/fastforward"
SCRIPT_WORK_DIR_POSTMAN = f"{SCRIPT_WORK_DIR}/postman"

"""
Note: python3, node.js, newman are all presumed installed via the Dockerfile
"""


def verify_continuation():
    while True:
        a = input("\nWOULD YOU LIKE TO CONTINUE WITH THIS OPTION? [Y/N] ")
        if a.lower() in ["yes", "y"]:
            break
        elif a.lower() in ["no", "n"]:
            input("PRESS ENTER TO EXIT")
            sys.exit(0)
        else:
            print("ENTER EITHER YES/NO")


def main():
    # search for postman collections and ask the user to choose one
    print("\n")
    all_postman_collection_files = [
        f
        for f in os.listdir(SCRIPT_WORK_DIR_POSTMAN)
        if os.path.isfile(os.path.join(SCRIPT_WORK_DIR_POSTMAN, f))
        and "postman_collection" in f
    ]
    if len(all_postman_collection_files) > 0:
        print("==> THE FOLLOWING POSTMAN COLLECTIONS WERE FOUND.")
        count = 0
        for f in all_postman_collection_files:
            count += 1
            print(f"{count} - {f}")
    else:
        print("==> COULD NOT FIND ANY FILE THAT APPEAR TO BE A POSTMAN COLLECTION!")
        sys.exit(1)

    selected_postman_collection_file = ""

    if len(all_postman_collection_files) == 1:
        selected_postman_collection_file = all_postman_collection_files[0]
        verify_continuation()
    else:
        while True:
            print("")
            try:
                a = int(
                    input(
                        f"WHICH ONE WOULD YOU LIKE TO UTILIZE? [1-{len(all_postman_collection_files)}] "
                    )
                )
                selected_postman_collection_file = all_postman_collection_files[a - 1]
                print(
                    f"\nYOU HAVE SELECTED POSTMAN COLLECTION:- {selected_postman_collection_file}"
                )

                a = input("\nWOULD YOU LIKE TO CONTINUE WITH THIS OPTION? [Y/N] ")
                if a.lower() in ["yes", "y"]:
                    break
            except Exception as e:
                print(f"THAT'S NOT A VALID OPTION!.  Error: {e}")

    # search for postman environments and ask the user to choose one
    print("\n")
    all_postman_environment_files = [
        f
        for f in os.listdir(SCRIPT_WORK_DIR_POSTMAN)
        if os.path.isfile(os.path.join(SCRIPT_WORK_DIR_POSTMAN, f))
        and "postman_environment" in f
    ]
    if len(all_postman_environment_files) > 0:
        print("==> THE FOLLOWING POSTMAN ENVIRONMENTS WERE FOUND.")
        count = 0
        for f in all_postman_environment_files:
            count += 1
            print(f"{count} - {f}")
    else:
        print("==> COULD NOT FIND ANY FILE THAT APPEAR TO BE A POSTMAN ENVIRONMENT!")
        input("PRESS ENTER TO EXIT")
        sys.exit(0)

    selected_postman_environment_file = ""
    if len(all_postman_environment_files) == 1:
        selected_postman_environment_file = all_postman_environment_files[0]
        verify_continuation()
    else:
        while True:
            print("")
            try:
                a = int(
                    input(
                        f"WHICH ONE WOULD YOU LIKE TO UTILIZE? [1-len(all_postman_environment_files)] "
                    )
                )
                selected_postman_environment_file = all_postman_environment_files[a - 1]
                print(
                    f"\nYOU HAVE SELECTED POSTMAN ENVIRONMENT:- {selected_postman_collection_file}"
                )

                a = input("\nWOULD YOU LIKE TO CONTINUE WITH THIS OPTION? [Y/N] ")
                if a.lower() in ["yes", "y"]:
                    break
            except Exception as e:
                print(f"THAT'S NOT A VALID OPTION!, {e}")

    # Now lets run the "newman"
    while True:
        print(
            f"\n==> WITH THE FOLLOWING SELECTION?\nPOSTMAN COLLECTION - {selected_postman_collection_file}"
            f"\nPOSTMAN ENVIRONMENT - {selected_postman_environment_file}\n"
        )
        a = input("\nARE YOU READY TO FAST FORWARD YOUR SDA POV? [Y/N] ")
        if a.lower() in ["yes", "y"]:
            break
        elif a.lower() in ["no", "n"]:
            input("PRESS ENTER TO EXIT")
            sys.exit(0)
        else:
            print("ENTER EITHER YES/NO")

    print("\n\n==> EXECUTING NEWMAN NOW\n")
    cmd = [
        "newman",
        "run",
        os.path.join(SCRIPT_WORK_DIR_POSTMAN, selected_postman_collection_file),
        "-e",
        os.path.join(SCRIPT_WORK_DIR_POSTMAN, selected_postman_environment_file),
    ]
    subprocess.call(cmd, shell=True)
    """
    subprocess.run(cmd, stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    """

    print("\n\n==> IF ALL API CALLS WORKED IN THE ABOVE RUN THEN YOU ARE ALL SET.\n")
    input("PRESS ENTER TO EXIT")
    sys.exit(0)


if __name__ == "__main__":
    main()
