import requests
from telegram.ext import Updater, CommandHandler
import logging

TOKEN = '6978306432:AAHZG3Uq-G3-k2MhcuFDXZKhyAbxBjs_TKE'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def start(update, context):
    update.message.reply_text(
        'Welcome to the OSINT bot! Send /search_ip <IP_address> to search for information about an IP address.'
    )


def search_ip(update, context):
    if not context.args:
        update.message.reply_text('Please provide an IP address to search')
        return
    ip_address = context.args[0]
    url = f"https://ipinfo.io/{ip_address}/json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if 'error' in data:
            update.message.reply_text(f"Error fetching data: {data['error']['message']}")
        else:
            info = f"Information about IP address {ip_address}:\n\n"
            info += f"🌐 IP Address: {data.get('ip', 'Not available')}\n"
            info += f"📍 Location: {data.get('city', 'Unknown')}, {data.get('region', 'Unknown')}, {data.get('country', 'Unknown')}\n"
            info += f"🔍 ISP: {data.get('org', 'Not available')}\n"
            info += f"📡 Timezone: {data.get('timezone', 'Not available')}\n"
            info += f"📶 Region: {data.get('region', 'Not available')}\n"
            info += f"🌍 Country: {data.get('country', 'Not available')}\n"
            info += f"🌆 City: {data.get('city', 'Not available')}\n"
            info += f"🏞️ Location: {data.get('loc', 'Not available')}\n"
            info += f"📱 Phone prefix: {data.get('phone', 'Not available')}\n"
            update.message.reply_text(info)

    except requests.HTTPError as e:
        logging.error(f"HTTP error occurred: {e}")
        update.message.reply_text("Error fetching user data")
    except requests.RequestException as e:
        logging.error(f"Request exception occurred: {e}")
        update.message.reply_text("Error fetching user data")
    except ValueError as e:
        logging.error(f"ValueError occurred: {e}")
        update.message.reply_text("Error parsing response data")


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("search_ip", search_ip))
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
