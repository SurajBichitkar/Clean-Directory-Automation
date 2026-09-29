# 🧹 Clean Directory Automation

A Python-based automation tool that scans a directory for duplicate files, identifies duplicates using **MD5 checksums**, automatically removes duplicate files, generates a detailed log report, and sends the report to a specified email address.

The project is designed to automate directory cleanup and reduce unnecessary duplicate files without requiring manual inspection.

---

## 🚀 Features

* 🔍 **Duplicate File Detection**

  * Scans files recursively inside the selected directory.
  * Uses MD5 checksum/hash values to identify files with identical contents.

* 🗑️ **Automatic Duplicate Removal**

  * Keeps the first occurrence of a duplicate file.
  * Automatically deletes subsequent duplicate copies.

* 📝 **Automatic Log Generation**

  * Creates a `Logs` directory automatically.
  * Generates a timestamped `.log` file for every cleanup operation.
  * Stores scanned files, deleted files, and operation statistics.

* ⏰ **Scheduled Automation**

  * Allows the cleanup operation to run automatically at a specified interval.

* 📧 **Email Report**

  * Sends an email after the cleanup operation.
  * Attaches the generated log file to the email.
  * Includes operation statistics such as files scanned, duplicates found, and files deleted.

* ✅ **Directory Validation**

  * Checks whether the provided path exists.
  * Verifies that the provided path is actually a directory.

---

## 🛠️ Technologies Used

* **Python 3**
* `os` – File and directory operations
* `hashlib` – MD5 checksum calculation
* `schedule` – Scheduling automated tasks
* `smtplib` – Sending email reports
* `email.message` – Creating email messages
* `sys` – Handling command-line arguments
* File Handling – Creating and maintaining log files

---

## 📂 Project Structure

```text
Clean-Directory-Automation/
│
├── CleanDirectory.py
│
├── Logs/
│   └── Report_<timestamp>.log
│
└── README.md
```

The `Logs` directory is created automatically when the program runs.

---

## ⚙️ How It Works

The automation follows these steps:

```text
Start
  │
  ▼
Validate Directory Path
  │
  ▼
Scan Directory Recursively
  │
  ▼
Calculate MD5 Checksum
  │
  ▼
Group Files with Same Checksum
  │
  ▼
Identify Duplicate Files
  │
  ▼
Delete Duplicate Copies
  │
  ▼
Generate Log Report
  │
  ▼
Send Report Through Email
  │
  ▼
Wait for Next Scheduled Run
```

---

## 🔐 Duplicate Detection

The project uses the **MD5 hashing algorithm** to calculate a checksum for each file.

Files with the same checksum are grouped together and treated as duplicates.

```python
def CalculateCheckSum(FileName):
    fobj = open(FileName,"rb")

    hobj = hashlib.md5()

    Buffer = fobj.read(1000)

    while(len(Buffer) > 0):
        hobj.update(Buffer)
        Buffer = fobj.read(1000)

    fobj.close()

    return hobj.hexdigest()
```

The checksum allows the program to compare file contents rather than relying only on filenames.

---

## 🗑️ Duplicate Removal

When duplicate files are detected, the first file in each duplicate group is retained and the remaining copies are deleted.

```python
for value in DuplicateFilesList:
    for subvalue in value[1:]:
        os.remove(subvalue)
```

This helps reduce unnecessary storage consumption caused by duplicate files.

> ⚠️ **Warning:** Deleted duplicate files are removed using `os.remove()`. Make sure you select the correct directory before running the automation.

---

## 📝 Logging

A separate log file is generated for each cleanup operation.

The log contains information such as:

* Directory scanned
* Files scanned
* Files detected as duplicates
* Files deleted
* Operation timestamp
* Cleanup statistics

Example:

```text
----------------------------------------
Clean Directory Automation script
----------------------------------------
Files in Directory C:\Example:

File Name:C:\Example\file1.txt
File Name:C:\Example\file2.txt

----------------------------------------
Deleted files list:
----------------------------------------
C:\Example\file2.txt

----------------------------------------
Total files scanned :10
Total files deleted :1
----------------------------------------
```

---

## 📧 Email Reporting

After the cleanup operation is completed, the program sends an email containing the operation statistics and attaches the generated log file.

The report includes:

* Starting time
* Completion time
* Total files scanned
* Total duplicate files found
* Total duplicate files deleted
* Detailed log file attachment

Before using the email functionality, configure your email address and application password in the Python file.

```python
sender_mail = "your_mail@gmail.com"
sender_password = "your_app_passward"
```

> **Security:** Do not upload your real email password or app password to GitHub. Use environment variables or another secure configuration method for production use.

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/SurajBichitkar/Clean-Directory-Automation.git
```

### 2. Navigate to the Project

```bash
cd Clean-Directory-Automation
```

### 3. Install Required Package

The project uses the `schedule` package for task scheduling.

```bash
pip install schedule
```

The other modules used by the project are part of Python's standard library.

---

## ▶️ Usage

Run the program using:

```bash
python CleanDirectory.py <Directory_Path> <Interval_in_minutes> <Receiver_Email>
```

### Example

```bash
python CleanDirectory.py "C:\Users\Suraj\Downloads" 10 example@gmail.com
```

This will run the directory cleanup every **10 minutes** and send the generated report to the specified email address.

---

## 📖 Help

To display the help information:

```bash
python CleanDirectory.py --h <anything>
```

Example:

```bash
python CleanDirectory.py --h 10
```

---

## 📌 Usage Information

The program expects:

```text
Directory Path
Interval in Minutes
Receiver Email
```

Example:

```text
python CleanDirectory.py <Directory_Path> <Interval_in_minutes> <Receiver_Email>
```

The directory path should be provided as an absolute path.

---

## 💡 Example Use Cases

This automation can be useful for:

* 🗂️ Cleaning Downloads folders
* 💻 Removing duplicate files from computers
* 📁 Organizing large directories
* 💾 Reducing unnecessary storage usage
* 🔄 Automating periodic directory maintenance
* 📊 Generating automated cleanup reports

---

## 🔒 Safety Considerations

This project permanently deletes duplicate files using Python's `os.remove()` function.

Before running it on an important directory:

1. Create a backup of important files.
2. Test the program on a sample directory.
3. Verify the directory path.
4. Make sure duplicate files can safely be removed.

---

## 🔮 Future Improvements

Possible improvements for future versions:

* [ ] Add a confirmation mode before deleting files
* [ ] Add a `--dry-run` option to preview deletions
* [ ] Support configurable hash algorithms such as SHA-256
* [ ] Add a graphical user interface
* [ ] Add file-type filtering
* [ ] Add file size comparison before hashing
* [ ] Improve email configuration using environment variables
* [ ] Add exception handling for inaccessible files
* [ ] Add a configurable log directory
* [ ] Add a summary dashboard
* [ ] Package the project as an executable

---

## 🎯 Project Objective

The main objective of this project is to demonstrate how Python can be used to automate repetitive file-management tasks.

By combining **file handling, hashing, directory traversal, scheduling, logging, and email automation**, the project provides an automated solution for identifying and removing duplicate files.

---

## 👨‍💻 Author

**Suraj Bichitkar**

GitHub:
https://github.com/SurajBichitkar

---

## 📄 License

This project is created for educational and automation purposes.

You are free to modify and improve the project according to your requirements.
