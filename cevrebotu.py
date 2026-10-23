import discord
import random
import os
import requests
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event  # bot belirli bir olay gerçekleştiğinde tetiklensin.
async def on_ready():  # bot başarılı bir şekilde Discord'a bağlandığında tetiklenir
    print(f'{bot.user} olarak giriş yaptık')


@bot.command()
async def geri_donusum(ctx):
    await ctx.send("Geri dönüştürülebilir malzemeler: Cam, kağıt, plastik ve metal. Unutmayın, geri dönüşüm önemlidir!" )
@bot.command()
async def plastik(ctx):
    await ctx.send("Bir plastik doğada 400 ila 450 yıl içinde yok olur")
@bot.command()
async def pil(ctx):
    await ctx.send("Bir pil doğada 300 yılda yok olur")
@bot.command()
async def cam(ctx):
    await ctx.send("Hammaddesi toprak olduğu için bir cam şişenin doğada yok olma süresi en az 4000 yıldır.")
@bot.command()
async def kimyasal(ctx):
    await ctx.send("Kimyasal atıklar (şampuan,sabun,duş jeli, temizlik malzemeleri):  100 - 400 yıl")
# Geri dönüşüm rehberi veritabanı
GERI_DONUSUM_REHBERI = {
    "plastik": "♻️ Plastik şişe ve kapları yıkayıp kurutarak sarı geri dönüşüm kutularına atabilirsiniz. Kapakları ayırmayı unutmayın!",
    "kağıt": "📦 Gazete, karton ve dergileri ıslatmadan mavi geri dönüşüm kutularına atın. Yağlı kağıtlar geri dönüştürülemez.",
    "cam": "🍾 Cam şişe ve kavanozları yıkayarak yeşil/beyaz cam kumbara kutularına atın. Ayna ve ampulleri buraya atmayın!",
    "pil": "🔋 Atık piller çevreye büyük zarar verir! Pilleri evsel çöpe değil, marketlerde veya okullarda bulunan Kırmızı Atık Pil Kutularına atın.",
    "elektronik": "💻 Eski telefon, kablo ve bilgisayar parçalarını belediyelerin atık getirme merkezlerine teslim edin.",
    "yağ": "🛢️ Kullanılmış kızartmalık yağları lavaboya dökmeyin! Bir biriktirme kabında toplayıp atık yağ toplama noktalarına verin. 1 litre atık yağ 1 milyon litre temiz suyu kirletir!"
}

# Çevre hakkında bilgiler
CEVRE_BILGILERI = [
    "🌍 Bir plastik şişenin doğada tamamen yok olması yaklaşık 450 yıl sürer.",
    "🌳 Bir yetişkin ağaç, yılda yaklaşık 22 kilogram karbondioksit emer.",
    "💧 Sifonu her çektiğimizde yaklaşık 6 ila 12 litre temiz su harcanır.",
    "🐝 Arılar olmasaydı, küresel gıda üretiminin %30'u ve çiçekli bitkilerin %90'ı tehlikeye girerdi.",
    "🌊 Denizlerdeki plastik atıkların %80'i karadaki karasal faaliyetlerden kaynaklanmaktadır."
]

# Günlük yeşil ipuçları
IPUCLARI = [
    "💡 Odadan çıkarken ışıkları kapatmayı ve kullanmadığın elektronik cihazların fişini çekmeyi alışkanlık edin.",
    "🛍️ Alışverişe giderken yanında bez çanta taşı, plastik poşet kullanımını azalt.",
    "🪥 Dişlerini fırçalarken musluğu kapatmak yılda binlerce litre su tasarrufu sağlar.",
    "🚲 Kısa mesafelerde yürümeyi veya bisiklete binmeyi tercih et."
]

@bot.event
async def on_ready():
    print(f'✅ {bot.user.name} olarak giriş yapıldı!')
    await bot.change_presence(activity=discord.Game(name="!yardim_cevre | Doğanızı Koruyun 🌿"))

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("🏓 Pong! Çevre Botu aktif ve çalışıyor.")

@bot.command(name="geridonusum")
async def geridonusum(ctx, *, madde: str = None):
    """Maddelerin nasıl geri dönüştürüleceğini söyler."""
    if not madde:
        await ctx.send("❓ Lütfen bir madde adı belirtin. Örnek: `!geridonusum plastik` (Kategoriler: plastik, kağıt, cam, pil, elektronik, yağ)")
        return
    
    madde_alt = madde.lower().strip()
    if madde_alt in GERI_DONUSUM_REHBERI:
        await ctx.send(GERI_DONUSUM_REHBERI[madde_alt])
    else:
        await ctx.send(f"⚠️ `{madde}` için bilgi bulunamadı. Lütfen şunlardan birini deneyin: plastik, kağıt, cam, pil, elektronik, yağ.")

