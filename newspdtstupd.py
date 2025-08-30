
import speedtest
import datetime
import schedule
import time
import os

LOG_FILE = "speed_log.txt"

def log_result(speed_info):
    """Сохраняет результат в файл"""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{speed_info}\n")

def run_speed_test():
    """Запускает тест скорости и сохраняет результат"""
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Запуск теста скорости...")
    
    try:
        st = speedtest.Speedtest()
        st.get_best_server()

        download = st.download() / 1_000_000  # Mbps
        upload = st.upload() / 1_000_000      # Mbps
        ping = st.results.ping                # ms
        server = st.results.server

        # Форматируем результат
        result = (
            f"⏱ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
            f"📥 {download:.2f} Mbps | "
            f"📤 {upload:.2f} Mbps | "
            f"🔁 {ping} ms | "
            f"📡 {server['name']}, {server['country']}"
        )

        print("✅ Тест завершён:")
        print(result)
        
        # Сохраняем в файл
        log_result(result)

    except Exception as e:
        error_msg = f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ Ошибка: {e}"
        print(error_msg)
        log_result(error_msg)

def main():
    print("🌐 Скрипт проверки скорости интернета с автозапуском")
    print("—" * 70)
    print("Выбери режим работы:")
    print("1. Запустить один раз")
    print("2. Запускать по расписанию (каждый час)")
    print("3. Запускать каждые 30 минут")
    print("4. Выход")

    choice = input("\nВведи номер (1–4): ").strip()

    if choice == "1":
        run_speed_test()
    elif choice == "2":
        print("\n⏰ Режим: каждый час. Нажми Ctrl+C для остановки.")
        schedule.every().hour.do(run_speed_test)
        run_speed_test()  # Запуск сразу при старте
    elif choice == "3":
        print("\n⏰ Режим: каждые 30 минут. Нажми Ctrl+C для остановки.")
        schedule.every(30).minutes.do(run_speed_test)
        run_speed_test()
    elif choice == "4":
        print("👋 Пока!")
        return
    else:
        print("❌ Неверный выбор.")
        return

    # Запуск цикла расписания
    print("📌 Скрипт работает в фоне. Чтобы остановить — нажми Ctrl+C.\n")
    try:
        while True:
            schedule.run_pending()
            time.sleep(10)  # Проверяем каждые 10 секунд
    except KeyboardInterrupt:
        print("\n\n🛑 Работа скрипта остановлена пользователем.")
        print(f"📄 Все результаты сохранены в файл: {LOG_FILE}")

if __name__ == "__main__":
    main()
