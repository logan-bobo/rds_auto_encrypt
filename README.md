# RDS Encrypt 🔒

A tool used to encrypt RDS instances that were previously created in an unencrypted state

Currently it is a strenuous process to encrypt an unencrypted RDS instance. This tool automates that process.

## The following actions are taken in your AWS account

- Snapshot your desired instance
- Name the snapshot
- Copy the snapshot to the region your RDS instance currently exists in
- Encrypt the snapshot on copy with your encryption key
- Rename your instance to `"RDS-OLD"`
- Create a new encrypted instance with the original name using the encrypted snapshot
- point any Route 53 records pointing to the old endpoint to the new
- Remove the old RDS instance (optional)

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

## Configuration parameters

Configure these environment variables before you execute the script

```bash
export VAR=VAL
```

- RDS_INSTANCE
  - The identifier for your RDS instance example `"test-01"`
- KMS_KEY
  - The ID of the encryption key to be used to encrypt your instance. If you need to create a key please see the [following](<https://www.google.com/search?q=create+a+kms+key+aws&oq=create+a+kms+key+aws&aqs=chrome..69i57j0i22i30j69i60l2.5186j0j4&sourceid=chrome&ie=UTF-8>).
- DELETE_OLD
  - If set to true your original un-encrypted instance will be removed.
