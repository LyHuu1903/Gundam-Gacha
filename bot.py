import os
import discord
from discord.ext import commands
import random
from datetime import date  # dùng cho hệ thống quest

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

# Sức mạnh base theo độ hiếm (dùng cho duel)
RARITY_POWER = {
    "UR": 4,
    "SR": 3,
    "R": 2,
    "C": 1,
}

# players[user_id] = {
#   "gems": int,
#   "inventory": {card_id: count},
#   "stats": {"rolls": int, "UR": int, "SR": int, "R": int, "C": int},
#   "quests": {"date": "YYYY-MM-DD", "gacha_rolls": int, "claimed": bool}
# }
players = {}

# Thống kê toàn server
GLOBAL_STATS = {
    "rolls": 0,
    "UR": 0,
    "SR": 0,
    "R": 0,
    "C": 0,
}


def get_player(user):
    """Lấy / tạo player, đảm bảo luôn có trường quests."""
    uid = user.id
    today = date.today().isoformat()

    if uid not in players:
        players[uid] = {
            "gems": 0,
            "inventory": {},
            "stats": {"rolls": 0, "UR": 0, "SR": 0, "R": 0, "C": 0},
            "quests": {
                "date": today,
                "gacha_rolls": 0,
                "claimed": False,
            },
        }

    player = players[uid]

    # Player cũ chưa có field quests thì bổ sung
    if "quests" not in player:
        player["quests"] = {
            "date": today,
            "gacha_rolls": 0,
            "claimed": False,
        }

    return player


def reset_quests_if_new_day(player):
    """Nếu qua ngày mới thì reset nhiệm vụ ngày."""
    today = date.today().isoformat()
    q = player["quests"]
    if q["date"] != today:
        q["date"] = today
        q["gacha_rolls"] = 0
        q["claimed"] = False


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


def get_random_card_from_inventory(player):
    """Chọn ngẫu nhiên 1 card từ inventory của player."""
    inv = player["inventory"]
    pool = []
    for card_id, count in inv.items():
        pool.extend([card_id] * count)

    if not pool:
        return None

    chosen_id = random.choice(pool)
    card = next((c for c in CARD_POOL if c["id"] == chosen_id), None)
    return card


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

    # Trừ gem + cập nhật stats
    player["gems"] -= total_cost
    stats = player["stats"]
    stats["rolls"] += times

    # Cập nhật tiến độ quest ngày
    reset_quests_if_new_day(player)
    player["quests"]["gacha_rolls"] += times

    # Cập nhật global stats
    GLOBAL_STATS["rolls"] += times

    results = []
    for _ in range(times):
        card = roll_one_card()
        results.append(card)
        add_card_to_inventory(player, card["id"], 1)
        stats[card["rarity"]] += 1
        GLOBAL_STATS[card["rarity"]] += 1

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

# =================== QUEST NGÀY ===================

@bot.command(name="quests")
async def quests_cmd(ctx):
    """Xem nhiệm vụ ngày để kiếm Gem."""
    player = get_player(ctx.author)
    reset_quests_if_new_day(player)
    q = player["quests"]

    target = 10     # cần quay 10 lần
    reward = 50     # thưởng 50 Gem
    progress = q["gacha_rolls"]
    done = progress >= target
    claimed = q["claimed"]

    status = "✅ ĐÃ HOÀN THÀNH" if done else "⏳ Đang làm"
    if done and claimed:
        status += " – 🎁 ĐÃ NHẬN THƯỞNG"

    embed = discord.Embed(
        title="📜 Nhiệm vụ ngày – Gundam Gacha",
        color=discord.Color.green()
    )
    embed.add_field(
        name="Nhiệm vụ 1: Quay gacha",
        value=(
            f"Quay **{target} lần gacha** trong hôm nay.\n"
            f"Tiến độ: **{progress}/{target}**\n"
            f"Trạng thái: {status}\n"
            f"Phần thưởng: **+{reward} Gem** (dùng `!questclaim` để nhận)"
        ),
        inline=False
    )

    await ctx.send(embed=embed)


