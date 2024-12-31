# Instructions How to Use.

1. gmail_multi_usr_bin.py   <-- This file will be sent to the /usr/local/bin/ folder so you can run gmail from the command line.>

2. gmail_ping_test.py       <-- This file must be in the same folder as gmail_multi.py and .env file to work.>  

This script will test the connections after you get your app password. # Change your name from Bob below in the script. Not below, but below on Line 39 and 40 in gmail_ping_test.py.

        # Get credentials from environment variables (BEST PRACTICE)
        # EMAIL_USER = os.getenv("EMAIL_USER_Bob")
        # EMAIL_PASS = os.getenv("EMAIL_PASS_Bob")

3. usr-bin.sh               <-- This script is to used for sending the gmail_multi_usr_bin.py to the /usr/local/bin/ folder so you can run gmail from the command line.>

4. how_to_use.md            <-- This is this file.>


**Making the Script Executable and Adding it to the PATH**

Here's how to make your script easily runnable from the terminal:

**Easy Step (macOS/Linux):**

Once you have your App Password and entered it into the .env file and also edit gmail_multi.py with the user and pass info entered. Now you can run the script with this command:

```bash
    python gmail_multi.py
```

## Using App Passwords (Recommended for accounts with 2-Step Verification)

1. Get your Google Less Secure Password first and enter the info into the gmail_multi_usr_bin.py file:

    A. Go to your Google Account's App Passwords page: https://myaccount.google.com/apppasswords
    B. Select "Mail" and "Other (Custom name)" from the dropdowns.
    C. Enter a name for the app (e.g., "Gmail CLI").
    D. Click "Generate".
    E. Use the generated 16-character password in your `.env` file instead of your regular Gmail password.

    **Note**: Keep this password secret and secure!

    For more information or support, please open an issue on the GitHub repository.

2. Enter the extra-bonus folder:
3. Then run the following command in the terminal. 

    This will also change the name from gmail_multi_usr_bin.py to gmail.

    ```bash
    bash usr-bin.sh
    ```
3. Refresh your terminal:

    ```bash
    source ~/.zshrc
    ```
4. Run this command in the terminal and the script gmail should work. 

    ```bash
    gmail
    ```

**Steps (macOS/Linux):**

1.  **Add Shebang:**

    *   At the very top of your `gmail_multi_usr_bin.py` file, add the following shebang line:

        ```bash
        #!/usr/bin/env python3
        ```

        This tells the system to use the Python 3 interpreter to run the script.

2.  **Make the Script Executable:**

    *   Use the `chmod` command in your terminal:

        ```bash
        chmod +x /path/to/your/gmail_multi_usr_bin.py
        ```

        Replace `/path/to/your/gmail_multi_usr_bin.py` with the actual path to your script.

3.  **Move to `/usr/local/bin/` (Recommended):**

    *   This directory is typically already in your `PATH`. Move your script there:

        ```bash
        sudo mv /path/to/your/todoist.py /usr/local/bin/todoist
        ```
        You are using `gmail` as the executable name for your script.
        If you have a `gmail` folder, you can move it to `/usr/local/bin` like so:

        ```bash
        sudo mv /path/to/your/gmail /usr/local/bin/
        ```
        Then create a symbolic link:
        ```bash
        sudo ln -s /usr/local/bin/gmail/gmail_multi_usr_bin.py /usr/local/bin/gmail
        ```

**Steps (Windows):**

1.  **Add .py Extension to PATHEXT:**

    1.  Search for "environment variables" in the Start Menu and select "Edit the system environment variables."
    2.  Click "Environment Variables...".
    3.  Under "System variables," select `PATHEXT` and click "Edit...".
    4.  Add `; .PY` to the end of the variable value (make sure there's a semicolon separating it from the previous entry).
    5.  Click "OK" on all open windows.

2.  **Move Script to a Directory in PATH:**

    *   You can move your `gmail_multi_usr_bin.py` script to a directory that's already in your `PATH` environment variable (e.g., `C:\Windows\System32`, but this is generally not recommended for user scripts).
    *   **Better:** Create a new directory for your scripts (e.g., `C:\Users\YourUserName\bin` or `C:\scripts`) and add that directory to your `PATH` environment variable (similar to how you edited `PATHEXT`).

**4. Running the Script**

After completing the steps above:

*   **macOS/Linux:**

    *   Open your terminal and simply type:

        ```bash
        gmail
        ```

*   **Windows:**

    *   Open a command prompt or PowerShell and type:

        ```powershell
        gmail_multi_usr_bin.py
        ```

        Or, if you followed the `PATHEXT` method, you can just type:

        ```bash
        gmail
        ```
