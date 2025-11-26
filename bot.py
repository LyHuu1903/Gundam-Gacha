import os
import discord
from discord.ext import commands
import random

# =================== CẤU HÌNH BOT ===================

# Lấy token từ biến môi trường DISCORD_TOKEN (set trên Railway)
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    # In ra cảnh báo khi chạy local mà quên set env
    print("⚠️  Không tìm thấy DISCORD_TOKEN trong biến môi trường!")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =================== DỮ LIỆU GAME ===================

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

# players[user_id] = {
#   "gems": int,
#   "inventory": {card_id: count},
#   "stats": {"rolls": int, "UR": int, "SR": int, "R": int, "C": int}
# }
players = {}


def get_player(user):
    uid = user.id
    if uid not in players:
        players[uid] = {
            "gems": 0,
            "inventory": {},
            "stats": {"rolls": 0, "UR": 0, "SR": 0, "R": 0, "C": 0},
        }
    return players[uid]


def get_cards_by_rarity(rarity: str):
    return [c for c in CARD_POOL if c["rarity"] == rarity]


def roll_one_card():
    rarities = list(RARITY_RATES.keys())
    weights = [RARITY_RATES[r] for r in rarities]
    rarity = random.choices(rarities, weights=weights, k=1)[0]
    pool = get_cards_by_rarity(rarity)
    card = random.choice(pool)
    return card


def add_card_to_inventory(player, card_id: str, amount: int = 1):
    inv = player["inventory"]
    inv[card_id] = inv.get(card_id, 0) + amount


def format_card(card):
    return f"{RARITY_EMOJI[card['rarity']]} **{card['name']}** (`{card['id']}`)"


# =================== EVENT ===================

@bot.event
async def on_ready():
    print(f"Đăng nhập thành công: {bot.user} (ID: {bot.user.id})")
    await bot.change_presence(
        activity=discord.Game(name="Gundam Gacha | !start")
    )

# =================== LỆNH CƠ BẢN ===================

@bot.command()
async def start(ctx):
    """Tạo tài khoản & nhận 100 Gem lần đầu."""
    player = get_player(ctx.author)
    if (
        player["gems"] == 0
        and not player["inventory"]
        and player["stats"]["rolls"] == 0
    ):
        player["gems"] = 100
        await ctx.send(
            f"🎉 {ctx.author.mention} đã tham gia **Gundam Gacha**!\n"
            f"Bạn nhận được **100 Gem** khởi đầu. Dùng `!gacha` để quay thử."
        )
    else:
        await ctx.send(
            f"✅ {ctx.author.mention} bạn đã có tài khoản rồi. "
            f"Dùng `!balance` để xem Gem."
        )


@bot.command()
async def balance(ctx):
    player = get_player(ctx.author)
    await ctx.send(
        f"💰 {ctx.author.mention} hiện đang có **{player['gems']} Gem**."
    )


@bot.command()
@commands.cooldown(1, 86400, commands.BucketType.user)
async def daily(ctx):
    player = get_player(ctx.author)
    reward = 50
    player["gems"] += reward
    await ctx.send(
        f"📅 {ctx.author.mention} nhận **{reward} Gem** daily!\n"
        f"Tổng Gem: **{player['gems']}**"
    )


@daily.error
async def daily_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            f"⏳ Bạn đã nhận daily rồi, hãy quay lại sau **{error.retry_after:.0f} giây** nữa."
        )

# =================== GACHA ===================

@bot.command()
async def gacha(ctx, times: int = 1):
    if times < 1:
        await ctx.send("❌ Số lần quay phải >= 1.")
        return
    if times > 10:
        await ctx.send("⚠️ Chỉ được quay tối đa **10 lần** mỗi lệnh.")
        return

    player = get_player(ctx.author)
    cost_per_roll = 20
    total_cost = cost_per_roll * times

    if player["gems"] < total_cost:
        await ctx.send(
            f"❌ {ctx.author.mention} không đủ Gem! Cần **{total_cost} Gem** "
            f"nhưng bạn chỉ có **{player['gems']} Gem**."
        )
        return

    player["gems"] -= total_cost
    stats = player["stats"]
    stats["rolls"] += times

    results = []
    for _ in range(times):
        card = roll_one_card()
        results.append(card)
        add_card_to_inventory(player, card["id"], 1)
        stats[card["rarity"]] += 1

    lines = [format_card(c) for c in results]

    embed = discord.Embed(
        title=f"🎰 Gundam Gacha – Kết quả ({times}x)",
        description="\n".join(lines),
        color=discord.Color.purple()
    )
    embed.set_footer(
        text=f"{ctx.author.display_name} | Gem còn lại: {player['gems']}"
    )

    await ctx.send(content=f"{ctx.author.mention}", embed=embed)

# =================== BỘ SƯU TẬP & LIST ===================

