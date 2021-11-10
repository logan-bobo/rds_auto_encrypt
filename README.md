# RDS_Encrypt
A tool used to encrypt RDS instances that were previously created with an unencrypted EBS volume

Currently it is a strenious process to encrypt an unencrypted RDS instance. This tool automates the process. It will even handle the process of creating an encryption key in AWS KMS should you not provide one to the script.


## The following actions are taken

 - Snapshot your desired instance
 - Name the snapshot
 - Copy the snapshot to the region your RDS instance currently exists in
 - Encrypt the snapshot on copy with a encryption key
 - Rename your instance to rds-old 
 - Create a new encrypted instance with the origonal name using the encrypted snapshot
 - point any Route 53 records pointing to the old endpoint to the new
 - Remove the old RDS instance

Where you once had an unencrypted RDS instance is a newly created, encrypted instance that is a replica of the origonal and all of the data held. 


