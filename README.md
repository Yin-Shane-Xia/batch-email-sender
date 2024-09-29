
##
Note this auto-email sender needs to be used carefully.
* When sending email > 40, the email will likely be put to spam folder
* When sending email > 200, the account will likely be locked. But even so, from my personal observation, the email can still be sent out.



Example command (save results to file without sending email):
```
python launch.py --dataset_file ./data/Assemble-2024-edited.csv
```

Command to send email
```
python launch.py --dataset_file ./data/Assemble-2024-edited.csv --mode SENDEMAIL
```

## Core function
email_sender.py, send_gmail function is the core function

## How to set Gmail App Password
https://support.google.com/accounts/answer/185833?hl=en