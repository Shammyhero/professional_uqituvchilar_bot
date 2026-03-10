from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def start_application_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📚 Kitobga ariza topshirish", callback_data="start_application")]
        ]
    )

def phone_request_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Raqamni yuborish", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

def region_selection_keyboard():
    regions = [
        "Toshkent shahri",
        "Toshkent viloyati",
        "Andijon viloyati",
        "Buxoro viloyati",
        "Farg'ona viloyati",
        "Jizzax viloyati",
        "Xorazm viloyati",
        "Namangan viloyati",
        "Navoiy viloyati",
        "Qashqadaryo viloyati",
        "Qoraqalpog'iston Respublikasi",
        "Samarqand viloyati",
        "Sirdaryo viloyati",
        "Surxondaryo viloyati"
    ]
    
    # Create inline keyboard with 2 buttons per row
    inline_keyboard = []
    row = []
    for region in regions:
        row.append(InlineKeyboardButton(text=region, callback_data=f"region_{region}"))
        if len(row) == 2:
            inline_keyboard.append(row)
            row = []
    if row:
        inline_keyboard.append(row)
        
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
