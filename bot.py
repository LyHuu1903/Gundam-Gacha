import os
import json
import random
import asyncio
from datetime import date, datetime, timedelta
import discord
from discord.ext import commands, tasks

# =====================================================
#   GUNDAM GACHA V2 - FULL SYSTEM
# =====================================================

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    print("⚠️ Không tìm thấy DISCORD_TOKEN trong biến môi trường!")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

DATA_FILE = "gundam_data.json"

players = {}
GLOBAL_STATS = {
    "rolls": 0,
    "UR": 0,
    "SR": 0,
    "R": 0,
    "C": 0,
}

# =====================================================
# LOAD & SAVE
# =====================================================

def load_data():
    global players, GLOBAL_STATS
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        new_players = {}
        for uid_str, pdata in data.get("players", {}).items():
            try:
                new_players[int(uid_str)] = pdata
            except:
                pass

        players = new_players or players
        GLOBAL_STATS.update(data.get("global_stats", {}))

        print("✅ Loaded saved data.")

    except FileNotFoundError:
        print("ℹ️ No save file found, starting fresh.")
    except Exception as e:
        print("⚠️ Error loading:", e)


def save_data():
    try:
        data = {
            "players": {str(uid): pdata for uid, pdata in players.items()},
            "global_stats": GLOBAL_STATS,
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    except Exception as e:
        print("⚠️ Error saving:", e)


@tasks.loop(seconds=30)
async def autosave():
    save_data()
    print("💾 Auto-saved data.")


# =====================================================
# PLAYER DATA SYSTEM
# =====================================================

def get_player(user):
    uid = user.id
    today = date.today().isoformat()

    if uid not in players:
        players[uid] = {
            "gems": 0,
            "inventory": {},

            "stats": {
                "rolls": 0,
                "UR": 0,
                "SR": 0,
                "R": 0,
                "C": 0,
            },

            "daily": {
                "date": today,
                "open": 0,
                "sell": 0,
                "sr": 0,
                "ur": 0,
                "duel": 0,
                "claimed": {},
            },

            "weekly": {
                "week_start": today,
                "open": 0,
                "sr": 0,
                "ur": 0,
                "duel": 0,
                "claimed": {},
            },

            "achievements": {},
        }

    return players[uid]


def reset_daily(player):
    today = date.today().isoformat()
    if player["daily"]["date"] != today:
        player["daily"] = {
            "date": today,
            "open": 0,
            "sell": 0,
            "sr": 0,
            "ur": 0,
            "duel": 0,
            "claimed": {},
        }


def reset_weekly(player):
    today = date.today()
    week_start = datetime.strptime(player["weekly"]["week_start"], "%Y-%m-%d").date()
    if today - week_start >= timedelta(days=7):
        player["weekly"] = {
            "week_start": today.isoformat(),
            "open": 0,
            "sr": 0,
            "ur": 0,
            "duel": 0,
            "claimed": {},
        }

# END OF PART 1
# =====================================================
# CARD POOL (RẤT NHIỀU CARD)
# =====================================================

CARD_POOL = [
    # ====== ULTRA RARE (UR) – HÀNG CỰC HIẾM ======
    {"id": "RX78",          "name": "RX-78-2 Gundam",                  "rarity": "UR"},
    {"id": "UNICORN",       "name": "RX-0 Unicorn Gundam",             "rarity": "UR"},
    {"id": "BANSHEE_N",     "name": "RX-0[N] Banshee Norn",            "rarity": "UR"},
    {"id": "FREEDOM",       "name": "ZGMF-X10A Freedom Gundam",        "rarity": "UR"},
    {"id": "STRIKEF",       "name": "ZGMF-X20A Strike Freedom",        "rarity": "UR"},
    {"id": "WINGZERO",      "name": "XXXG-00W0 Wing Zero Custom",      "rarity": "UR"},
    {"id": "GOD",           "name": "GF13-017NJII God Gundam",         "rarity": "UR"},
    {"id": "HI_NU",         "name": "RX-93-ν2 Hi-ν Gundam",            "rarity": "UR"},
    {"id": "00Q",           "name": "GN-0000QAN[T] 00 Qan[T]",         "rarity": "UR"},
    {"id": "BARBATOS_L",    "name": "ASW-G-08 Barbatos Lupus Rex",     "rarity": "UR"},

    # ====== SUPER RARE (SR) – MAIN, ACE, BOSS ======
    {"id": "ASTRAY_RED",    "name": "MBF-P02 Astray Red Frame",        "rarity": "SR"},
    {"id": "ASTRAY_BLUE",   "name": "MBF-P03 Astray Blue Frame",       "rarity": "SR"},
    {"id": "BARBATOS",      "name": "ASW-G-08 Gundam Barbatos",        "rarity": "SR"},
    {"id": "EXIA",          "name": "GN-001 Gundam Exia",              "rarity": "SR"},
    {"id": "EXIA_R2",       "name": "GN-001REII Exia Repair II",       "rarity": "SR"},
    {"id": "DESTINY",       "name": "ZGMF-X42S Destiny Gundam",        "rarity": "SR"},
    {"id": "INFINITE_J",    "name": "ZGMF-X19A Infinite Justice",      "rarity": "SR"},
    {"id": "RAISER00",      "name": "GN-0000+GNR-010 00 Raiser",       "rarity": "SR"},
    {"id": "SAZABI",        "name": "MSN-04 Sazabi",                   "rarity": "SR"},
    {"id": "SINANJU",       "name": "MSN-06S Sinanju",                 "rarity": "SR"},
    {"id": "STRIKE_NOIR",   "name": "GAT-X105E Strike Noir",           "rarity": "SR"},
    {"id": "AGE1",          "name": "AGE-1 Gundam AGE-1 Normal",       "rarity": "SR"},
    {"id": "AGE2",          "name": "AGE-2 Gundam AGE-2 Normal",       "rarity": "SR"},
    {"id": "EPYON",         "name": "OZ-13MS Gundam Epyon",            "rarity": "SR"},
    {"id": "TURN_A",        "name": "System-∀99 ∀ Gundam",             "rarity": "SR"},
    {"id": "FA_ZZ",         "name": "FA-010S Full Armor ZZ Gundam",    "rarity": "SR"},
    {"id": "ALEX",          "name": "RX-78NT-1 Gundam NT-1 'Alex'",    "rarity": "SR"},
    {"id": "GP01FB",        "name": "RX-78GP01Fb Zephyranthes FB",     "rarity": "SR"},

    # ====== RARE (R) – HÀNG MẠNH, HAY RA ======
    {"id": "ZAKU2",         "name": "MS-06 Zaku II",                   "rarity": "R"},
    {"id": "ZAKU2_S",       "name": "MS-06S Char's Zaku II",           "rarity": "R"},
    {"id": "GM",            "name": "RGM-79 GM",                       "rarity": "R"},
    {"id": "GOUF",          "name": "MS-07B Gouf",                     "rarity": "R"},
    {"id": "DOM",           "name": "MS-09 Dom",                       "rarity": "R"},
    {"id": "DOM_TROPEN",    "name": "MS-09F Dom Tropen",               "rarity": "R"},
    {"id": "GUNTANK",       "name": "RX-75 Guntank",                   "rarity": "R"},
    {"id": "GUNCANNON",     "name": "RX-77-2 Guncannon",               "rarity": "R"},
    {"id": "GELGOOG",       "name": "MS-14A Gelgoog",                  "rarity": "R"},
    {"id": "GM_SNIPER2",    "name": "RGM-79SP GM Sniper II",           "rarity": "R"},
    {"id": "JEGAN",         "name": "RGM-89 Jegan",                    "rarity": "R"},
    {"id": "GEARA_ZULU",    "name": "AMS-129 Geara Zulu",              "rarity": "R"},
    {"id": "HY_GOGG",       "name": "MSM-03C Hy-Gogg",                 "rarity": "R"},
    {"id": "ACGUY",         "name": "MSM-04 Acguy",                    "rarity": "R"},
    {"id": "GM_COMMAND",    "name": "RGM-79G GM Command",              "rarity": "R"},
    {"id": "GM_COLD",       "name": "RGM-79D GM Cold Districts",       "rarity": "R"},
    {"id": "ZAKU_SNIPER",   "name": "MS-05L Zaku I Sniper",            "rarity": "R"},
    {"id": "LEO",           "name": "OZ-06MS Leo (Custom Colors)",     "rarity": "R"},
    {"id": "GINN_H",        "name": "ZGMF-1017 GINN High-Maneuver",    "rarity": "R"},
    {"id": "AHEAD",         "name": "GNX-704T Ahead",                  "rarity": "R"},

    # ====== COMMON (C) – LÍNH, MASS PRODUCED ======
    {"id": "BALL",          "name": "RB-79 Ball",                      "rarity": "C"},
    {"id": "ZAKU1",         "name": "MS-05B Zaku I",                   "rarity": "C"},
    {"id": "MAGELLA",       "name": "HT-01B Magella Attack",           "rarity": "C"},
    {"id": "LEO_MASS",      "name": "OZ-06MS Leo",                     "rarity": "C"},
    {"id": "GINN",          "name": "ZGMF-1017 GINN",                  "rarity": "C"},
    {"id": "AEU_ENACT",     "name": "AEU-09Y812 Enact",                "rarity": "C"},
    {"id": "TIEREN",        "name": "MSJ-06II-A Tieren",               "rarity": "C"},
    {"id": "FLAG",          "name": "SVMS-01 Union Flag",              "rarity": "C"},
    {"id": "GM_TRAINING",   "name": "RGM-79T GM Trainer",              "rarity": "C"},
    {"id": "ZOLA_MASS",     "name": "ZM-S08G Zolo (Mass)",             "rarity": "C"},
    {"id": "ZAKU_TANK",     "name": "MS-06V Zaku Tank",                "rarity": "C"},
    {"id": "GUNTANK_MASS",  "name": "Mass-Production Guntank",         "rarity": "C"},
    {"id": "GM_CANNON",     "name": "RGC-80 GM Cannon",                "rarity": "C"},
    {"id": "GM_CUSTOM",     "name": "RGM-79N GM Custom",               "rarity": "C"},
    {"id": "GM_II",         "name": "RMS-179 GM II",                   "rarity": "C"},
    {"id": "GM_III",        "name": "RGM-86R GM III",                  "rarity": "C"},
    {"id": "DRAGOON",       "name": "OZ-02MD Virgo (Basic)",           "rarity": "C"},
    {"id": "BUCUE",         "name": "TMF/A-802 BuCUE",                 "rarity": "C"},
    {"id": "N_DAGGER",      "name": "GAT-01A1+AQM/E-A4E N Dagger",     "rarity": "C"},
    {"id": "GN_X",          "name": "GN-X (Standard)",                 "rarity": "C"},
]

RARITY_RATES = {
    "UR": 5,
    "SR": 10,
    "R": 25,
    "C": 60,
}

RARITY_EMOJI = {
    "UR": "🌈⭐⭐⭐⭐",
    "SR": "💎⭐⭐⭐",
    "R": "✨⭐⭐",
    "C": "⭐",
}

SELL_VALUES = {
    "UR": 100,
    "SR": 40,
    "R": 10,
    "C": 3,
}

RARITY_POWER = {
    "UR": 4,
    "SR": 3,
    "R": 2,
    "C": 1,
}


# =====================================================
# UTILS
# =====================================================

def get_cards_by_rarity(rarity):
    return [c for c in CARD_POOL if c["rarity"] == rarity]


def roll_one_card():
    rarities = list(RARITY_RATES.keys())
    weights = [RARITY_RATES[r] for r in rarities]
    rarity = random.choices(rarities, weights=weights, k=1)[0]
    pool = get_cards_by_rarity(rarity)
    return random.choice(pool)


def add_card(player, card):
    inv = player["inventory"]
    inv[card["id"]] = inv.get(card["id"], 0) + 1


def format_card(card):
    return f"{RARITY_EMOJI[card['rarity']]} **{card['name']}** (`{card['id']}`)"


def get_random_card(player):
    pool = []
    for cid, count in player["inventory"].items():
        pool += [cid] * count
    if not pool:
        return None
    cid = random.choice(pool)
    return next((c for c in CARD_POOL if c["id"] == cid), None)


# =====================================================
# BOT EVENTS
# =====================================================

@bot.event
async def on_ready():
    print(f"🤖 Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game("Gundam Gacha | !start"))
    autosave.start()


# =====================================================
# BASIC COMMANDS
# =====================================================

@bot.command()
async def start(ctx):
    p = get_player(ctx.author)
    if p["gems"] == 0 and p["stats"]["rolls"] == 0:
        p["gems"] = 100
        await ctx.send(f"🎉 {ctx.author.mention} đã vào **Gundam Gacha**!\nBạn nhận được **100 Gem**.")
        save_data()
    else:
        await ctx.send("✅ Bạn đã có tài khoản rồi.")


@bot.command()
async def balance(ctx):
    p = get_player(ctx.author)
    await ctx.send(f"💰 {ctx.author.mention} hiện có **{p['gems']} Gem**.")


@bot.command()
@commands.cooldown(1, 86400, commands.BucketType.user)
async def daily(ctx):
    p = get_player(ctx.author)
    p["gems"] += 100
    await ctx.send(f"📅 Bạn nhận được **100 Gem Daily**!\nGem hiện tại: **{p['gems']}**")
    save_data()


@daily.error
async def daily_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏳ Hãy quay lại sau **{error.retry_after:.0f} giây**.")


# =====================================================
# GACHA (HIỆU ỨNG + 1 LẦN/LỆNH)
# =====================================================

@bot.command()
async def gacha(ctx):
    p = get_player(ctx.author)

    cost = 20
    if p["gems"] < cost:
        await ctx.send("❌ Không đủ Gem!")
        return

    p["gems"] -= cost
    p["stats"]["rolls"] += 1
    GLOBAL_STATS["rolls"] += 1

    # DAILY + WEEKLY
    reset_daily(p)
    reset_weekly(p)
    p["daily"]["open"] += 1
    p["weekly"]["open"] += 1

    # EFFECT 1
    msg = await ctx.send(f"{ctx.author.mention} 🎰 **Đang quay...**")
    await asyncio.sleep(0.5)
    await msg.edit(content=f"{ctx.author.mention} 🎰 **Đang quay... ✨**")
    await asyncio.sleep(0.5)
    await msg.edit(content=f"{ctx.author.mention} 🎰 **Đang quay... 🌈**")
    await asyncio.sleep(0.5)

    # ROLL
    card = roll_one_card()
    add_card(p, card)

    rarity = card["rarity"]
    p["stats"][rarity] += 1
    GLOBAL_STATS[rarity] += 1

    # DAILY count rare
    if rarity == "SR":
        p["daily"]["sr"] += 1
        p["weekly"]["sr"] += 1
    if rarity == "UR":
        p["daily"]["ur"] += 1
        p["weekly"]["ur"] += 1

    embed = discord.Embed(
        title="🎰 Gundam Gacha – Kết quả",
        description=format_card(card),
        color=discord.Color.purple(),
    )
    embed.set_footer(text=f"Gem còn lại: {p['gems']}")

    await msg.edit(content=f"{ctx.author.mention}", embed=embed)
    save_data()


# =====================================================
# COLLECTION
# =====================================================

@bot.command()
async def collection(ctx):
    p = get_player(ctx.author)
    inv = p["inventory"]
    if not inv:
        await ctx.send("🎒 Bạn chưa có card nào!")
        return

    by_r = {"UR": [], "SR": [], "R": [], "C": []}
    for card in CARD_POOL:
        if card["id"] in inv:
            by_r[card["rarity"]].append(f"{format_card(card)} x{inv[card['id']]}")

    embed = discord.Embed(
        title=f"📚 Bộ sưu tập của {ctx.author.display_name}",
        color=discord.Color.blue(),
    )

    for rarity in ["UR", "SR", "R", "C"]:
        if by_r[rarity]:
            embed.add_field(
                name=f"{RARITY_EMOJI[rarity]} {rarity}",
                value="\n".join(by_r[rarity]),
                inline=False,
            )

    await ctx.send(embed=embed)


@bot.command()
async def cards(ctx):
    text = "🎴 **Danh sách card:**\n" + "\n".join(format_card(c) for c in CARD_POOL)

    if len(text) > 1900:
        chunks = [text[i:i+1900] for i in range(0, len(text), 1900)]
        for c in chunks:
            await ctx.send(c)
    else:
        await ctx.send(text)


# =====================================================
# SELL CARD
# =====================================================

@bot.command()
async def sell(ctx, card_id: str, amount: int = 1):
    p = get_player(ctx.author)
    card_id = card_id.upper()

    if amount < 1:
        await ctx.send("❌ Số lượng không hợp lệ.")
        return

    if card_id not in p["inventory"] or p["inventory"][card_id] < amount:
        await ctx.send("❌ Bạn không có đủ card.")
        return

    card = next((c for c in CARD_POOL if c["id"] == card_id), None)
    if not card:
        await ctx.send("❌ Card ID không hợp lệ.")
        return

    rarity = card["rarity"]
    reward = SELL_VALUES[rarity] * amount

    p["inventory"][card_id] -= amount
    if p["inventory"][card_id] <= 0:
        del p["inventory"][card_id]

    p["gems"] += reward
    p["daily"]["sell"] += amount

    await ctx.send(
        f"💸 Bán **{amount}x {card['name']}** và nhận **{reward} Gem**!\n"
        f"Gem hiện tại: **{p['gems']}**"
    )

    save_data()

# END OF PART 2
# =====================================================
# QUEST CONFIG
# =====================================================

DAILY_QUESTS = [
    {"key": "open_5", "label": "Quay 5 lần gacha", "target": 5, "reward": 80},
    {"key": "open_10", "label": "Quay 10 lần gacha", "target": 10, "reward": 150},
    {"key": "open_20", "label": "Quay 20 lần gacha", "target": 20, "reward": 300},
    {"key": "sell_3", "label": "Bán 3 card", "target": 3, "reward": 40},
    {"key": "sr_1", "label": "Nhận 1 SR", "target": 1, "reward": 70},
    {"key": "ur_1", "label": "Nhận 1 UR", "target": 1, "reward": 150},
    {"key": "duel_1", "label": "Thắng 1 trận đấu", "target": 1, "reward": 100},
    {"key": "duel_3", "label": "Thắng 3 trận đấu", "target": 3, "reward": 250},
]


WEEKLY_QUESTS = [
    {"key": "open_100", "label": "Quay 100 lần gacha", "target": 100, "reward": 600},
    {"key": "sr_10", "label": "Nhận 10 SR", "target": 10, "reward": 500},
    {"key": "ur_3", "label": "Nhận 3 UR", "target": 3, "reward": 1200},
    {"key": "duel_10", "label": "Thắng 10 trận đấu", "target": 10, "reward": 1000},
]


ACHIEVEMENTS = [
    {"key": "roll_100", "label": "Quay tổng 100 lần", "check": lambda p: p["stats"]["rolls"] >= 100, "reward": 200},
    {"key": "roll_1000", "label": "Quay tổng 1000 lần", "check": lambda p: p["stats"]["rolls"] >= 1000, "reward": 2000},
    {"key": "ur_master", "label": "Sở hữu 10 UR", 
        "check": lambda p: sum(p["inventory"].get(c["id"],0) for c in CARD_POOL if c["rarity"]=="UR") >= 10,
        "reward": 1500},
    {"key": "collector", "label": "Sở hữu 50 card khác nhau",
        "check": lambda p: len(p["inventory"]) >= 50,
        "reward": 1000},
    {"key": "rich", "label": "Có 5000 Gem", "check": lambda p: p["gems"] >= 5000, "reward": 500},
]


# =====================================================
# QUEST VIEW COMMANDS
# =====================================================

@bot.command()
async def quests(ctx):
    p = get_player(ctx.author)
    reset_daily(p)

    embed = discord.Embed(
        title="📜 Nhiệm vụ ngày",
        color=discord.Color.green()
    )

    for q in DAILY_QUESTS:
        key = q["key"]
        label = q["label"]
        target = q["target"]
        reward = q["reward"]

        # progress
        if key.startswith("open"):
            progress = p["daily"]["open"]
        elif key.startswith("sell"):
            progress = p["daily"]["sell"]
        elif key.startswith("sr"):
            progress = p["daily"]["sr"]
        elif key.startswith("ur"):
            progress = p["daily"]["ur"]
        elif key.startswith("duel"):
            progress = p["daily"]["duel"]
        else:
            progress = 0

        claimed = p["daily"]["claimed"].get(key, False)

        status = "🎁 ĐÃ NHẬN" if claimed else ("✅ XONG" if progress >= target else "⏳ Đang làm")

        embed.add_field(
            name=f"{label}",
            value=f"Tiến độ: **{progress}/{target}**\nPhần thưởng: **+{reward} Gem**\nTrạng thái: {status}",
            inline=False,
        )

    embed.set_footer(text="Dùng !claim daily để nhận thưởng đã hoàn thành.")
    await ctx.send(embed=embed)



@bot.command()
async def weekly(ctx):
    p = get_player(ctx.author)
    reset_weekly(p)

    embed = discord.Embed(
        title="📅 Nhiệm vụ tuần",
        color=discord.Color.blue()
    )

    for q in WEEKLY_QUESTS:
        key = q["key"]
        label = q["label"]
        target = q["target"]
        reward = q["reward"]

        if key.startswith("open"):
            progress = p["weekly"]["open"]
        elif key.startswith("sr"):
            progress = p["weekly"]["sr"]
        elif key.startswith("ur"):
            progress = p["weekly"]["ur"]
        elif key.startswith("duel"):
            progress = p["weekly"]["duel"]
        else:
            progress = 0

        claimed = p["weekly"]["claimed"].get(key, False)

        status = "🎁 ĐÃ NHẬN" if claimed else ("✅ XONG" if progress >= target else "⏳ Đang làm")

        embed.add_field(
            name=label,
            value=f"Tiến độ: **{progress}/{target}**\nThưởng: **+{reward} Gem**\nTrạng thái: {status}",
            inline=False,
        )

    embed.set_footer(text="Dùng !claim weekly để nhận nhiệm vụ tuần.")
    await ctx.send(embed=embed)



@bot.command()
async def achievements(ctx):
    p = get_player(ctx.author)

    embed = discord.Embed(
        title="🏆 Thành tựu",
        color=discord.Color.gold()
    )

    for a in ACHIEVEMENTS:
        key = a["key"]
        label = a["label"]
        reward = a["reward"]
        unlocked = a["check"](p)
        claimed = p["achievements"].get(key, False)

        status = "🎁 ĐÃ NHẬN" if claimed else ("🏅 MỞ KHÓA" if unlocked else "🔒 Chưa đạt")

        embed.add_field(
            name=label,
            value=f"Thưởng: **+{reward} Gem**\nTrạng thái: {status}",
            inline=False,
        )

    embed.set_footer(text="Dùng !claim achievement để nhận thành tựu mở khóa.")
    await ctx.send(embed=embed)


# =====================================================
# CLAIM COMMAND
# =====================================================

@bot.command()
async def claim(ctx, type: str):
    p = get_player(ctx.author)

    if type == "daily":
        reset_daily(p)
        total = 0

        for q in DAILY_QUESTS:
            key = q["key"]
            target = q["target"]
            reward = q["reward"]

            # progress
            if key.startswith("open"):
                progress = p["daily"]["open"]
            elif key.startswith("sell"):
                progress = p["daily"]["sell"]
            elif key.startswith("sr"):
                progress = p["daily"]["sr"]
            elif key.startswith("ur"):
                progress = p["daily"]["ur"]
            elif key.startswith("duel"):
                progress = p["daily"]["duel"]
            else:
                progress = 0

            if progress >= target and not p["daily"]["claimed"].get(key, False):
                p["daily"]["claimed"][key] = True
                total += reward

        if total == 0:
            await ctx.send("⏳ Chưa có nhiệm vụ ngày để nhận.")
        else:
            p["gems"] += total
            await ctx.send(f"🎁 Nhận được **{total} Gem** từ nhiệm vụ ngày!")
            save_data()
        return


    elif type == "weekly":
        reset_weekly(p)
        total = 0

        for q in WEEKLY_QUESTS:
            key = q["key"]
            target = q["target"]
            reward = q["reward"]

            if key.startswith("open"):
                progress = p["weekly"]["open"]
            elif key.startswith("sr"):
                progress = p["weekly"]["sr"]
            elif key.startswith("ur"):
                progress = p["weekly"]["ur"]
            elif key.startswith("duel"):
                progress = p["weekly"]["duel"]
            else:
                progress = 0

            if progress >= target and not p["weekly"]["claimed"].get(key, False):
                p["weekly"]["claimed"][key] = True
                total += reward

        if total == 0:
            await ctx.send("⏳ Không có nhiệm vụ tuần để nhận.")
        else:
            p["gems"] += total
            await ctx.send(f"🎁 Nhận **{total} Gem** từ nhiệm vụ tuần!")
            save_data()
        return


    elif type == "achievement":
        total = 0

        for a in ACHIEVEMENTS:
            key = a["key"]
            reward = a["reward"]
            if a["check"](p) and not p["achievements"].get(key, False):
                p["achievements"][key] = True
                total += reward

        if total == 0:
            await ctx.send("⏳ Không có thành tựu để nhận.")
        else:
            p["gems"] += total
            await ctx.send(f"🏆 Nhận **{total} Gem** từ thành tựu!")
            save_data()

        return

    else:
        await ctx.send("❌ Sai cú pháp. Dùng:\n`!claim daily`\n`!claim weekly`\n`!claim achievement`")



# =====================================================
# DUEL SYSTEM
# =====================================================

@bot.command()
async def duel(ctx, opponent: discord.Member, bet: int = 0):
    if opponent.id == ctx.author.id:
        await ctx.send("❌ Bạn không thể tự đấu với chính mình.")
        return

    p1 = get_player(ctx.author)
    p2 = get_player(opponent)

    # check inventory
    if not p1["inventory"]:
        await ctx.send("❌ Bạn chưa có card để đấu.")
        return
    if not p2["inventory"]:
        await ctx.send("❌ Đối thủ không có card để đấu.")
        return

    # bet check
    if bet < 0:
        await ctx.send("❌ Tiền cược không hợp lệ.")
        return
    if bet > 0:
        if p1["gems"] < bet:
            await ctx.send("❌ Bạn không đủ Gem để cược.")
            return
        if p2["gems"] < bet:
            await ctx.send("❌ Đối thủ không đủ Gem để cược.")
            return

        p1["gems"] -= bet
        p2["gems"] -= bet

    c1 = get_random_card(p1)
    c2 = get_random_card(p2)

    base1 = RARITY_POWER[c1["rarity"]]
    base2 = RARITY_POWER[c2["rarity"]]

    roll1 = random.randint(0, 3)
    roll2 = random.randint(0, 3)

    power1 = base1 + roll1
    power2 = base2 + roll2

    # update stats daily + weekly
    if power1 > power2:
        winner = ctx.author
        p1["daily"]["duel"] += 1
        p1["weekly"]["duel"] += 1
    elif power2 > power1:
        winner = opponent
        p2["daily"]["duel"] += 1
        p2["weekly"]["duel"] += 1
    else:
        winner = None  # draw

    embed = discord.Embed(
        title="🤺 Trận đấu Gundam",
        color=discord.Color.red()
    )
    embed.add_field(
        name=f"{ctx.author.display_name}",
        value=f"Card: {format_card(c1)}\nSức mạnh: **{power1}** (roll: {roll1})",
        inline=False
    )
    embed.add_field(
        name=f"{opponent.display_name}",
        value=f"Card: {format_card(c2)}\nSức mạnh: **{power2}** (roll: {roll2})",
        inline=False
    )

    if winner is None:
        embed.add_field(name="Kết quả", value="⚔️ **HÒA**! Hoàn lại cược.", inline=False)
        if bet > 0:
            p1["gems"] += bet
            p2["gems"] += bet
    else:
        if bet > 0:
            reward = bet * 2
            players[winner.id]["gems"] += reward
            embed.add_field(name="Kết quả", value=f"🏆 {winner.mention} thắng và nhận **{reward} Gem**!", inline=False)
        else:
            embed.add_field(name="Kết quả", value=f"🏆 {winner.mention} thắng!", inline=False)

    await ctx.send(embed=embed)
    save_data()


# =====================================================
# COMMAND LIST
# =====================================================

@bot.command(name="commands")
async def commands_list(ctx):
    embed = discord.Embed(
        title="🤖 Gundam Gacha – Danh sách lệnh",
        color=discord.Color.cyan()
    )

    embed.add_field(name="🔰 Cơ bản",
        value="`!start`\n`!balance`\n`!daily`\n`!commands`",
        inline=False)

    embed.add_field(name="🎰 Gacha & Card",
        value="`!gacha`\n`!collection`\n`!cards`\n`!sell <id> <sl>`",
        inline=False)

    embed.add_field(name="📜 Nhiệm vụ",
        value="`!quests`\n`!weekly`\n`!achievements`\n`!claim daily`\n`!claim weekly`\n`!claim achievement`",
        inline=False)

    embed.add_field(name="🤺 Đấu",
        value="`!duel @user [cược]`",
        inline=False)

    await ctx.send(embed=embed)


# =====================================================
# RUN BOT
# =====================================================

load_data()
bot.run(TOKEN)

# END OF PART 3
