# RDS Auto Encrypt 🔒

![CI](https://github.com/logan-bobo/rds_auto_encrypt/actions/workflows/python-app.yml/badge.svg)

A tool used to encrypt RDS instances that were previously created in an unencrypted state

Currently it is a strenuous process to encrypt an unencrypted RDS instance. This tool automates that process.

## The following actions are taken in your AWS account

- Snapshot your desired instance
- Name the snapshot
- Copy the snapshot to the region your RDS instance currently exists in
- Encrypt the snapshot on copy with your encryption key
- Rename your instance to `"RDS-OLD"`
- Create a new encrypted instance with the original name using the encrypted snapshot
- Remove the old instance

Where you once had an unencrypted RDS instance is a newly created, encrypted instance that is a replica of the original and all of the data held.

## Getting Started

A dependency of this script is having the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) configured with your credentials in `~/.aws/credentials`

```bash
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

Also we should configure our default region

```bash
[default]
region=us-east-1
```

alternatively you can configure the AWS CLI by running the following

```bash
aws configure
```

## Script Arguments

The following arguments can be passed to the script to set your desired instance and KMS key.

- `-instance` the RDS instance you wish to execute the script against
- `-keyid` the KMS key you wish to use to encrypt your instance with
- `-h, --help` help for the tool

## Running the script

Frist ensure that the file is executable on your system 
```bash 
$ chmod ug+x test_rds_encrypt.py
```

Now you are able to execute the script 
```
$ ./rds_encrypt.py --instance <instance> --keyis <keyid>
```