@bot.command()
async def questclaim(ctx):
    """Nhận thưởng nhiệm vụ ngày (nếu đủ điều kiện)."""
    player = get_player(ctx.author)
    reset_quests_if_new_day(player)
    q = player["quests"]

    target = 10
    reward = 50

    if q["claimed"]:
        await ctx.send(
            f"✅ {ctx.author.mention} hôm nay bạn đã nhận thưởng nhiệm vụ rồi, "
            "hãy quay lại vào ngày mai nhé!"
        )
        return

    if q["gacha_rolls"] < target:
        await ctx.send(
            f"⏳ {ctx.author.mention} bạn chưa hoàn thành nhiệm vụ.\n"
            f"Hãy quay thêm gacha (hiện tại **{q['gacha_rolls']}/{target}**)."
        )
        return

    q["claimed"] = True
    player["gems"] += reward

    await ctx.send(
        f"🎁 {ctx.author.mention} nhận **{reward} Gem** từ nhiệm vụ ngày!\n"
        f"Gem hiện tại: **{player['gems']}**"
    )

# =================== TÍNH NĂNG MỚI: GIFT / REROLL / CARDINFO / GLOBAL STATS ===================

@bot.command()
async def gift(ctx, member: discord.Member, amount: int):
    """
    Chuyển Gem cho người khác.
    Ví dụ: !gift @TênNgườiNhận 50
    """
    if amount <= 0:
        await ctx.send("❌ Số Gem chuyển phải > 0.")
        return

    if member.id == ctx.author.id:
        await ctx.send("❌ Bạn không thể tự chuyển Gem cho chính mình.")
        return

    sender = get_player(ctx.author)
    receiver = get_player(member)

    if sender["gems"] < amount:
        await ctx.send(
            f"❌ {ctx.author.mention} không đủ Gem để chuyển.\n"
            f"Gem hiện tại: **{sender['gems']}**"
        )
        return

    sender["gems"] -= amount
    receiver["gems"] += amount

    await ctx.send(
        f"💳 {ctx.author.mention} đã chuyển **{amount} Gem** cho {member.mention}.\n"
        f"Gem của bạn còn: **{sender['gems']}**"
    )


@bot.command()
async def reroll(ctx, card_id: str):
    """
    Đổi 1 card sang 1 card random cùng độ hiếm (tốn Gem).
    Ví dụ: !reroll ZAKU2
    """
    card_id = card_id.upper()
    cost = 30  # giá reroll

    player = get_player(ctx.author)
    inv = player["inventory"]

    if card_id not in inv or inv[card_id] < 1:
        await ctx.send(
            f"❌ {ctx.author.mention} không có card `{card_id}` để reroll."
        )
        return

    if player["gems"] < cost:
        await ctx.send(
            f"❌ {ctx.author.mention} không đủ Gem để reroll (cần **{cost} Gem**).\n"
            f"Gem hiện tại: **{player['gems']}**"
        )
        return

    old_card = next((c for c in CARD_POOL if c["id"] == card_id), None)
    if not old_card:
        await ctx.send("❌ Card ID không hợp lệ.")
        return

    rarity = old_card["rarity"]
    same_rarity_cards = [c for c in CARD_POOL if c["rarity"] == rarity and c["id"] != card_id]

    if not same_rarity_cards:
        await ctx.send("⚠️ Không có card nào khác cùng độ hiếm để reroll.")
        return

    # Trừ Gem + trừ card cũ
    player["gems"] -= cost
    inv[card_id] -= 1
    if inv[card_id] <= 0:
        del inv[card_id]

    # Nhận card mới cùng rarity
    new_card = random.choice(same_rarity_cards)
    add_card_to_inventory(player, new_card["id"], 1)

    await ctx.send(
        f"🎲 {ctx.author.mention} đã reroll **{old_card['name']}** (`{old_card['id']}`) "
        f"thành **{new_card['name']}** (`{new_card['id']}`) – độ hiếm **{rarity}**.\n"
        f"💰 Gem còn lại: **{player['gems']}**"
    )


