import requests

ROBO_KASSA_SECRET_KEY = "your_robokassa_secret_key"
ROBO_KASSA_LOGIN = "your_robokassa_login"
ROBO_KASSA_URL = "https://merchant.roboxchange.com/Index.aspx"

async def create_payment_link(tariff_id, user_id, amount):
    # Генерация уникального номера заказа
    order_id = f"{user_id}_{tariff_id}_{int(time.time())}"

    # Параметры запроса для RoboKassa
    params = {
        'MrchLogin': ROBO_KASSA_LOGIN,
        'OutSum': amount,
        'InvId': order_id,
        'Desc': f"Оплата подписки для пользователя {user_id}",
        'SignatureValue': generate_signature(order_id, amount),  # Генерация подписи
    }

    # Ссылка на оплату
    payment_link = f"{ROBO_KASSA_URL}?{urlencode(params)}"
    return payment_link

def generate_signature(order_id, amount):
    # Генерация подписи для RoboKassa
    signature = f"{ROBO_KASSA_LOGIN}:{amount}:{order_id}:{ROBO_KASSA_SECRET_KEY}"
    return md5(signature.encode('utf-8')).hexdigest().upper()

# Метод для обработки уведомления от RoboKassa
async def handle_robokassa_notification(request):
    data = request.POST
    order_id = data.get('InvId')
    amount = float(data.get('OutSum'))
    signature = data.get('SignatureValue')

    # Проверка подписи
    expected_signature = generate_signature(order_id, amount)
    if signature != expected_signature:
        raise Exception("Ошибка подписи")

    # Обработка успешного платежа
    user_id = extract_user_id_from_order(order_id)
    await activate_subscription(user_id, amount)  # Активируем подписку

    return "OK"

async def activate_subscription(user_id, amount):
    # Здесь логика активации подписки для пользователя
    pass