@bot.command(name="bilgi")
async def bilgi(ctx):
    """Çevre hakkında rastgele bir bilgi verir."""
    secilen_bilgi = random.choice(CEVRE_BILGILERI)
    await ctx.send(f"ℹ️ **Biliyor muydunuz?**\n{secilen_bilgi}")

@bot.command(name="ipucu")
async def ipucu(ctx):
    """Günlük doğa dostu ipucu verir."""
    secilen_ipucu = random.choice(IPUCLARI)
    await ctx.send(f"🌱 **Günün Doğa Dostu İpucu:**\n{secilen_ipucu}")

@bot.command(name="karbon_hesapla")
async def karbon_hesapla(ctx, aylik_km: float = None, aylik_elektrik: float = None):
    """Aylık araç ve elektrik tüketimine göre detaylı karbon ayak izini hesaplar."""
    if aylik_km is None or aylik_elektrik is None:
        embed = discord.Embed(
            title="🌿 Karbon Ayak İzi Hesaplama Rehberi",
            description="Aylık tahmini karbon ayak izinizi hesaplamak için şu formatı kullanın:\n\n`!karbon_hesapla <aylık_araç_km> <aylık_elektrik_kwh>`",
            color=discord.Color.green()
        )
        embed.add_field(name="Örnek Kullanım", value="`$karbon_hesapla 500 200`\n*(Ayda ortalama 500 km araç kullanan ve 200 kWh elektrik harcayan biri için)*", inline=False)
        await ctx.send(embed=embed)
        return

    # Yaklaşık Karbon Salınım Katsayıları:
    # 1 km benzinli araç kullanımı ortalama ~0.12 kg CO2 salınımına yol açar.
    # 1 kWh elektrik tüketimi ortalama ~0.45 kg CO2 salınımına yol açar.
    arac_co2 = aylik_km * 0.12
    elektrik_co2 = aylik_elektrik * 0.45
    toplam_co2 = arac_co2 + elektrik_co2
    yillik_ton = (toplam_co2 * 12) / 1000

    # Sonuca göre değerlendirme mesajı
    if yillik_ton < 2.5:
        yorum = "Tebrikler! Karbon ayak izin küresel ortalamanın oldukça altında, harika bir doğa dostusun! 🌟"
    elif yillik_ton < 6.0:
        yorum = "Karbon ayak izin ortalama seviyelerde. Enerji tasarrufu ve toplu taşıma ile bunu daha da düşürebilirsin. 🌱"
    else:
        yorum = "Karbon ayak izin biraz yüksek görünüyor. Daha yeşil alternatifler denemek dünyamız için harika olur! ⚠️"

    embed = discord.Embed(
        title="📊 Karbon Ayak İzi Hesaplama Sonucun",
        color=discord.Color.blue()
    )
    embed.add_field(name="🚗 Araç Kaynaklı Emisyon", value=f"{arac_co2:.2f} kg CO₂ / ay", inline=False)
    embed.add_field(name="⚡ Elektrik Kaynaklı Emisyon", value=f"{elektrik_co2:.2f} kg CO₂ / ay", inline=False)
    embed.add_field(name="🌍 Toplam Aylık Salınım", value=f"**{toplam_co2:.2f} kg CO₂**", inline=False)
    embed.add_field(name="📈 Tahmini Yıllık Toplam", value=f"**{yillik_ton:.2f} ton CO₂ / yıl**", inline=False)
    embed.add_field(name="💡 Değerlendirme", value=yorum, inline=False)
    embed.set_footer(text="Geleceğimiz için doğayı koruyalım! ✨")

    await ctx.send(embed=embed)

@bot.command(name="yardim_cevre")
async def yardim_cevre(ctx):
    """Kullanılabilecek çevre komutlarını listeler."""
    embed = discord.Embed(
        title="🌿 Çevre Botu Komut Rehberi",
        description="Doğayı korumak ve bilinçlenmek için kullanabileceğiniz komutlar:",
        color=discord.Color.green()
    )
    embed.add_field(name="$geridonusum <madde>", value="Maddelerin nasıl geri dönüştürüleceğini gösterir. (plastik, pil, yağ vb.)", inline=False)
    embed.add_field(name="$bilgi", value="Çevre hakkında ilginç ve öğretici bilgiler verir.", inline=False)
    embed.add_field(name="$ipucu", value="Doğayı korumak için günlük pratik tavsiyeler sunar.", inline=False)
    embed.add_field(name="$karbon_hesapla <km> <elektrik>", value="Aylık araç ve elektrik tüketimine göre karbon ayak izinizi hesaplar.", inline=False)
    embed.add_field(name="$ping", value="Botun çalışıp çalışmadığını kontrol eder.", inline=False)
    
    embed.set_footer(text="Geleceğimiz için doğayı koruyalım! ✨")
    await ctx.send(embed=embed)
bot.run("")
# Bu özellik, botun kendisine gönderilen komutları tanıması için bir ön ek tanımlar.
# $ işareti komut ön eki olarak belirlenmiştir. Yani bot sadece $ ile başlayan komutları algılar.
