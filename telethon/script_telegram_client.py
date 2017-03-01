import shutil, time
from getpass import getpass

from telethon import RPCError, TelegramClient
from telethon.tl.types import UpdateShortChatMessage, UpdateShortMessage
from telethon.utils import get_display_name


class ScriptTelegramClient(TelegramClient):
    def __init__(self, session_user_id, user_phone, api_id, api_hash):
        print('Initializing script mode...')
        super().__init__(session_user_id, api_id, api_hash)

        # Store all the found media in memory here,
        # so it can be downloaded if the user wants
        self.found_media = set()

        print('Connecting to Telegram servers...')
        self.connect()

        # Then, ensure we're authorized and have access
        if not self.is_user_authorized():
            print('First run. Sending code request...')
            self.send_code_request(user_phone)

            code_ok = False
            while not code_ok:
                code = input('Enter the code you just received: ')
                try:
                    code_ok = self.sign_in(user_phone, code)

                # Two-step verification may be enabled
                except RPCError as e:
                    if e.password_required:
                        pw = getpass(
                            'Two step verification is enabled. Please enter your password: ')
                        code_ok = self.sign_in(password=pw)
                    else:
                        raise e


    def run(self):
        # Listen for updates
        self.add_update_handler(self.update_handler)

        # Enter a while loop to chat as long as the user wants
        while True:
            time.sleep(0.1)


    @staticmethod
    def update_handler(update_object):
        print('')
        print(type(update_object))
        print(vars(update_object))
        if type(update_object) is UpdateShortMessage:
            if update_object.out:
                print('You sent {} to user #{}'.format(update_object.message,
                                                       update_object.user_id))
            else:
                print('[User #{} sent {}]'.format(update_object.user_id,
                                                  update_object.message))

        elif type(update_object) is UpdateShortChatMessage:
            if update_object.out:
                print('You sent {} to chat #{}'.format(update_object.message,
                                                       update_object.chat_id))
            else:
                print('[Chat #{}, user #{} sent {}]'.format(
                    update_object.chat_id, update_object.from_id,
                    update_object.message))
