#!/usr/bin/env python3

"""
AUTHORS: Anand Kanani and Dax Mickelson
PURPOSE: This script helps in SDA PoV configuration (fast forwarding)
REQUIREMENTS: DNAC, ISE, and WLC need to be accessible.
HOW TO USE:
1.  `docker pull dmickels/sdapov-fastforwardscripts:selfservelabs-latest`
2.  `docker stop fastforward`
3.  `docker run -i --tty --rm --name fastforward dmickels/sdapov-fastforwardscripts:selfservelabs-latest`
Note: python3, node.js, newman are all presumed installed via the Dockerfile
"""

import os
import sys
import subprocess

GIT_REPO_URL = "https://github.com/daxm/sdapov.git"
GIT_BRANCH = "selfservelabs"
SCRIPT_WORK_DIR = "/usr/src/app/sdapov/docker/fastforward"
SCRIPT_WORK_DIR_POSTMAN = f"{SCRIPT_WORK_DIR}/postman"
POSTMAN_COLLECTION_FILTER = "postman_collection"
POSTMAN_ENVIRONMENT_FILTER = "postman_environment"


def verify_continuation():
    while True:
        a = input("\nWould you like to continue with this option? [y/n] ")
        if a.lower() in ["yes", "y"]:
            break
        elif a.lower() in ["no", "n"]:
            print("Exiting...")
            sys.exit(0)
        else:
            print("Input y or n.")


def make_selection(postman_option):
    # search for postman collection/environment and ask the user to choose one
    postman_files = [
        f
        for f in os.listdir(SCRIPT_WORK_DIR_POSTMAN)
        if os.path.isfile(os.path.join(SCRIPT_WORK_DIR_POSTMAN, f))
        and postman_option in f
    ]
    if len(postman_files) > 0:
        print("Files:")
        count = 0
        for f in postman_files:
            count += 1
            print(f"\t{count} - {f}")
    else:
        print("Warning: Could not find any Postman files.")
        sys.exit(1)

    if len(postman_files) == 1:
        # There is only one option so just go with it.
        return postman_files[0]
    else:
        while True:
            try:
                a = int(input(f"Choose an option: [1-{len(postman_files)}] "))
                selected_postman_file = postman_files[a - 1]
                print(f"You selected the {selected_postman_file}.")
                # verify_continuation()
                return selected_postman_file

            except Exception as e:
                print(f"Invalid option.  Error: {e}")


def main():
    # search for postman collections and ask the user to choose one
    selected_postman_collection_file = make_selection(postman_option=POSTMAN_COLLECTION_FILTER)

    # search for postman environments and ask the user to choose one
    selected_postman_environment_file = make_selection(postman_option=POSTMAN_ENVIRONMENT_FILTER)

    # Now lets run the "newman"
    print(
        f"Time to run fast forward scripts.\n"
        f"\tPOSTMAN COLLECTION: {selected_postman_collection_file}\n"
        f"\tPOSTMAN ENVIRONMENT: {selected_postman_environment_file}\n"
    )
    verify_continuation()

    print("Executing API calls now...")
    cmd = [
        f"newman run {os.path.join(SCRIPT_WORK_DIR_POSTMAN, selected_postman_collection_file)} "
        f"-e {os.path.join(SCRIPT_WORK_DIR_POSTMAN, selected_postman_environment_file)}"
    ]
    subprocess.call(cmd, shell=True)

    print("\n\nReview the output of the API calls to ensure they were all successful.")
    sys.exit(0)


if __name__ == "__main__":
    main()
