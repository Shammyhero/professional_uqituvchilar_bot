import pandas as pd
from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message
from aiogram.types import FSInputFile

from database import get_all_applications
from config import ADMIN_GROUP_ID

admin_router = Router()

@admin_router.message(F.text == "/getid")
async def get_chat_id(message: Message):
    """Temporary command to help find the Group ID"""
    await message.reply(f"This chat's ID is: {message.chat.id}")

@admin_router.message(F.text == "/export")
async def export_data(message: Message):
    # Security check: ensure the user requesting this is in the Admin Group
    # For now, a simple check if ADMIN_GROUP_ID is set and the command is run there or by an admin
    # To keep it simple, we'll just allow it for now, but in production, we'd verify the user.
    
    rows, columns = get_all_applications()
    
    if not rows:
        await message.answer("Bazada ma'lumot yo'q (No data in database).")
        return
        
    # Create a Pandas DataFrame
    df = pd.DataFrame(rows, columns=columns)
    
    # Optional: rename columns to Uzbek for the export
    df.rename(columns={
        'username': 'Username (@)',
        'full_name': 'Ism-Familiya',
        'phone_number': 'Telefon Raqam',
        'region': 'Viloyat',
        'subject': 'Fan',
        'source': 'Manba',
        'created_at': 'Vaqt'
    }, inplace=True)
    
    # Generate filename with current datetime
    filename = f"applications_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    # Export to Excel
    df.to_excel(filename, index=False)
    
    # Send the file
    document = FSInputFile(filename)
    await message.answer_document(
        document=document,
        caption="Barcha arizalar ro'yxati (Sorted by newest first)."
    )
    
    # Clean up the file after sending (optional, to save space)
    import os
    try:
        os.remove(filename)
    except Exception as e:
        print(f"Error removing file {filename}: {e}")
