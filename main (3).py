import discord
from discord.ext import commands
import requests
import json
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# API key and bot token
bot_token = #ENTER BOT TOKEN HERE AS A STRING!!!

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

def format_commodity(commodity):
    """Utility function to format a single commodity's data."""
    return (
        f"**Commodity Name:** {commodity['commodity_name']}\n"
        f"**Terminal Name:** {commodity['terminal_name']}\n"
        f"**Price Buy:** {commodity['price_buy']}\n"
        f"**Price Buy Avg:** {commodity['price_buy_avg']}\n"
        f"**Price Sell:** {commodity['price_sell']}\n"
        f"**Price Sell Avg:** {commodity['price_sell_avg']}\n"
        f"**SCU Buy:** {commodity['scu_buy']}\n"
        f"**SCU Buy Avg:** {commodity['scu_buy_avg']}\n"
        f"**SCU Sell Stock:** {commodity['scu_sell_stock']}\n"
        f"**SCU Sell Stock Avg:** {commodity['scu_sell_stock_avg']}\n"
        f"**SCU Sell:** {commodity['scu_sell']}\n"
        f"**SCU Sell Avg:** {commodity['scu_sell_avg']}\n"
        f"**Status Buy:** {commodity['status_buy']}\n"
        f"**Status Sell:** {commodity['status_sell']}\n"
        f"**Date Added:** {commodity['date_added']}\n"
        f"**Date Modified:** {commodity['date_modified']}\n"
        "-------------------------\n"
    )

def chunk_message(message, chunk_size=1800): # DO NOT EDIT CHUNK_SIZE, This is to avoid discord message limits. 1900+ will stop working
    """Utility function to split a message into chunks."""
    return [message[i:i+chunk_size] for i in range(0, len(message), chunk_size)]