@bot.command()
async def cardinfo(ctx, card_id: str):
    """
    Xem thông tin 1 card.
    Ví dụ: !cardinfo RX78
    """
    card_id = card_id.upper()
    card = next((c for c in CARD_POOL if c["id"] == card_id), None)

    if not card:
        await ctx.send(f"❌ Không tìm thấy card với ID `{card_id}`.")
        return

    rarity = card["rarity"]
    embed = discord.Embed(
        title=f"📇 Thông tin card: {card['name']}",
        color=discord.Color.from_str("#FFD700") if rarity == "UR" else (
            discord.Color.from_str("#00FFFF") if rarity == "SR" else (
                discord.Color.from_str("#00FF7F") if rarity == "R" else discord.Color.light_grey()
            )
        )
    )
    embed.add_field(name="ID", value=card["id"], inline=True)
    embed.add_field(name="Độ hiếm", value=f"{RARITY_EMOJI[rarity]} `{rarity}`", inline=True)
    await ctx.send(embed=embed)


@bot.command()
async def globalstats(ctx):
    """
    Thống kê chung toàn server: tổng lượt quay, tổng UR/SR/R/C.
    """
    if GLOBAL_STATS["rolls"] == 0:
        await ctx.send("⚠️ Chưa có ai quay gacha cả.")
        return

    embed = discord.Embed(
        title="🌐 Thống kê toàn server – Gundam Gacha",
        color=discord.Color.teal()
    )
    embed.add_field(name="Tổng lượt quay", value=str(GLOBAL_STATS["rolls"]), inline=False)
    embed.add_field(
        name="Rarity tổng",
        value=(
            f"🌈 UR: **{GLOBAL_STATS['UR']}**\n"
            f"💎 SR: **{GLOBAL_STATS['SR']}**\n"
            f"✨ R: **{GLOBAL_STATS['R']}**\n"
            f"⭐ C: **{GLOBAL_STATS['C']}**"
        ),
        inline=False
    )
    await ctx.send(embed=embed)

# =================== ĐÁNH NHAU – DUEL ===================