@bot.command()
async def collection(ctx):
    player = get_player(ctx.author)
    inv = player["inventory"]

    if not inv:
        await ctx.send(
            f"🎒 {ctx.author.mention} chưa có card nào, thử `!gacha` đi!"
        )
        return

    card_map = {c["id"]: c for c in CARD_POOL}

    lines_ur, lines_sr, lines_r, lines_c = [], [], [], []

    for card_id, count in inv.items():
        card = card_map.get(card_id)
        if not card:
            continue
        line = f"{format_card(card)} x{count}"
        if card["rarity"] == "UR":
            lines_ur.append(line)
        elif card["rarity"] == "SR":
            lines_sr.append(line)
        elif card["rarity"] == "R":
            lines_r.append(line)
        else:
            lines_c.append(line)

    embed = discord.Embed(
        title=f"📚 Bộ sưu tập của {ctx.author.display_name}",
        color=discord.Color.blue()
    )

    if lines_ur:
        embed.add_field(name="🌈 Ultra Rare", value="\n".join(lines_ur[:10]), inline=False)
    if lines_sr:
        embed.add_field(name="💎 Super Rare", value="\n".join(lines_sr[:10]), inline=False)
    if lines_r:
        embed.add_field(name="✨ Rare", value="\n".join(lines_r[:10]), inline=False)
    if lines_c:
        embed.add_field(name="⭐ Common", value="\n".join(lines_c[:10]), inline=False)

    await ctx.send(embed=embed)


@bot.command()
async def cards(ctx):
    """Xem danh sách card có thể quay (tự chia nhỏ tránh > 2000 ký tự)."""
    lines = [format_card(c) for c in CARD_POOL]
    text = "🎴 **Các card có thể quay:**\n" + "\n".join(lines)

    chunk_size = 1900
    for i in range(0, len(text), chunk_size):
        await ctx.send(text[i:i + chunk_size])

# =================== PROFILE / SELL / TOP ===================

@bot.command()
async def profile(ctx):
    player = get_player(ctx.author)
    s = player["stats"]

    embed = discord.Embed(
        title=f"🧾 Gundam Gacha – Profile của {ctx.author.display_name}",
        color=discord.Color.gold()
    )
    embed.add_field(name="Gem", value=str(player["gems"]), inline=True)
    embed.add_field(name="Total Rolls", value=str(s["rolls"]), inline=True)
    embed.add_field(
        name="Rarity stats",
        value=(
            f"🌈 UR: **{s['UR']}**\n"
            f"💎 SR: **{s['SR']}**\n"
            f"✨ R: **{s['R']}**\n"
            f"⭐ C: **{s['C']}**"
        ),
        inline=False
    )

    await ctx.send(embed=embed)


@bot.command()
async def sell(ctx, card_id: str, amount: int = 1):
    card_id = card_id.upper()
    if amount < 1:
        await ctx.send("❌ Số lượng bán phải >= 1.")
        return

    player = get_player(ctx.author)
    inv = player["inventory"]

    if card_id not in inv or inv[card_id] < amount:
        await ctx.send(
            f"❌ {ctx.author.mention} không đủ card `{card_id}` để bán."
        )
        return

    card = next((c for c in CARD_POOL if c["id"] == card_id), None)
    if not card:
        await ctx.send("❌ Card ID không hợp lệ.")
        return

    rarity = card["rarity"]
    value_per = SELL_VALUES.get(rarity, 1)
    total_value = value_per * amount

    inv[card_id] -= amount
    if inv[card_id] <= 0:
        del inv[card_id]

    player["gems"] += total_value

    await ctx.send(
        f"💸 {ctx.author.mention} đã bán **{amount}x {card['name']}** "
        f"({rarity}) và nhận được **{total_value} Gem**.\n"
        f"Gem hiện tại: **{player['gems']}**"
    )


@bot.command()
async def top(ctx):
    if not players:
        await ctx.send("⚠️ Chưa có ai chơi Gundam Gacha. Dùng `!start` trước nhé!")
        return

    def score(pdata):
        s = pdata["stats"]
        return s["UR"] * 3 + s["SR"] * 2 + s["R"]

    sorted_players = sorted(
        players.items(),
        key=lambda kv: score(kv[1]),
        reverse=True
    )

    lines = []
    for rank, (uid, pdata) in enumerate(sorted_players[:10], start=1):
        s = pdata["stats"]
        lines.append(
            f"**#{rank}** <@{uid}> – "
            f"Điểm: **{score(pdata)}** "
            f"(UR: {s['UR']}, SR: {s['SR']}, R: {s['R']})"
        )

    embed = discord.Embed(
        title="🏆 Gundam Gacha – Leaderboard",
        description="\n".join(lines),
        color=discord.Color.dark_gold()
    )
    await ctx.send(embed=embed)

# =================== LỆNH LIỆT KÊ COMMAND ===================

@bot.command(name="commands")
async def commands_list(ctx):
    embed = discord.Embed(
        title="🤖 Gundam Gacha – Command List",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="🔰 Bắt đầu",
        value=(
            "`!start` – tạo tài khoản\n"
            "`!daily` – nhận Gem mỗi ngày\n"
            "`!balance` – xem số Gem hiện tại\n"
            "`!profile` – xem hồ sơ gacha của bạn"
        ),
        inline=False
    )

    embed.add_field(
        name="🎰 Gacha & Bộ sưu tập",
        value=(
            "`!gacha` hoặc `!gacha 10` – quay 1 / 10 lần\n"
            "`!collection` – xem bộ sưu tập card\n"
            "`!cards` – xem tất cả card có thể quay"
        ),
        inline=False
    )

    embed.add_field(
        name="💸 Bán & Xếp hạng",
        value=(
            "`!sell <CARD_ID> <SỐ_LƯỢNG>` – bán card lấy Gem\n"
            "`!top` – bảng xếp hạng người chơi"
        ),
        inline=False
    )

    embed.set_footer(text="Gõ tên lệnh như trên, không cần <>.")

    await ctx.send(embed=embed)

# =================== CHẠY BOT ===================

bot.run(TOKEN)
