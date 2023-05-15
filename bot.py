import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram import types
import yt_dlp
import os
import time

logging.basicConfig(level=logging.INFO)

bot = Bot(token="6179334416:AAGM4dztib7bYuUo7XY8ERP383RYMZabTuM")
dp = Dispatcher(bot)

class FilenameCollectorPP(yt_dlp.postprocessor.common.PostProcessor):
	def __init__(self):
		super(FilenameCollectorPP, self).__init__(None)
		self.filenames = []

	def run(self, information):
		self.filenames.append(information["filepath"])
		return [], information

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
	await message.reply("Не очень добрый день. Меня зовут Марвин. Вы можете использовать меня для извлечения аудифайлов из видео, выложенных на платформе YouTube. Только прошу вас, давайте разберёмся с этим быстрее...")

@dp.message_handler(commands=['find'])
async def search(message: types.Message):
	arg = message.get_args()
	await message.reply('Обработка запроса... Мучительное ожидание.')
	YDL_OPTIONS = {'format': 'bestaudio/best',
		'noplaylist':'True',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192'
		}],
	}
	with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
		try:
			get(arg) 
		except:
			filename_collector = FilenameCollectorPP()
			ydl.add_post_processor(filename_collector)
			video = ydl.extract_info(f"ytsearch:{arg}", download=True)['entries'][0]
			await message.reply_document(open(filename_collector.filenames[0], 'rb'))
			await message.reply(f'Файл был отправлен... Мои страдания наконец-то окончены?\n\n{arg}')
			time.sleep(5)
			os.remove(filename_collector.filenames[0])
			
		else:
			video = ydl.extract_info(arg, download=True)
		
		return filename_collector.filenames[0]

@dp.message_handler(commands=['youtube'])
async def youtube(message: types.Message):
	arguments = message.get_args()
	await message.reply("Обработка запроса... Мучительное ожидание.")
	ydl_opts = {
		'format': 'bestaudio/best',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}],
	}
	with yt_dlp.YoutubeDL(ydl_opts) as ydl:
		filename_collector = FilenameCollectorPP()
		ydl.add_post_processor(filename_collector)
		ydl.download([arguments])
		
		
		await message.reply_document(open(filename_collector.filenames[0], 'rb'))
		await message.reply(f'Файл был отправлен... Мои страдания наконец-то окончены?\n\n{arg}')
		time.sleep(5)
		os.remove(filename_collector.filenames[0])
		return filename_collector.filenames[0]

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)