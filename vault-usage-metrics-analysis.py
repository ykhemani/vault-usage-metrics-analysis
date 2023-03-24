#!/usr/bin/env python3

version = '0.0.4'

import argparse
import logging
from os import path
import sys
import json
import csv

help_indent_formatter = lambda prog: argparse.RawTextHelpFormatter(
  prog,
  max_help_position=4, 
  indent_increment=2,
  width=80
)

if __name__ == '__main__':

  parser = argparse.ArgumentParser(
    formatter_class=help_indent_formatter,
    description = 'vault-usage-metrics-analysis.py provides an analysis of your Vault usage metrics.',
  )

  parser.add_argument(
    '--input', '-input',
    help = 'File containing usage metrics in JSON format.',
    required = True
  )

  parser.add_argument(
    '--output', '-output',
    help = 'File to write usage metrics in CSV format.',
    required = True
  )

  parser.add_argument(
    '--log_level', '-log_level',
    #action = env_default('LOG_LEVEL'),
    help = 'Optional: Log level. Default: INFO.',
    choices = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
    required = False
  )

  parser.add_argument(
    '--version', '-version', '-v',
    help='Show version and exit.',
    action='version',
    version=f"{version}"
  )

  args = parser.parse_args()

  # logging
  format = "%(asctime)s: %(message)s"
  date_format = "%Y-%m-%d %H:%M:%S %Z"
  logging.basicConfig(format=format, level=logging.INFO, datefmt=date_format)

  if args.log_level == 'CRITICAL':
    logging.getLogger().setLevel(logging.CRITICAL)
  elif args.log_level == 'ERROR':
    logging.getLogger().setLevel(logging.ERROR)
  elif args.log_level == 'WARNING':
    logging.getLogger().setLevel(logging.WARNING)
  elif args.log_level == 'INFO':
    logging.getLogger().setLevel(logging.INFO)
  elif args.log_level == 'DEBUG':
    logging.getLogger().setLevel(logging.DEBUG)

  logging.debug("Log level set to %s", args.log_level)
  logging.debug("Starting %s", path.basename(__file__))

  try:
    json_file = args.input
    logging.debug("json_file: %s", json_file)
  except Exception as e:
    logging.error(e)
    logging.error('[error]: JSON file not specified.')
    sys.exit(1)

  try:
    f = open(json_file)
    data = json.load(f)['data']
    # print(data['data'])
    # sys.exit(7)
    with open(args.output, 'w', newline='') as output:
      csvwriter = csv.writer(output, delimiter=',')
      for namespace_data in data['by_namespace']:
        namespace_path = namespace_data['namespace_path']
        namespace_id = namespace_data['namespace_id']
        clients = namespace_data['counts']['clients']
        entities = namespace_data['counts']['distinct_entities']
        non_entity_tokens = namespace_data['counts']['non_entity_tokens']
        #print(namespace_data)
        csvwriter.writerow([
          namespace_path,
          namespace_id,
          str(clients),
          str(entities),
          str(non_entity_tokens)
        ])
    f.close()
  except Exception as e:
    logging.error(e)
    sys.exit(1)

