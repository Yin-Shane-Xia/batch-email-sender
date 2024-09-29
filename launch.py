import csv
import time
import random
import datetime
from enum import Enum
from tqdm import tqdm
from absl import app, flags

from email_sender import EmailAccount, EmailContent, send_gmail

from dataset_assemble import AssembleDataset

FLAGS = flags.FLAGS


class ModeType(Enum):
    LOCAL = 0
    SENDEMAIL = 1


EMAIL_SUBJECT = "Assemble 2024 註冊信息 registration information"
SENDER_EMAIL_ADDRESS = ""
SENDER_EMAIL_PASSWORD = "" # In Gmail, create App Password

# Launcher flags.
flags.DEFINE_enum_class(
    "mode",
    ModeType.LOCAL,
    enum_class=ModeType,
    help=(
        "mode: [LOCAL, SENDEMAIL]." "LOCAL: local testing; SENDMAIL: send the emails"
    ),
)
flags.DEFINE_string(
    "dataset_file",
    None,
    help=("file path of input assemble dataset"),
)


def main(_):
    print("=" * 50)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    log_send_email = []

    sender_account = EmailAccount(
        email_address=SENDER_EMAIL_ADDRESS,
        password=SENDER_EMAIL_PASSWORD,
    )
    dataset = AssembleDataset(dataset_csv_file=FLAGS.dataset_file)

    print("Sending email ...")
    for participant in tqdm(dataset.participants):
        email_body = dataset.compose_single_email(participant)
        content = EmailContent(
            send_to=[participant.email],
            subject=EMAIL_SUBJECT,
            body=email_body,
            # files_paths=["/Users/shane/Downloads/2024北美靈糧青年特會手冊.pdf"],
        )
        log_send_email.append([participant.email, content.body])
        if FLAGS.mode == ModeType.SENDEMAIL:
            send_gmail(sender_account, content)

        ## Don't really need this, but to slow down and less likelly be sent to spam
        # random_timer = random.uniform(1, 3)
        # time.sleep(random_timer)


    with open(f"log-send-email-{timestamp}.csv", "w", encoding="utf-8") as fid:
        writer = csv.writer(fid)
        for log in log_send_email:
            writer.writerow(log)

    print("-" * 25 + "\nStats:")
    dataset.print_stats()
    print("=" * 50 + "\nSuccess!\n")


if __name__ == "__main__":
    app.run(main)
