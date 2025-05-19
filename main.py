import discord
from discord.ext import commands
import os

# Setup required intents
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# أسماء الرولات المستخدمة
ROLE_VERIFIED = "Verified"
ROLE_PENDING = "Pending Verification"

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_member_update(before, after):
    # التحقق من الرولات التي تمت إضافتها للعضو
    added_roles = [role for role in after.roles if role not in before.roles]
    for role in added_roles:
        if role.name == ROLE_VERIFIED:
            # إذا حصل العضو على "تم التحقق" نحذف "قيد التحقق"
            pending_role = discord.utils.get(after.guild.roles, name=ROLE_PENDING)
            if pending_role and pending_role in after.roles:
                try:
                    await after.remove_roles(pending_role)
                    print(f"✅ Removed '{ROLE_PENDING}' from {after.name}")
                except discord.Forbidden:
                    print("❌ لا يوجد صلاحيات كافية لإزالة الرول")
                except Exception as e:
                    print(f"⚠️ خطأ غير متوقع: {e}")

# تشغيل البوت باستخدام التوكن من المتغيرات السرية (Secrets)
token = os.getenv("TOKEN")
if not token:
    raise Exception("❌ لم يتم العثور على التوكن في Secrets")
bot.run(token)
