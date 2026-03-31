import discord
from discord.ext import tasks
from datetime import time
import os

# ─────────────────────────────────────────
#  EINSTELLUNGEN – hier anpassen!
# ─────────────────────────────────────────
TOKEN      = os.environ.get("DISCORD_TOKEN", "DEIN_BOT_TOKEN_HIER")
CHANNEL_ID = 1488624091140460716          # <-- Ersetze mit deiner Channel-ID (int, keine Anführungszeichen)
ROLE_NAME  = "RaidPings"         # Exakt wie die Rolle in Discord heißt
MESSAGE    = "⚔️ Raid-Zeit! Macht euch bereit!"   # Nachricht nach dem Ping
# ─────────────────────────────────────────

# Alle 48 halben Stunden eines Tages (00:00, 00:30, 01:00, … 23:30)
PING_TIMES = [time(hour=h, minute=m) for h in range(24) for m in (0, 30)]

intents = discord.Intents.default()
client  = discord.Client(intents=intents)


@tasks.loop(time=PING_TIMES)
async def raid_ping():
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print(f"[FEHLER] Channel {CHANNEL_ID} nicht gefunden.")
        return

    role = discord.utils.get(channel.guild.roles, name=ROLE_NAME)
    if role is None:
        print(f"[FEHLER] Rolle '{ROLE_NAME}' nicht gefunden.")
        return

    await channel.send(f"{role.mention} {MESSAGE}")
    print(f"[OK] Gepingt um {discord.utils.utcnow().strftime('%H:%M UTC')}")


@client.event
async def on_ready():
    print(f"✅ Bot online als: {client.user} (ID: {client.user.id})")
    print(f"   Pinge alle 30 Minuten in Channel-ID: {CHANNEL_ID}")
    if not raid_ping.is_running():
        raid_ping.start()


client.run(TOKEN)
