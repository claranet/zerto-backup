# Zerto ZVM Config backup

# Install

```
git clone git@github.com:claranet/zerto-backup.git
pip3 install -r requirements.txt
```

# Usage

```
usage: backup_zvm.py [-h] [--host HOST] [--username USERNAME] --password
                     PASSWORD [--output OUTPUT]

Create ZVM Configuratio Dump and download it

options:
  -h, --help           show this help message and exit
  --host HOST          Zerto ZVM Hostname
  --username USERNAME  ZVM Login Username
  --password PASSWORD  ZVM Login Password
  --output OUTPUT      Define file for output, use '-' for stdout, default
                       file <host>_<timestamp>.json
```

# Run with Docker

```
docker run -v $PWD:/backup claranet/zvm_backup [-h] [--host HOST] [--username USERNAME] --password PASSWORD [--output OUTPUT]
```
