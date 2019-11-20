#!/usr/bin/env python3

"""
AUTHORs: Anand Kanani and Dax Mickelson
PURPOSE: This script helps in SDA PoV configuration (fast forwarding)
REQUIREMENTS: DNAC, ISE, and WLC need to be accessible.
HOW TO USE:
1.  `docker pull dmickels/sdapov-fastforwardscripts:selfservelabs-latest`
2.  `docker stop fastforward`
3.  `docker run -i --tty --rm --name fastforward dmickels/sdapov-fastforwardscripts:selfservelabs-latest`
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
        a = input("\nWould you like to continue with this option? [y/n]")
        if a.lower() in ["yes", "y"]:
            break
        elif a.lower() in ["no", "n"]:
            input("Press ENTER to exit.")
            sys.exit(0)
        else:
            print("Input y or n.")


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
        print("POSTMAN COLLECTIONS:")
        count = 0
        for f in all_postman_collection_files:
            count += 1
            print(f"\t{count} - {f}")
    else:
        print("Warning: Could not find any Postman collections.")
        sys.exit(1)

    if len(all_postman_collection_files) == 1:
        selected_postman_collection_file = all_postman_collection_files[0]
        verify_continuation()
    else:
        while True:
            print("")
            try:
                a = int(
                    input(
                        f"Choose a collection to run: [1-{len(all_postman_collection_files)}] "
                    )
                )
                selected_postman_collection_file = all_postman_collection_files[a - 1]
                print(
                    f"\nYou selected the {selected_postman_collection_file} collection."
                )

                a = input("\nContinue with this collection? [y/n]")
                if a.lower() in ["yes", "y"]:
                    break
            except Exception as e:
                print(f"Invalid option.  Error: {e}")

    # search for postman environments and ask the user to choose one
    print("\n")
    all_postman_environment_files = [
        f
        for f in os.listdir(SCRIPT_WORK_DIR_POSTMAN)
        if os.path.isfile(os.path.join(SCRIPT_WORK_DIR_POSTMAN, f))
        and "postman_environment" in f
    ]
    if len(all_postman_environment_files) > 0:
        print("POSTMAN ENVIRONMENTS:")
        count = 0
        for f in all_postman_environment_files:
            count += 1
            print(f"\t{count} - {f}")
    else:
        print("Warning: Could not find any Postman environments.")
        sys.exit(1)

    if len(all_postman_environment_files) == 1:
        selected_postman_environment_file = all_postman_environment_files[0]
        verify_continuation()
    else:
        while True:
            print("")
            try:
                a = int(
                    input(
                        f"Select an environment: [1-len(all_postman_environment_files)] "
                    )
                )
                selected_postman_environment_file = all_postman_environment_files[a - 1]
                print(
                    f"\nYou selected the {selected_postman_collection_file} environment."
                )

                a = input("\nContinue with this environment? [y/n] ")
                if a.lower() in ["yes", "y"]:
                    break
            except Exception as e:
                print(f"Invalid option.  Error: {e}")

    # Now lets run the "newman"
    while True:
        print(
            f"\nSelected options:\n"
            f"\tPOSTMAN COLLECTION: {selected_postman_collection_file}\n"
            f"\tPOSTMAN ENVIRONMENT: {selected_postman_environment_file}\n"
        )
        a = input("\nFast forward the SDA PoV with these options? [y/n] ")
        if a.lower() in ["yes", "y"]:
            break
        elif a.lower() in ["no", "n"]:
            print("Exiting...")
            sys.exit(0)
        else:
            print("Input y or n.")

    print("\n\nExecuting newman now...\n")
    cmd = [
        f"newman run {os.path.join(SCRIPT_WORK_DIR_POSTMAN, selected_postman_collection_file)} "
        f"-e {os.path.join(SCRIPT_WORK_DIR_POSTMAN, selected_postman_environment_file)}"
    ]
    subprocess.call(cmd, shell=True)

    print("\n\nReview the output of the API calls to ensure they were all successful.\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
