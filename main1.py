import telebot
import requests
import re
import yt_dlp as youtube_dl
import os

# указываем токен для доступа к боту
bot = telebot.TeleBot('')

# приветственный текст
start_txt = 'Привет!'


# обрабатываем старт бота
@bot.message_handler(commands=['start'])
def start(message):
    # выводим приветственное сообщение
    bot.send_message(message.from_user.id, start_txt, parse_mode='Markdown')

# обрабатываем любой текстовый запрос
@bot.message_handler(commands=["weather", "w"])
def weather(message):
    # получаем город из сообщения пользователя
  city = message.text.split(maxsplit=1)[1]
  # формируем запрос
  url = 'https://api.openweathermap.org/data/2.5/weather?q='+city+'&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
  # отправляем запрос на сервер и сразу получаем результат
  weather_data = requests.get(url).json()
  # получаем данные о температуре и о том, как она ощущается
  temperature = round(weather_data['main']['temp'])
  temperature_feels = round(weather_data['main']['feels_like'])
  # формируем ответы
  w_now = 'Сейчас в городе ' + city + ' ' + str(temperature) + ' °C'
  w_feels = 'Ощущается как ' + str(temperature_feels) + ' °C'
  # отправляем значения пользователю
  bot.send_message(message.chat.id, w_now)
  bot.send_message(message.chat.id, w_feels)


@bot.message_handler(commands=["youtube", "y"])
def download_youtube_video(message):
    try:
        video_url = message.text.split(maxsplit=1)[1]
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': 'videos/%(id)s.%(ext)s',
            'noplaylist': True,
            'quiet': True
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            video_filename = ydl.prepare_filename(info_dict)
        
        video = open(video_filename, 'rb')
        bot.send_video(message.chat.id, video)
        video.close()
            
        os.remove(video_filename)

    except Exception as e:
        bot.send_message(message.chat.id, 'Произошла ошибка при обработке вашего запроса: ' + str(e))

# запускаем бота
if __name__ == '__main__':
    while True:
        # в бесконечном цикле постоянно опрашиваем бота — есть ли новые сообщения
        try:
            bot.polling(none_stop=True, interval=0)
        # если возникла ошибка — сообщаем про исключение и продолжаем работу
        except Exception as e: 
            print('❌❌❌❌❌ Сработало исключение! ❌❌❌❌❌')