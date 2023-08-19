import logging
import subprocess
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode, ContentType
from aiogram.utils import executor

logging.basicConfig(level=logging.INFO)
API_TOKEN = 'YOUR_BOT_TOEKEN_SHOULD_BE_HERE'


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

users_state = {}

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Send .p12!📜")

@dp.message_handler(content_types=ContentType.DOCUMENT)
async def handle_docs_photo(message: types.Message):
    if not message.document.file_name.endswith('.p12'):
        await message.reply("Wrong file type! 🥹")
        return

    file_id = message.document.file_id
    users_state[message.from_user.id] = {'file_id': file_id}
    await message.reply(".P12 current password? 🔐")


@dp.message_handler(lambda message: message.from_user.id in users_state and 'new_password' not in users_state[message.from_user.id])
async def handle_passwords(message: types.Message):
    user_data = users_state.get(message.from_user.id, {})

    if 'file_id' not in user_data:
        await message.reply("Please upload a .p12 file first.")
        return

    downloaded_file_path = f"{user_data['file_id']}.p12"

    if 'old_password' not in user_data:
        user_data['old_password'] = message.text

        file_info = await bot.get_file(user_data['file_id'])
        file_path = f'./{user_data["file_id"]}.p12'
        await bot.download_file(file_info.file_path, destination=file_path)

        if not check_p12_password(file_path, user_data['old_password']):
            await message.reply("Wrong password. 🥲")
            os.remove(file_path)
            del users_state[message.from_user.id]
            return

        await message.reply("Correct! ✅🔑 \nSend new password.")

    else:
        user_data['new_password'] = message.text

        result = change_p12_password(downloaded_file_path, user_data['old_password'], user_data['new_password'])

        if result is not True:
            await message.reply(f"Failed to change password:🥹\n {result}")
            os.remove(downloaded_file_path)
            del users_state[message.from_user.id]
            return

        checker_command = f"node checker/index.js {downloaded_file_path} {user_data['new_password']}"
        certificate_info = subprocess.check_output(checker_command, shell=True, text=True)

        new_file_path = f'./Certificate({user_data["new_password"][:8]}).p12'
        os.rename(downloaded_file_path, new_file_path)

        new_file_description = f"📜 Certificate Modified!\n\n\n{certificate_info.strip()}\n"

        with open(new_file_path, 'rb') as file:
            await bot.send_document(message.from_user.id, document=file, caption=new_file_description, parse_mode=ParseMode.MARKDOWN)

        os.remove(new_file_path)
        del users_state[message.from_user.id]

def check_p12_password(input_file, password):
    cmd = [
        'openssl', 'pkcs12',
        '-info',
        '-in', input_file,
        '-password', f'pass:{password}',
        '-noout'
    ]
    result = subprocess.run(cmd, capture_output=True)
    return result.returncode == 0

def change_p12_password(input_file, old_password, new_password):
    try:
        temp_file = input_file + "_temp.p12"
        cmd_export = [
            'openssl', 'pkcs12',
            '-in', input_file,
            '-out', 'temp.pem',
            '-nodes',
            '-password', f'pass:{old_password}'
        ]

        result_export = subprocess.run(cmd_export, capture_output=True, text=True)
        if result_export.returncode != 0:
            raise Exception(result_export.stderr)

        cmd_pack = [
            'openssl', 'pkcs12',
            '-export',
            '-in', 'temp.pem',
            '-out', temp_file,
            '-password', f'pass:{new_password}'
        ]

        result_pack = subprocess.run(cmd_pack, capture_output=True, text=True)
        if result_pack.returncode != 0:
            os.remove('temp.pem')
            raise Exception(result_pack.stderr)

        os.remove(input_file)
        os.rename(temp_file, input_file)
        os.remove('temp.pem')
        return True
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

