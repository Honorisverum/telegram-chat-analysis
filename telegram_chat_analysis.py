#!/usr/bin/env python3
"""
Telegram Chat Analysis Script

This script calculates the percentage of days you've been talking in a Telegram 1-on-1 chat
over the last year.
"""

import os
import sys
from datetime import datetime, timedelta
from collections import defaultdict
import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetHistoryRequest
import configparser

# Configuration
config = configparser.ConfigParser()
config_file = 'config.ini'

def create_default_config():
    """Create a default configuration file if it doesn't exist."""
    config['Telegram'] = {
        'api_id': 'YOUR_API_ID',
        'api_hash': 'YOUR_API_HASH',
        'phone': 'YOUR_PHONE_NUMBER',
        'username': 'YOUR_USERNAME'
    }
    
    with open(config_file, 'w') as f:
        config.write(f)
    
    print(f"Created default config file at {config_file}")
    print("Please edit this file with your Telegram API credentials.")
    print("You can get your API credentials at https://my.telegram.org/apps")
    sys.exit(1)

# Check if config file exists, create it if not
if not os.path.exists(config_file):
    create_default_config()

# Read config
config.read(config_file)

# Telegram API credentials
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
phone = config['Telegram']['phone']
username = config['Telegram']['username']

async def calculate_chat_days_percentage(client, chat_entity):
    """
    Calculate the percentage of days with messages in a chat over the last year.
    
    Args:
        client: Telegram client instance
        chat_entity: The chat entity to analyze
        
    Returns:
        float: Percentage of days with messages
    """
    # Calculate date range (last 365 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    print(f"Analyzing messages from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    # Dictionary to track days with messages
    days_with_messages = defaultdict(bool)
    
    # Get message history
    offset_id = 0
    limit = 100
    total_messages = 0
    
    while True:
        history = await client(GetHistoryRequest(
            peer=chat_entity,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        
        if not history.messages:
            break
            
        messages = history.messages
        
        for message in messages:
            message_date = message.date
            
            # Skip messages outside our date range
            if message_date < start_date:
                # We've gone past our date range, no need to fetch more
                offset_id = 0
                break
                
            # Mark this day as having messages
            day_key = message_date.strftime('%Y-%m-%d')
            days_with_messages[day_key] = True
            
            total_messages += 1
        
        if offset_id == 0:
            break
            
        # Update offset for next batch
        offset_id = messages[-1].id
        
        # Simple progress indicator
        print(f"Processed {total_messages} messages so far...")
    
    # Calculate percentage
    total_days = (end_date - start_date).days + 1
    days_with_communication = len(days_with_messages)
    percentage = (days_with_communication / total_days) * 100
    
    return percentage, days_with_communication, total_days, total_messages

async def main():
    # Create the client and connect
    client = TelegramClient(username, api_id, api_hash)
    await client.start(phone)
    print("Client Created")
    
    # Get list of dialogs
    dialogs = await client.get_dialogs()
    
    # Display available chats
    print("\nAvailable chats:")
    for i, dialog in enumerate(dialogs):
        if dialog.is_user:  # Only show 1-on-1 chats
            print(f"{i}: {dialog.name} (1-on-1 chat)")
    
    # Ask user to select a chat
    while True:
        try:
            chat_index = int(input("\nEnter the number of the chat to analyze: "))
            if 0 <= chat_index < len(dialogs) and dialogs[chat_index].is_user:
                selected_chat = dialogs[chat_index]
                break
            else:
                print("Invalid selection. Please choose a valid 1-on-1 chat.")
        except ValueError:
            print("Please enter a number.")
    
    print(f"\nAnalyzing chat with {selected_chat.name}...")
    
    # Calculate percentage
    percentage, days_with_comm, total_days, total_messages = await calculate_chat_days_percentage(
        client, selected_chat.entity
    )
    
    # Display results
    print("\n--- Results ---")
    print(f"Total messages analyzed: {total_messages}")
    print(f"Days with communication: {days_with_comm} out of {total_days} days")
    print(f"Percentage of days with communication: {percentage:.2f}%")
    
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())