# RDS Encrypt
A tool used to encrypt RDS instances that were previously created in an unencrypted state 

Currently it is a strenuous process to encrypt an unencrypted RDS instance. This tool automates that process. It will even handle the process of creating an encryption key in AWS KMS should you not provide one to the script.


## The following actions are taken in your AWS account
 - Snapshot your desired instance
 - Name the snapshot
 - Copy the snapshot to the region your RDS instance currently exists in
 - Encrypt the snapshot on copy with an encryption key
 - Rename your instance to `"RDS-OLD"`
 - Create a new encrypted instance with the original name using the encrypted snapshot
 - point any Route 53 records pointing to the old endpoint to the new
 - Remove the old RDS instance (optional)

Where you once had an unencrypted RDS instance is a newly created, encrypted instance that is a replica of the original and all of the data held. 

## Getting Started
A dependency of this script is having the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) configured with your credentials in `~/.aws/credentials` 

```
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

Also we should configure our default region 

```
[default]
region=us-east-1
```

alternatively you can configure the AWS CLI by running the following
 
```
$ aws configure 
```

## Configuration parameters
Configure these environment variables before you execute the script
```
$ export VAR=VAL
```

 - RDS_INSTANCE
   - The identifier for your RDS instance example `"test-01"`
 - KMS_KEY (Optional)
    - If you have a KMS key you wish to use to encrypt your snapshot please reference the ID here. If not the program will create you a key called `"auto-gen-<random-string>"`
 - DELETE_OLD
    - If set to true your original unencrypted instance will be removed. 




