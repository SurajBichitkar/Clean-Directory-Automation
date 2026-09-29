import sys
import schedule
import time
import os
import hashlib
import smtplib
from email.message import EmailMessage

def Send_Email(recevier_mail, body, Attachment):
    sender_mail = "your_mail@gmail.com"
    sender_password = "your_app_passward"

    msg = EmailMessage()
    msg["From"] = sender_mail
    msg["To"] = recevier_mail
    msg["Subject"] = "Duplicate file cleaner report."
    msg.set_content(body)

    fobj = open(Attachment,"rb")
    msg.add_attachment(fobj.read(),
                       maintype = 'application',
                       subtype = 'octet-stream',
                       filename = fobj.name)

    smpt = smtplib.SMTP_SSL("smpt.gmail.com", 465)
    smpt.login(sender_mail, sender_password)
    smpt.send_message(msg)
    smpt.quit()

    print("Email sent successfully!")
    

def CheckForDirectory(DirectoryPath):
    FileExists = os.path.exists(DirectoryPath)

    if not FileExists:
        raise FileNotFoundError(f"No such directory:{DirectoryPath}")
    if not os.path.isdir(DirectoryPath):
        raise NotADirectoryError(f"Not a directory:{DirectoryPath}")

def DirectoryLog():

    Border = "-"*40

    timestamp = time.ctime()

    LogfileName = "Report_%s.log"%(timestamp)
    LogfileName = LogfileName.replace(" ","_").replace(":","_")
    os.makedirs("Logs", exist_ok=True)
    LogfileName = os.path.join("Logs",LogfileName)

    fobj = open(LogfileName,"w")

    fobj.write(Border+"\n")
    fobj.write("Clean Directory Automation script \n")
    fobj.write(Border+"\n")

    fobj.close()

    return LogfileName

def CalculateCheckSum(FileName):
    
    fobj = open(FileName,"rb")

    hobj = hashlib.md5()

    Buffer = fobj.read(1000)

    while(len(Buffer) > 0):
        hobj.update(Buffer)
        Buffer = fobj.read(1000)

    fobj.close()

    return hobj.hexdigest()

def FindDuplicates(DirectoryPath,LogFile):

    Border = "-"*40

    Duplicate = {}
    count = 0

    if not os.path.isabs(DirectoryPath):
        DirectoryPath = os.path.abspath(DirectoryPath)


    fobj = open(LogFile,"a")
    fobj.write("Files in Directory " +DirectoryPath+ ":"+ "\n")
    fobj.write(Border +"\n")

    for FolderName, SubFolder, FileName in os.walk(DirectoryPath):
        for Fname in FileName:
            count += 1

            #Make path absolute if it is relative
            Fname = os.path.join(FolderName,Fname)

            #Write file name in log file
            fobj.write("File Name:" +Fname+ "\n")

            #Get Check Sum
            CheckSum = CalculateCheckSum(Fname)

            #Group files by check sum
            if CheckSum in Duplicate:
                Duplicate[CheckSum].append(Fname)
            else:
                Duplicate[CheckSum] = [Fname]

    fobj.write(Border +"\n")
    fobj.close()

    return Duplicate, count

def DeleteDuplicates(DirectoryPath):

    Border = "-"*40
    timestamp = time.ctime()

    LogFile = DirectoryLog()

    print("Log file created...!!!")

    Files, TotalFiles = FindDuplicates(DirectoryPath,LogFile)

    DuplicateFilesList = list(filter(lambda X: len(X)>1, Files.values()))

    fobj = open(LogFile,"a")

    fobj.write("Deleted files list:" + "\n")
    fobj.write(Border + "\n")
    DeletedFiles = 0

    #Delete duplicate files
    for value in DuplicateFilesList:
        for subvalue in value[1:]:
            fobj.write(subvalue + "\n")
            os.remove(subvalue)
            DeletedFiles += 1

    #Log summary
    fobj.write(Border + "\n")
    fobj.write("Total files scanned :" + str(TotalFiles) + "\n")
    fobj.write("Total files deleted :" + str(DeletedFiles) + "\n")

    fobj.write(Border + "\n")
    fobj.write("Log created at :" + timestamp + "\n")
    fobj.write(Border + "\n")

    fobj.close()

    return TotalFiles, len(DuplicateFilesList), DeletedFiles, LogFile


def CleanDirectory(DirectoryPath,Email):
    #Check for path exists as directory
    try:
        CheckForDirectory(DirectoryPath)
    except (FileNotFoundError,NotADirectoryError) as e:
        print(e)
        return

    starting_time = time.strftime("%d-%m-%Y %I:%M:%S %p")

    #Deletion operation starts here
    total_files, duplicate_found, deleted_files, Attachment = DeleteDuplicates(DirectoryPath)

    completion_time = time.strftime("%d-%m-%Y %I:%M:%S %p")

    body = f"""
              The duplicate file removal operation has been completed successfully.\n
              Opertaion Stactistics: \n
              Starting time of scanning: {starting_time} \n
              completion time of scanning: {completion_time} \n
              Total number of files scanned: {total_files} \n
              Total number of duplicate files found: {duplicate_found} \n        
              Total number of duplicate files deleted: {deleted_files} \n
              
              please find the detailed log file attached to this email.\n

              Regards,\n
              Automation System \n
           """

    Send_Email(Email,body,Attachment)


def main():
    Border = "-"*40

    print(Border)
    print("Automation Script")
    print(Border)

    if (len(sys.argv) == 3):
        if (sys.argv[1] == "--h" or sys.argv[1] == "--H"):
            print("This automation script is use to clean directory.")
            print("For better usage check --u flag.")
        elif (sys.argv[1] == "--u" or sys.argv[1] == "--U"):
            print("Please execute script as:")
            print("'python <File_Name.py> <Directory_path> <Interval_in_minutes> <Receiver_Email>'")
            print("Directory name should be absolute path.")
        else:
            schedule.every(sys.argv[2]).minute.do(CleanDirectory,sys.argv[1],sys.argv[3])

            while(True):
                schedule.run_pending()
                time.sleep(1)
    else:
        print("Invalid number of arguments...!!!")
        print("Please use --h and --u for more information.")

    print(Border)
    print("Thank you for using clean directory script...!!!")
    print(Border)
    
if __name__ == "__main__":
    main()