def format_commodity_averages(data):
    """Utility function to format a single commodity's averages data."""
    return (
        f"**Commodity Name:** {data['commodity_name']}\n"
        f"**Commodity Code:** {data['commodity_code']}\n"
        f"**Price Buy (Last Reported):** {data['price_buy']}\n"
        f"**Price Buy Min:** {data['price_buy_min']}\n"
        f"**Price Buy Min Week:** {data['price_buy_min_week']}\n"
        f"**Price Buy Min Month:** {data['price_buy_min_month']}\n"
        f"**Price Buy Max:** {data['price_buy_max']}\n"
        f"**Price Buy Max Week:** {data['price_buy_max_week']}\n"
        f"**Price Buy Max Month:** {data['price_buy_max_month']}\n"
        f"**Price Buy Avg:** {data['price_buy_avg']}\n"
        f"**Price Buy Avg Week:** {data['price_buy_avg_week']}\n"
        f"**Price Buy Avg Month:** {data['price_buy_avg_month']}\n"
        f"**Price Buy Users:** {data['price_buy_users']}\n"
        f"**Price Buy Users Rows:** {data['price_buy_users_rows']}\n"
        f"**Price Sell (Last Reported):** {data['price_sell']}\n"
        f"**Price Sell Min:** {data['price_sell_min']}\n"
        f"**Price Sell Min Week:** {data['price_sell_min_week']}\n"
        f"**Price Sell Min Month:** {data['price_sell_min_month']}\n"
        f"**Price Sell Max:** {data['price_sell_max']}\n"
        f"**Price Sell Max Week:** {data['price_sell_max_week']}\n"
        f"**Price Sell Max Month:** {data['price_sell_max_month']}\n"
        f"**Price Sell Avg:** {data['price_sell_avg']}\n"
        f"**Price Sell Avg Week:** {data['price_sell_avg_week']}\n"
        f"**Price Sell Users:** {data['price_sell_users']}\n"
        f"**Price Sell Users Rows:** {data['price_sell_users_rows']}\n"
        f"**SCU Buy (Last Reported):** {data['scu_buy']}\n"
        f"**SCU Buy Min:** {data['scu_buy_min']}\n"
        f"**SCU Buy Min Week:** {data['scu_buy_min_week']}\n"
        f"**SCU Buy Min Month:** {data['scu_buy_min_month']}\n"
        f"**SCU Buy Max:** {data['scu_buy_max']}\n"
        f"**SCU Buy Max Week:** {data['scu_buy_max_week']}\n"
        f"**SCU Buy Max Month:** {data['scu_buy_max_month']}\n"
        f"**SCU Buy Avg:** {data['scu_buy_avg']}\n"
        f"**SCU Buy Avg Week:** {data['scu_buy_avg_week']}\n"
        f"**SCU Buy Avg Month:** {data['scu_buy_avg_month']}\n"
        f"**SCU Buy Total:** {data['scu_buy_total']}\n"
        f"**SCU Buy Total Week:** {data['scu_buy_total_week']}\n"
        f"**SCU Buy Total Month:** {data['scu_buy_total_month']}\n"
        f"**SCU Buy Users:** {data['scu_buy_users']}\n"
        f"**SCU Buy Users Rows:** {data['scu_buy_users_rows']}\n"
        f"**SCU Sell Stock (Last Reported):** {data['scu_sell_stock']}\n"
        f"**SCU Sell Stock Week:** {data['scu_sell_stock_week']}\n"
        f"**SCU Sell Stock Month:** {data['scu_sell_stock_month']}\n"
        f"**SCU Sell (Last Calculated Demand):** {data['scu_sell']}\n"
        f"**SCU Sell Min:** {data['scu_sell_min']}\n"
        f"**SCU Sell Min Week:** {data['scu_sell_min_week']}\n"
        f"**SCU Sell Min Month:** {data['scu_sell_min_month']}\n"
        f"**SCU Sell Max:** {data['scu_sell_max']}\n"
        f"**SCU Sell Max Week:** {data['scu_sell_max_week']}\n"
        f"**SCU Sell Max Month:** {data['scu_sell_max_month']}\n"
        f"**SCU Sell Avg:** {data['scu_sell_avg']}\n"
        f"**SCU Sell Avg Week:** {data['scu_sell_avg_week']}\n"
        f"**SCU Sell Avg Month:** {data['scu_sell_avg_month']}\n"
        f"**SCU Sell Total:** {data['scu_sell_total']}\n"
        f"**SCU Sell Total Week:** {data['scu_sell_total_week']}\n"
        f"**SCU Sell Total Month:** {data['scu_sell_total_month']}\n"
        f"**SCU Sell Users:** {data['scu_sell_users']}\n"
        f"**SCU Sell Users Rows:** {data['scu_sell_users_rows']}\n"
        f"**Status Buy:** {data['status_buy']}\n"
        f"**Status Buy Min:** {data['status_buy_min']}\n"
        f"**Status Buy Min Week:** {data['status_buy_min_week']}\n"
        f"**Status Buy Min Month:** {data['status_buy_min_month']}\n"
        f"**Status Buy Max:** {data['status_buy_max']}\n"
        f"**Status Buy Max Week:** {data['status_buy_max_week']}\n"
        f"**Status Buy Max Month:** {data['status_buy_max_month']}\n"
        f"**Status Buy Avg:** {data['status_buy_avg']}\n"
        f"**Status Buy Avg Week:** {data['status_buy_avg_week']}\n"
        f"**Status Buy Avg Month:** {data['status_buy_avg_month']}\n"
        f"**Status Sell:** {data['status_sell']}\n"
        f"**Status Sell Min:** {data['status_sell_min']}\n"
        f"**Status Sell Min Week:** {data['status_sell_min_week']}\n"
        f"**Status Sell Min Month:** {data['status_sell_min_month']}\n"
        f"**Status Sell Max:** {data['status_sell_max']}\n"
        f"**Status Sell Max Week:** {data['status_sell_max_week']}\n"
        f"**Status Sell Max Month:** {data['status_sell_max_month']}\n"
        f"**Status Sell Avg:** {data['status_sell_avg']}\n"
        f"**Status Sell Avg Week:** {data['status_sell_avg_week']}\n"
        f"**Status Sell Avg Month:** {data['status_sell_avg_month']}\n"
        f"**Volatility Buy:** {data['volatility_buy']}\n"
        f"**Volatility Sell:** {data['volatility_sell']}\n"
        f"**CAX Score:** {data['cax_score']}\n"
        f"**Game Version:** {data['game_version']}\n"
        f"**Date Added:** {data['date_added']}\n"
        f"**Date Modified:** {data['date_modified']}\n"
        "-------------------------\n"
    )

@bot.command()
async def commodities_averages(ctx, id):
    try:
        int_id = int(id)
    except ValueError:
        await ctx.send("Invalid ID format. Please provide a valid integer ID.")
        return

    api_url = f'https://uexcorp.space/api/2.0/commodities_averages?id_commodity={int_id}'
    headers = {
        'Content-Type': 'application/json',
    }

    try:
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            try:
                data = response.json()

                if 'data' not in data or not data['data']:
                    await ctx.send("No data found for the given commodity ID.")
                    return


                for item in data['data']:
                    formatted_data = format_commodity_averages(item)
                    chunks = chunk_message(formatted_data)

                    for chunk in chunks:
                        await ctx.send(f"```json\n{chunk}\n```")
                        await asyncio.sleep(1)  # Add a delay between messages to avoid rate-limiting

            except json.JSONDecodeError:
                await ctx.send("Error: The API response is not in the expected JSON format.")
        elif response.status_code == 401:
            await ctx.send("Error: Unauthorized access. Check your API key.")
        else:
            await ctx.send(f"Error: Failed to retrieve averages. Status code: {response.status_code}")
            await ctx.send(f"Error details: {response.text}")
    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.command()
async def test(ctx):
    await ctx.send("Test command works!")

bot.run(bot_token)
