import telebot
import requests
import time
import os
from datetime import datetime

# Configurações do bot
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_ADMIN_CHAT_ID = os.getenv('TELEGRAM_ADMIN_CHAT_ID')

# Inicializar bot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    response = """🌊 *Wave Song Bot* 🌊

*Comandos disponíveis:*
/status - Ver status do sistema
/notify [mensagem] - Enviar notificação global
/users - Estatísticas do sistema
/help - Mostra esta ajuda

*Desenvolvido por Schutz*"""
    bot.send_message(message.chat.id, response, parse_mode='Markdown')

@bot.message_handler(commands=['status'])
def handle_status(message):
    if str(message.chat.id) != TELEGRAM_ADMIN_CHAT_ID:
        bot.send_message(message.chat.id, "❌ Apenas administradores podem usar este comando.")
        return
    
    try:
        # Testar conexão com Firebase
        response = requests.get("https://wavesong-default-rtdb.firebaseio.com/.json", timeout=10)
        status = "✅ Online" if response.status_code == 200 else "⚠️ Offline"
        bot.send_message(message.chat.id, f"🌊 *Status do Wave Song*\n\n{status}\n\n🕒 {datetime.now().strftime('%d/%m/%Y %H:%M')}", parse_mode='Markdown')
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ *Erro de conexão:*\n{str(e)}", parse_mode='Markdown')

@bot.message_handler(commands=['notify'])
def handle_notify(message):
    if str(message.chat.id) != TELEGRAM_ADMIN_CHAT_ID:
        bot.send_message(message.chat.id, "❌ Apenas administradores podem enviar notificações.")
        return
    
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.send_message(message.chat.id, "❌ Uso: /notify [mensagem]")
        return
    
    notification_text = parts[1]
    
    try:
        # Enviar notificação para Firebase
        import firebase_admin
        from firebase_admin import credentials, db
        
        # Configuração do Firebase
        firebase_config = {
            "type": "service_account",
            # ... (sua configuração completa do Firebase)
        }
        
        if not firebase_admin._apps:
            cred = credentials.Certificate(firebase_config)
            firebase_admin.initialize_app(cred, {
                "databaseURL": "https://wavesong-default-rtdb.firebaseio.com/"
            })
        
        ref = db.reference("/global_notifications")
        notification_data = {
            "message": notification_text,
            "admin": "Schutz (Telegram)",
            "timestamp": datetime.now().isoformat(),
            "read_by": {}
        }
        ref.push(notification_data)
        
        bot.send_message(message.chat.id, f"✅ *Notificação enviada:*\n{notification_text}", parse_mode='Markdown')
        
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ *Erro ao enviar notificação:*\n{str(e)}", parse_mode='Markdown')

@bot.message_handler(commands=['users'])
def handle_users(message):
    if str(message.chat.id) != TELEGRAM_ADMIN_CHAT_ID:
        bot.send_message(message.chat.id, "❌ Apenas administradores podem ver estatísticas.")
        return
    
    try:
        # Contar músicas no Firebase
        import firebase_admin
        from firebase_admin import credentials, db
        
        if not firebase_admin._apps:
            cred = credentials.Certificate(firebase_config)
            firebase_admin.initialize_app(cred, {
                "databaseURL": "https://wavesong-default-rtdb.firebaseio.com/"
            })
        
        ref = db.reference("/songs")
        songs = ref.get()
        total_songs = len(songs) if songs else 0
        
        response = f"""👥 *Estatísticas do Wave Song*

🎵 Músicas: {total_songs}
🛡️ Admin: Schutz
🕒 {datetime.now().strftime('%d/%m/%Y %H:%M')}"""
        
        bot.send_message(message.chat.id, response, parse_mode='Markdown')
        
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ *Erro ao buscar estatísticas:*\n{str(e)}", parse_mode='Markdown')

if __name__ == "__main__":
    print("🤖 Iniciando Wave Song Bot...")
    print(f"🆔 Chat ID do Admin: {TELEGRAM_ADMIN_CHAT_ID}")
    print("✅ Bot pronto para receber comandos!")
    
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"❌ Erro no bot: {e}")
        time.sleep(5)
