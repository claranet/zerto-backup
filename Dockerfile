FROM python:3-slim

LABEL description="Create and save Zerto ZVM Backups" \
      author="Martin Weber <martin.weber@de.clara.net>" \
      version="0.1.0"

VOLUME /backup
WORKDIR /backup

COPY requirements.txt /tmp
COPY ./backup_zvm.py /usr/local/bin/backup_zvm

RUN pip3 install -r /tmp/requirements.txt

ENTRYPOINT [ "python3", "/usr/local/bin/backup_zvm" ]
CMD [ ]
