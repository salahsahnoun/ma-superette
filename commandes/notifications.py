import threading
import urllib.request
import urllib.parse
from django.conf import settings
from django.utils import timezone


def _get_config():
    from .models import ConfigNotification
    return ConfigNotification.get()


def _send(phone, apikey, texte):
    url = (
        "https://api.callmebot.com/whatsapp.php?"
        + urllib.parse.urlencode({'phone': phone, 'text': texte, 'apikey': apikey})
    )
    try:
        urllib.request.urlopen(url, timeout=8)
        return True
    except Exception:
        return False


def _envoyer_whatsapp(commande):
    cfg = _get_config()
    if not cfg.actif or not cfg.whatsapp_phone or not cfg.whatsapp_apikey:
        return

    currency = getattr(settings, 'CURRENCY_SYMBOL', 'DA')
    heure = timezone.localtime(commande.created).strftime('%Hh%M')
    date  = timezone.localtime(commande.created).strftime('%d/%m/%Y')

    lignes_txt = '\n'.join(
        f"  ▫️ {l.quantite}× {l.nom_produit}  —  {l.total_ligne():.2f} {currency}"
        for l in commande.lignes.all()
    )

    if commande.mode_livraison == 'livraison':
        mode_ligne = f"🚚 *Livraison à domicile*\n📍 {commande.adresse or 'adresse non précisée'}"
    else:
        hr = commande.heure_retrait.strftime('%Hh%M') if commande.heure_retrait else '?'
        mode_ligne = f"🏪 *Retrait en magasin* à {hr}"

    financier = f"💰 Sous-total : {commande.sous_total:.2f} {currency}"
    if commande.frais_livraison:
        financier += f"\n🚛 Livraison : +{commande.frais_livraison:.2f} {currency}"

    texte = (
        f"🛒 *Nouvelle commande #{commande.pk}*\n"
        f"🕐 {heure}  —  {date}\n"
        f"\n"
        f"👤 *{commande.nom}*\n"
        f"📞 {commande.telephone}\n"
        f"\n"
        f"{mode_ligne}\n"
        f"\n"
        f"🛍️ *Articles :*\n"
        f"{lignes_txt}\n"
        f"\n"
        f"{financier}\n"
        f"━━━━━━━━━━━━━\n"
        f"💳 *TOTAL : {commande.total:.2f} {currency}*"
    )
    if commande.note:
        texte += f"\n\n💬 _{commande.note}_"

    _send(cfg.whatsapp_phone, cfg.whatsapp_apikey, texte)


def _envoyer_whatsapp_test(cfg):
    texte = (
        "🧪 *Test de notification — Ma Superette*\n\n"
        "✅ La configuration WhatsApp fonctionne correctement.\n"
        "Vous recevrez les nouvelles commandes sur ce numéro."
    )
    return _send(cfg.whatsapp_phone, cfg.whatsapp_apikey, texte)


def notifier_nouvelle_commande(commande):
    threading.Thread(target=_envoyer_whatsapp, args=(commande,), daemon=True).start()
