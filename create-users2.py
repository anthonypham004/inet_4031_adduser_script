#!/usr/bin/python3

# INET4031[
# Anthony Pham
# Data Created: 04/23/2026
# Date Last Modified: 04/23/2026

import os # Gives Python the ability to run OS commands
import re # Regular expressions, used here for matching strings to detect comment lines
import sys # Gives Python access to Linux-specific parameters and functions like stdin


def main():
    # Prompt the user to choose between dry-run and normal execution mode.
    # Dry-run mode runs the script without executing system commands, only previews them.
    mode = input("Would you like to run in dry-mode? (Y/N): ").strip().upper()
    dry_run = mode == 'Y'

    if dry_run:
        print("[DRY-RUN MODE] **System commands will not be executed.**\n") 
    with open('create-users.input') as f:
        for line in f:
            # Boolean value that's true if the line starts with a '#'. 
            # This marks the line as a comment, ignoring the contents for that line for processing.
            match = re.match("^#",line)

            # Cleans up each field in the line by clearing whitespace and removing the ':' delimiter used to separate each field,
            # and puts those fields in an array.
            fields = line.strip().split(':')

            # Continues this iteration of the for loop, skipping the rest of the for loop for this line if:
            # - 'match' is true, which signifies that this line starts with a '#' and should be treated as a comment and have its contents be ignored
            # - The length of the 'fields' array isn't exactly 5, meaning that there's too much or too little fields for processing 
            if match or len(fields) != 5:
                if dry_run:
                    if match:
                        print("[SKIPPED] Commented line was ignored: %s" % line.strip())
                    else:
                        print("[SKIPPED] Line skipped: expected 5 fields but received %d: %s" % (len(fields), line.strip()))
                continue

            # Extracts user details from the parsed fields and places them into their respective /etc/passwd fields:
            # field[0] = username, field[1] = password, field[3] = first name, and field[2] = last name.
            username = fields[0]
            password = fields[1]
            gecos = "%s %s,,," % (fields[3],fields[2])

            # Splits field 5 (groups) by comma to get a list of individual group names that the user could be assigned to. 
            groups = fields[4].split(',')

            # Updates on the automation status by printing to terminal that the account is being made for 'username'
            print("==> Creating account for %s..." % (username))
            # Builds the adduser command to create the account without asking for a password, and passes the gecos details and username as the arguments.
            cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos,username)

            # Shows the command to be executed to the terminal and has the system run that command.
            if dry_run:
                print("[DRY-RUN MODE] Would have executed: %s" % cmd)
            else:
                print(cmd)
                os.system(cmd)

            # Updates on the status, saying to the terminal that the password is being set for the account
            print("==> Setting the password for %s..." % (username))
            # Builds the passwd command to set the account's password. 'echo -ne' pipes the password twice (the second time is for the confirmation) into 'passwd'.
            # The sudo command is needed since passwd requires superuser privileges.
            cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password,password,username)

            # Shows the command to be executed to the terminal and has the system run that command.
            if dry_run:
                print("[DRY-RUN MODE] Would have executed: %s" % cmd)
            else:
                print(cmd)
                os.system(cmd)

            for group in groups:
                # A '-' in the groups field signifies that no additional groups are needed to be assigned to the user.
                # Anything else is treated as a group name and the user gets added to it.
                if group != '-':
                    print("==> Assigning %s to the %s group..." % (username,group))
                    cmd = "/usr/sbin/adduser %s %s" % (username,group)
                if dry_run:
                    print("[DRY-RUN MODE] Would have executed: %s" % cmd)
                else:
                    print(cmd)
                    os.system(cmd)

if __name__ == '__main__':
    main()


