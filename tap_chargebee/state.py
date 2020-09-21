import datetime
import json
import singer

LOGGER = singer.get_logger()


def get_last_record_value_for_table(state, table, field):
    last_value = state.get('bookmarks', {}) \
                      .get(table, {}) \
                      .get(field)

    if last_value is None:
        return None

    #return json.load(last_value)
    return last_value


def incorporate(state, table, key, value, force=False):
    if value is None or not bool(value):
        return state

    if isinstance(value['resource_updated_at'], datetime.datetime):
        value['resource_updated_at'] = value['resource_updated_at'].strftime('%Y-%m-%dT%H:%M:%SZ')

    if state is None:
        new_state = {}
    else:
        new_state = state.copy()

    if 'bookmarks' not in new_state:
        new_state['bookmarks'] = {}

    if table not in new_state['bookmarks']:
        new_state['bookmarks'][table] = {}

    if(new_state['bookmarks'].get(table, {}).get(key) is None or
       new_state['bookmarks'].get(table, {}).get(key).get('resource_updated_at') < value['resource_updated_at'] or
       new_state['bookmarks'].get(table, {}).get(key).get('last_processed_id') < value['last_processed_id'] or
       new_state['bookmarks'].get(table, {}).get(key).get('last_processed_dsid') < value['last_processed_dsid'] or
       force):
        new_state['bookmarks'][table][key] = value

    return new_state


def save_state(state, filename):
    if not state:
        return

    LOGGER.info('Updating state.')

    singer.write_state(state)
    try:
    	with open(filename, 'w') as handle:
    		handle.write(json.dumps(state)) 
    except Exception as e:
        LOGGER.fatal(e)
        raise RuntimeError

def load_state(filename):
    if filename is None:
        return {}

    try:
        with open(filename) as handle:
            return json.load(handle)
    except:
        LOGGER.fatal("Failed to decode state file. Is it valid json?")
        raise RuntimeError
