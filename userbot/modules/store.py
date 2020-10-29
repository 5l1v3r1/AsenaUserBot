# Copyright (C) 2020 Yusuf Usta.
#
# Licensed under the  GPL-3.0 License;
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta

import os
from telethon.tl.types import InputMessagesFilterDocument
from userbot.events import register
from userbot import BOT_USERNAME, PATTERNS, CMD_HELP, PLUGIN_CHANNEL_ID
import userbot.cmdhelp
from random import choice, sample
import importlib
import re

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("__plugin")

# ████████████████████████████████ #

# Plugin Mağazası
@register(outgoing=True, pattern="^.store ?(.*)")
@register(outgoing=True, pattern="^.ma[gğ]aza ?(.*)")
async def magaza(event):
    plugin = event.pattern_match.group(1)
    await event.edit('**🐺 Asena Plugin Mağazası**\n__Versiyon 1.0__\n\n`🔎 Plugin\'i arıyorum... Lütfen biraz bekle.`')
    split = plugin.split()
    if plugin == '':
        plugin = 'Son Yüklenen'
        plugins = await event.client.get_messages('@asenaplugin', limit=15, filter=InputMessagesFilterDocument)
    elif len(split) >= 1 and (split[0] == 'random' or split[0] == 'rastgele'):
        plugin = 'Rastgele'
        plugins = await event.client.get_messages('@asenaplugin', limit=None, filter=InputMessagesFilterDocument)
        plugins = sample(plugins, int(split[1]) if len(split) == 2 else 5)
    else:
        plugins = await event.client.get_messages('@asenaplugin', limit=None, search=plugin, filter=InputMessagesFilterDocument)
        random = await event.client.get_messages('@asenaplugin', limit=None, filter=InputMessagesFilterDocument)
        random = choice(random)
        random_file = random.file.name

    result = f'**🐺 Asena Plugin Mağazası**\n__Versiyon 1.0__\n\n**🔎 Arama:** `{plugin}`\n**🔢 Sonuçlar: __({len(plugins)})__**\n➖➖➖➖➖\n\n'
    
    if len(plugins) == 0:
        result += f'**Hiçbir şey bulamadım...**\n`{random_file}` __pluginine ne dersin?__'
    else:
        for plugin in plugins:
            plugin_lines = plugin.raw_text.splitlines()
            result += f'**⬇️ {plugin_lines[0]}** `({plugin.file.name})`**:** '
            if len(plugin_lines[2]) < 50:
                result += f'__{plugin_lines[2]}__'
            else:
                result += f'__{plugin_lines[2][:50]}...__'
            result += f'\n**ℹ️ Yüklemek için:** `{PATTERNS[:1]}sinstall {plugin.id}`\n➖➖➖➖➖\n'
    return await event.edit(result)

