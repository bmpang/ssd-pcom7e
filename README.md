# Track Management

## About
This repository hosts the python code necessary to run our track management application. The app allows for artists to create and manage artifacts of copyrightable material related to their songs. Whether it is lyrics, audio, or a score, they can upload their work where it will be stored encrypted-at-rest while checksums verify data integrity and prevent reuse of others' work.

### External Libraries / Dependencies
We are using sqlite3 to mangage database interactions from within python, pyca/cryptography for AES-128 symmetric key encryption, and pwinput for user-friendly masked password inputs

### Run the application
Use Python3 to run src/app.py to run the application
