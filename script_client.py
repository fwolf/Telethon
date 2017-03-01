import traceback

from telethon.script_telegram_client import (ScriptTelegramClient)
from telethon.tl import MTProtoRequest, Session


def load_settings(path='api/settings'):
    """Loads the user settings located under `api/`"""
    settings = {}
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            value_pair = line.split('=')
            left = value_pair[0].strip()
            right = value_pair[1].strip()
            if right.isnumeric():
                settings[left] = int(right)
            else:
                settings[left] = right

    return settings


if __name__ == '__main__':
    # Load the settings and initialize the client
    settings = load_settings()
    session_user_id = settings.get('session_name', 'anonymous')
    api_id = settings['api_id']
    api_hash = settings['api_hash']
    user_phone = str(settings['user_phone'])

    client = ScriptTelegramClient(
        session_user_id,
        user_phone,
        api_id,
        api_hash)

    print('Initialization done!')

    try:
        client.run()

    except Exception as e:
        print('Unexpected error ({}): {} at\n{}'.format(
            type(e), e, traceback.format_exc()))

    finally:
        print('Exiting...')
        client.disconnect()