@bot.command()
async def duel(ctx, opponent: discord.Member, bet: int = 0):
    """
    Thách đấu 1vs1 dùng card trong bộ sưu tập.
    Ví dụ:
      !duel @TênBạn         -> không cược
      !duel @TênBạn 50      -> mỗi người đặt 50 Gem, thắng ăn hết
    """
    if opponent.id == ctx.author.id:
        await ctx.send("❌ Bạn không thể tự đấu với chính mình.")
        return

    if bet < 0:
        await ctx.send("❌ Tiền cược không thể âm.")
        return

    p1 = get_player(ctx.author)
    p2 = get_player(opponent)

    # Check có card để đánh không
    if not p1["inventory"]:
        await ctx.send(f"❌ {ctx.author.mention} chưa có card nào để đấu, hãy `!gacha` trước.")
        return

    if not p2["inventory"]:
        await ctx.send(f"❌ {opponent.mention} chưa có card nào để đấu, họ cần `!gacha` trước.")
        return

    # Check Gem đủ cược nếu có bet
    if bet > 0:
        if p1["gems"] < bet:
            await ctx.send(
                f"❌ {ctx.author.mention} không đủ Gem để cược (**{bet} Gem**).\n"
                f"Gem của bạn: **{p1['gems']}**"
            )
            return
        if p2["gems"] < bet:
            await ctx.send(
                f"❌ {opponent.mention} không đủ Gem để cược (**{bet} Gem**).\n"
                f"Gem của họ: **{p2['gems']}**"
            )
            return

        # Trừ cược tạm thời
        p1["gems"] -= bet
        p2["gems"] -= bet

    # Chọn card random cho mỗi người
    c1 = get_random_card_from_inventory(p1)
    c2 = get_random_card_from_inventory(p2)

    if c1 is None or c2 is None:
        await ctx.send("⚠️ Lỗi chọn card, thử lại sau.")
        # Hoàn lại cược nếu có
        if bet > 0:
            p1["gems"] += bet
            p2["gems"] += bet
        return

    # Tính sức mạnh: base theo rarity + random thêm
    base1 = RARITY_POWER.get(c1["rarity"], 1)
    base2 = RARITY_POWER.get(c2["rarity"], 1)
    roll1 = random.randint(0, 3)
    roll2 = random.randint(0, 3)
    power1 = base1 + roll1
    power2 = base2 + roll2

    # Xử lý kết quả
    result_text = ""
    if power1 > power2:
        # ctx.author thắng
        if bet > 0:
            reward = bet * 2
            p1["gems"] += reward
            result_text = (
                f"🏆 {ctx.author.mention} **CHIẾN THẮNG** và nhận **{reward} Gem** "
                f"từ tiền cược!"
            )
        else:
            result_text = f"🏆 {ctx.author.mention} **CHIẾN THẮNG**!"
    elif power2 > power1:
        # opponent thắng
        if bet > 0:
            reward = bet * 2
            p2["gems"] += reward
            result_text = (
                f"🏆 {opponent.mention} **CHIẾN THẮNG** và nhận **{reward} Gem** "
                f"từ tiền cược!"
            )
        else:
            result_text = f"🏆 {opponent.mention} **CHIẾN THẮNG**!"
    else:
        # Hòa -> hoàn cược
        if bet > 0:
            p1["gems"] += bet
            p2["gems"] += bet
        result_text = "⚔️ Trận đấu **HÒA**! Cả hai đều chiến quá ác."

    embed = discord.Embed(
        title="🤺 Gundam Gacha – Trận đấu 1vs1",
        color=discord.Color.red()
    )
    embed.add_field(
        name=f"{ctx.author.display_name}",
        value=(
            f"Card: {format_card(c1)}\n"
            f"Sức mạnh: **{power1}** "
            f"(base {base1} + roll {roll1})"
        ),
        inline=False
    )
    embed.add_field(
        name=f"{opponent.display_name}",
        value=(
            f"Card: {format_card(c2)}\n"
            f"Sức mạnh: **{power2}** "
            f"(base {base2} + roll {roll2})"
        ),
        inline=False
    )

    if bet > 0:
        embed.add_field(
            name="💰 Tiền cược",
            value=f"Mỗi người: **{bet} Gem**",
            inline=False
        )

    embed.add_field(name="Kết quả", value=result_text, inline=False)

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
            "`!profile` – xem hồ sơ gacha của bạn\n"
            "`!quests` – xem nhiệm vụ ngày\n"
            "`!questclaim` – nhận thưởng nhiệm vụ ngày"
        ),
        inline=False
    )

    embed.add_field(
        name="🎰 Gacha & Bộ sưu tập",
        value=(
            "`!gacha` hoặc `!gacha 10` – quay 1 / 10 lần\n"
            "`!collection` – xem bộ sưu tập card\n"
            "`!cards` – xem tất cả card có thể quay\n"
            "`!cardinfo <CARD_ID>` – xem thông tin 1 card"
        ),
        inline=False
    )

    embed.add_field(
        name="💸 Giao dịch, Đấu & Xếp hạng",
        value=(
            "`!sell <CARD_ID> <SỐ_LƯỢNG>` – bán card lấy Gem\n"
            "`!gift @user <SỐ_GEM>` – chuyển Gem cho người khác\n"
            "`!reroll <CARD_ID>` – đổi 1 card sang card khác cùng độ hiếm (tốn Gem)\n"
            "`!duel @user [CƯỢC]` – đấu 1vs1, dùng card random, có thể cược Gem\n"
            "`!top` – bảng xếp hạng người chơi\n"
            "`!globalstats` – thống kê toàn server"
        ),
        inline=False
    )

    embed.set_footer(text="Gõ tên lệnh như trên, không cần <>.")

    await ctx.send(embed=embed)

# =================== CHẠY BOT ===================

bot.run(TOKEN)
