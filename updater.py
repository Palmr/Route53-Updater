#!/usr/bin/env python
import logging
from logging.handlers import TimedRotatingFileHandler
import ipgetter
import boto3

def createLogger():
  """
  Sets up logging
  """
  log_file = '/home/nick/Documents/code/DNS-update/updater.log'

  formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

  logger = logging.getLogger('DNS-updater')
  logger.setLevel(logging.DEBUG)
  file_logger = TimedRotatingFileHandler(log_file,
                                         when="w0",
                                         interval=1,
                                         backupCount=5)
  file_logger.setLevel(logging.INFO)
  file_logger.setFormatter(formatter)
  logger.addHandler(file_logger)
  
  console = logging.StreamHandler()
  console.setLevel(logging.DEBUG)
  console.setFormatter(formatter)
  logger.addHandler(console)

  return logger

def main():
  """
  Update IP on route53
  """
  logger = createLogger()

  current_ip = ipgetter.myip()
  logger.info('Current IP: %s', current_ip)

  # Hosted Zone => Domain List
  domains_to_update = {'palmr.me.': ['palmr.me.', 'git.palmr.me.']}

  client = boto3.client('route53')

  # Get HostedZone IDs
  for hosted_zone in client.list_hosted_zones_by_name()['HostedZones']:
    if hosted_zone['Name'] in domains_to_update:
      logger.debug('Hosted Zone found: %s', hosted_zone['Name'])
      change_batch = {'Comment': 'Refreshing IP', 'Changes': []}
      for record_set in client.list_resource_record_sets(HostedZoneId=hosted_zone['Id'])['ResourceRecordSets']:
        if record_set['Name'] in domains_to_update[hosted_zone['Name']] and record_set['Type'] == 'A' and record_set['ResourceRecords'][0]['Value'] != current_ip:
          logger.info('Updating: %s :: old=%s new=%s', record_set['Name'], record_set['ResourceRecords'][0]['Value'], current_ip)
          change = {'Action': 'UPSERT', 'ResourceRecordSet': record_set}
          change['ResourceRecordSet']['ResourceRecords'][0]['Value'] = current_ip
          change_batch['Changes'].append(change)
      # Only apply changes if there were any
      if len(change_batch['Changes']) > 0:
        response = client.change_resource_record_sets(HostedZoneId=hosted_zone['Id'], ChangeBatch=change_batch)
        logger.info('Update Response: %s', response)
      else:
        logger.debug('Hosted Zone already up to date')

if __name__ == '__main__':
  main()

