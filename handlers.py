from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, FSInputFile
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
import os

from states import ApplicationForm
from keyboards import phone_request_keyboard, region_selection_keyboard, start_application_keyboard
from database import add_application
from config import ADMIN_GROUP_ID

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    welcome_text = (
        "Ustozlar uchun yozilgan <b>“Professional o’qituvchilar”</b> nomli kitobimizga "
        "qiziqish bildirganingizdan xursandmiz.\n\n"
        "Ushbu kitob endilikda ustozlikka kirib kelgan barcha fan ustozlariga mos keladi "
        "va ustozlikni umuman boshqa nuqtadan kashf qilishlariga yordam beradi.\n\n"
        "📚 <b>Kitobni chegirma narxda buyurtma qilish uchun quyidagi tugmani bosing 👇</b>"
    )
    
    image_path = "images/image.png"
    if os.path.exists(image_path):
        photo = FSInputFile(image_path)
        await message.answer_photo(
            photo=photo,
            caption=welcome_text,
            parse_mode="HTML",
            reply_markup=start_application_keyboard()
        )
    else:
        await message.answer(
            welcome_text, 
            parse_mode="HTML", 
            reply_markup=start_application_keyboard()
        )

@router.callback_query(F.data == "start_application")
async def start_application(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("👤 Ism-familyangizni kiriting:")
    await state.set_state(ApplicationForm.waiting_for_name)
    await callback.answer()

@router.message(ApplicationForm.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer(
        "📞 Telefon raqamingizni yuboring:\n"
        "(Iltimos, pastdagi \"📱 Raqamni yuborish\" tugmasini bosing)",
        reply_markup=phone_request_keyboard()
    )
    await state.set_state(ApplicationForm.waiting_for_phone)

@router.message(ApplicationForm.waiting_for_phone, F.contact)
async def process_phone_contact(message: Message, state: FSMContext):
    phone_number = message.contact.phone_number
    await state.update_data(phone_number=phone_number)
    
    # Remove the reply keyboard after getting the phone number
    await message.answer("Raqam qabul qilindi ✅", reply_markup=ReplyKeyboardRemove())
    # Send the inline keyboard for regions
    await message.answer("📍 Qaysi viloyat yoki shahardansiz?\nIltimos, quyidagilardan birini tanlang:", reply_markup=region_selection_keyboard())
    await state.set_state(ApplicationForm.waiting_for_region)

@router.message(ApplicationForm.waiting_for_phone, F.text)
async def process_phone_invalid(message: Message):
    await message.answer(
        "❌ Noto'g'ri format.\n"
        "Iltimos, telefon raqamingizni kiritish uchun pastdagi "
        "**\"📱 Raqamni yuborish\"** tugmasini bosing.",
        reply_markup=phone_request_keyboard()
    )

@router.callback_query(ApplicationForm.waiting_for_region, F.data.startswith("region_"))
async def process_region(callback: CallbackQuery, state: FSMContext):
    region = callback.data.split("_")[1]
    await state.update_data(region=region)
    
    # Edit the message to remove the buttons
    await callback.message.edit_text(f"📍 Tanlangan hudud: {region}")
    
    await callback.message.answer("📚 Qaysi fandan dars berasiz (yoki dars bermoqchisiz)?")
    await state.set_state(ApplicationForm.waiting_for_subject)
    await callback.answer() # Required to stop the loading spinner on the button

@router.message(ApplicationForm.waiting_for_subject)
async def process_subject(message: Message, state: FSMContext):
    await state.update_data(subject=message.text)
    await message.answer("📢 Kitob haqida qayerdan eshitdingiz?")
    await state.set_state(ApplicationForm.waiting_for_source)

@router.message(ApplicationForm.waiting_for_source)
async def process_source(message: Message, state: FSMContext):
    await state.update_data(source=message.text)
    
    # Get all the collected data
    data = await state.get_data()
    
    # Get username if it exists
    username_raw = message.from_user.username
    username = f"@{username_raw}" if username_raw else "Yo'q (None)"
    
    # Save to database
    add_application(
        user_id=message.from_user.id,
        username=username,
        full_name=data['full_name'],
        phone_number=data['phone_number'],
        region=data['region'],
        subject=data['subject'],
        source=data['source']
    )
    
    # Send confirmation to user
    confirmation_text = (
        "<b>Kitobga ariza topshirganingiz uchun rahmat!</b> 🎉\n\n"
        "Tez orada kitob muallifi, Uktamovaning shaxsan o’zlari sizga qo’ng’iroq orqali bog’lanadilar va "
        "kitob haqida to’liq informatsiya beradilar."
    )
    await message.answer(confirmation_text, parse_mode="HTML")
    
    # Send notification to Admin Group
    if ADMIN_GROUP_ID:
        admin_text = (
            f"🆕 YANGA BUYURTMA\n\n"
            f"👤 Ismi: {data['full_name']}\n"
            f"🌐 Username: {username}\n"
            f"📞 Tel: {data['phone_number']}\n"
            f"📍 Hudud: {data['region']}\n"
            f"📚 Fan: {data['subject']}\n"
            f"📢 Manba: {data['source']}\n"
            f"🆔 User ID: {message.from_user.id}"
        )
        try:
            await message.bot.send_message(chat_id=ADMIN_GROUP_ID, text=admin_text)
        except Exception as e:
            print(f"Failed to send admin notification: {e}")
            
    # Clear state
    await state.clear()
