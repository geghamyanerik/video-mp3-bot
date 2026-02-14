import telebot
import os
import yt_dlp






bot = telebot.TeleBot('6532678746:AAGGIJfxIjZdM0PQ7UCmP--3qbRLerLbFVc')




  

     
@bot.message_handler(commands=['download'])
def download_command(message):
    bot.send_message(message.chat.id, "Խնդրում եմ ուղարկեք հղումը:")
    bot.register_next_step_handler(message, process_download)

def process_download(message):
    url = message.text
    msg = bot.send_message(message.chat.id, "Ներբեռնում եմ վիդեոն, սպասեք...")

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)

        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id,
                              text=f"Վիդեոն ներբեռնված է՝\n{filename}")

        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video)

    except Exception as e:
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id,
                              text="Սխալ՝ հնարավոր է հղումը սխալ է կամ վիդեոն պաշտպանված է։")






           
               

@bot.message_handler(commands=['downloadmp3'])
def download_audio(message):
    
    try:
      
        url = message.text.split(maxsplit=1)[1]

        msg = bot.send_message(message.chat.id, "Ներբեռնում եմ աուդիոն, սպասեք...")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            title = info_dict.get('title', None)
            filename = ydl.prepare_filename(info_dict)
            mp3_filename = os.path.splitext(filename)[0] + '.mp3'

        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id,
                              text=f"Աուդիոն ներբեռնված է՝ {title}.mp3")

        with open(mp3_filename, 'rb') as audio:
            bot.send_audio(message.chat.id, audio)

        # Ուղղակի ցանկության դեպքում կարող ես ֆայլը ջնջել
        os.remove(mp3_filename)

    except IndexError:
        bot.reply_to(message, "Խնդրում եմ, ուղարկեք հղումը այս ձևաչափով՝ /downloadmp3 <լինկ>")
    except Exception as e:
        bot.reply_to(message, f"Սխալ՝ {e}")


bot.infinity_polling()
