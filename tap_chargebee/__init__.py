import os
import sys
import json
import singer
import argparse
import tap_framework
import tap_chargebee.client
import tap_chargebee.streams

LOGGER = singer.get_logger()


class ChargebeeRunner(tap_framework.Runner):
    pass


@singer.utils.handle_top_exception(LOGGER)
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-c', '--config',
        help='Config file',
        required=True)

    parser.add_argument(
        '-s', '--state',
        help='State file')

    parser.add_argument(
        '-p', '--properties',
        help='Property selections: DEPRECATED, Please use --catalog instead')

    parser.add_argument(
        '--catalog',
        help='Catalog file')

    parser.add_argument(
        '-d', '--discover',
        action='store_true',
        help='Do schema discovery')

    cmdline_args = parser.parse_args()

    state_file = os.environ.get('CB_RS_STATE_FILE_NAME')
    if cmdline_args.state:
        raise Exception('Invalid argument. Instead, please set environment variable CB_RS_STATE_FILE_NAME and execute without this argument')

    if not state_file:
        raise Exception('Environment variable CB_RS_STATE_FILE_NAME not set. Please set this value to state file name')


    if not os.path.exists(state_file) or os.path.getsize(state_file) == 0:
        with open(state_file, 'w') as fp:
            json.dump({}, fp)

    sys.argv.extend(['-s', state_file])

    args = singer.utils.parse_args(
        required_config_keys=['api_key', 'start_date', 'site'])


    client = tap_chargebee.client.ChargebeeClient(args.config)

    runner = ChargebeeRunner(
        args, client, tap_chargebee.streams.AVAILABLE_STREAMS
        )

    if args.discover:
        runner.do_discover()
    else:
        runner.do_sync()


if __name__ == '__main__':
    main()
