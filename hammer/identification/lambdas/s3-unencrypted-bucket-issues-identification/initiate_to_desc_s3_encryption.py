import os
import logging

from library.logger import set_logging
from library.config import Config
from library.aws.utility import Sns


def lambda_handler(event, context):
    """ Lambda handler to initiate to find S3 bucket encryption """
    set_logging(level=logging.INFO)
    logging.debug("Initiating S3 encryption checking")

    try:
        sns_arn = os.environ["SNS_S3_ENCRYPT_ARN"]
        config = Config()

        if not config.s3Encrypt.enabled:
            logging.debug("S3 bucket encryption checking disabled")
            return

        logging.debug("Iterating over each account to initiate s3 encyption check")
        for account_id, account_name in config.s3Encrypt.accounts.items():
            payload = {"account_id": account_id,
                       "account_name": account_name,
                      }
            logging.debug(f"Initiating s3 encyption checking for '{account_name}'")
            Sns.publish(sns_arn, payload)
    except Exception:
        logging.exception("Error occurred while initiation of S3 encyption checking")
        return

    logging.debug("S3 encyption checking initiation done")