# Plugin Mağazası
@register(outgoing=True, pattern="^.sy[üu]kle ?(.*)")
@register(outgoing=True, pattern="^.sinstall ?(.*)")
async def sinstall(event):
    plugin = event.pattern_match.group(1)
    try:
        plugin = int(plugin)
    except:
        return await event.edit('**🐺 Asena Plugin Mağazası**\n__Versiyon 1.0__\n\n**⚠️ Hata:** `Lütfen sadece sayı yazın. Eğer Plugin aramak istiyorsanız .store komutunu kullanın.`')
    
    await event.edit('**🐺 Asena Plugin Mağazası**\n__Versiyon 1.0__\n\n`🔎 Plugin\'i getiriyorum... Lütfen biraz bekle.`')
    plugin = await event.client.get_messages('@asenaplugin', ids=plugin)
    await event.edit(f'**🐺 Asena Plugin Mağazası**\n__Versiyon 1.0__\n\n`✅ {plugin.file.name} plugini getirildi!`\n`⬇️ Plugini indiriyorum... Lütfen bekleyiniz.`')
    dosya = await plugin.download_media('./userbot/modules/')
    await event.edit(f'**🐺 Asena Plugin Mağazası**\n__Versiyon 1.0__\n\n`✅ {plugin.file.name} indirme başarılı!`\n`⬇️ Plugini yüklüyorum... Lütfen bekleyiniz.`')
    
    try:
        spec = importlib.util.spec_from_file_location(dosya, dosya)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    except Exception as e:
        os.remove("./userbot/modules/" + dosya)
        return await event.edit(f'**🐺 Asena Plugin Mağazası**\n__Versiyon 1.0__\n\n**⚠️ Hata:** `Plugin hatalı. {e}`\n**LÜTFEN BUNU ADMİNLERE BİLDİRİN!**')

    dosy = open(dosya, "r").read()
    if re.search(r"@tgbot\.on\(.*pattern=(r|)\".*\".*\)", dosy):
        komu = re.findall(r"\(.*pattern=(r|)\"(.*)\".*\)", dosy)
        komutlar = ""
        i = 0
        while i < len(komu):
            komut = komu[i][1]
            CMD_HELP["tgbot_" + komut] = f"{LANG['PLUGIN_DESC']} {komut}"
            komutlar += komut + " "
            i += 1
        await event.edit(LANG['PLUGIN_DOWNLOADED'] % komutlar)
    else:
        Pattern = re.findall(r"@register\(.*pattern=(r|)\"(.*)\".*\)", dosy)
        Komutlar = []

        if (not type(Pattern) == list) or (len(Pattern) < 1 or len(Pattern[0]) < 1):
            CMD_HELP[dosya] = LANG['PLUGIN_WITHOUT_DESC']
            return await event.edit(LANG['PLUGIN_DESCLESS'])
        else:
            if re.search(r'CmdHelp\(.*\)', dosy):
                cmdhelp = re.findall(r"CmdHelp\([\"'](.*)[\"']\)", dosy)[0]
                await plugin.forward_to(PLUGIN_CHANNEL_ID)
                return await event.edit(f'**🐺 Asena Plugin Mağazası**\n__Versiyon 1.0__\n\n**✅ Modül başarıyla yüklendi!**\n__ℹ️ Modülun komutları ve kullanım hakkında bilgi almak için__ `.asena {cmdhelp}` __yazınız.__')
            else:
                dosyaAdi = plugin.file.name.replace('.py', '')
                CmdHelp = userbot.cmdhelp.CmdHelp(dosyaAdi, False)
                # Komutları Alıyoruz #
                for Command in Pattern:
                    Command = Command[1]
                    if Command == '' or len(Command) <= 1:
                        continue
                    Komut = re.findall("([^.].*\w)(\W*)", Command)
                    if (len(Komut[0]) > 1) and (not Komut[0][1] == ''):
                        KomutStr = Command.replace(Komut[0][1], '')
                        if KomutStr[0] == '^':
                            KomutStr = KomutStr[1:]
                            if KomutStr[0] == '.':
                                KomutStr = PATTERNS[:1] + KomutStr[1:]
                        Komutlar.append(KomutStr)
                    else:
                        if Command[0] == '^':
                            KomutStr = Command[1:]
                            if KomutStr[0] == '.':
                                KomutStr = PATTERNS[:1] + KomutStr[1:]
                        else:
                            KomutStr = Command
                        Komutlar.append(KomutStr)

                # AsenaPY
                Asenapy = re.search('\"\"\"ASENAPY(.*)\"\"\"', dosy, re.DOTALL)
                if not Asenapy == None:
                    Asenapy = Asenapy.group(0)
                    for Satir in Asenapy.splitlines():
                        if (not '"""' in Satir) and (':' in Satir):
                            Satir = Satir.split(':')
                            Isim = Satir[0]
                            Deger = Satir[1][1:]

                            CmdHelp.set_file_info(Isim, Deger)
                            
                for Komut in Komutlar:
                    CmdHelp.add_command(Komut, None, 'Bu plugin dışarıdan yüklenmiştir. Herhangi bir açıklama tanımlanmamıştır.')
                CmdHelp.add()
                await plugin.forward_to(PLUGIN_CHANNEL_ID)
                return await event.edit(f'**🐺 Asena Plugin Mağazası**\n__Versiyon 1.0__\n\n**✅ Modül başarıyla yüklendi!**\n__ℹ️ Modülun komutları ve kullanım hakkında bilgi almak için` `.asena {dosyaAdi}` `yazınız.__')

userbot.cmdhelp.CmdHelp('store').add_command(
    'store', '<kelime>', 'Plugin kanalına son atılan Pluginleri getirir. Eğer kelime yazarsanız arama yapar.'
).add_command(
    'store random', '<sayı>', 'Pluginden kanalından rastgele plugin getirir.', 'store random 10'
).add_command(
    'sinstall', '<sayı>', 'Plugin kanalından direkt olarak Plugini yükler.'
).add()