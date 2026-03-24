# INET4031 Add Users Script and User List
## Program Description
This Python script automates the creation of users and groups to a Ubuntu system by passing in the information of those users from a create-users.input file. 

The goal of this script is to automate the account creation process, removing the lengthy process of manually adding users, setting passwords, and assigning them to groups. It does this by building the *adduser* and *passwd* commands typically used for these processes and has the system execute them.

## Input File Format
The create-users.input file follows a structure resembling the format used in the /etc/passwd file, storing one user per line with each field separated a colon. The Python script parses each line, extracts the user details from those parsed fields, and passes those details into the built *adduser* and *passwd* commands.

The order of these fields are *username*, *password*, *lastName*, *firstName*, *group*. For example, a line in the file could look something like:

>user01:pass01:Doe:John:group01

and the resulting commands built and executed by the script would be:
>/usr/sbin/adduser --disabled-password --gecos 'John Doe,,,' user01
>
>/bin/echo -ne 'pass01\npass01' | /usr/bin/sudo /usr/bin/passwd user01
>
>/usr/sbin/adduser user01 group01
>
Comments are also possible if you wish to skip lines for processing. These are made by adding a *#* char to the beginning of a line.

## Running the Script
To run the script:
1. Format the input file to match the description in the Input File Format section for each user.
2. Move to the script directory
   >cd ~/inet_4031_adduser_script
   >
3. You may need to change the Python file's permissions to be executable.
   >chmod +x create-user.py
   >
4. Run the command in the shell.
   >sudo ./create-users.py < createusers.input

If you wish to do a "dry run", **be sure to comment out *every* line containing** *"os.system(cmd)"* using a text editor. This is especially important since you do not want to accidentally add users to your system during your dry run that you'll end up having to delete. 

Alternatively, you can run the *create-users2.py* script and follow its prompts. Note that you *should not* redirect the input file when running the command.
   


