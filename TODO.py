# +TODO - születésnap, stakeholder, entry, exit (csak, ha entry megvan)
# , nickname, membership level, 
# Egy új tabot hozz létre a többinek: SSN, TAX, Bool értékek stb... 
# logikus csoportosítás!

# +TODO - Változó nevek legyenek intuitívek!

# +TODO - Családi kapcsolatok: Odoo részek újrafelhasználásával: 
# LIST VIEW (- Meglévő táblázat vezérlőt próbáld újrahasználni - list_view): 
# 3 oszlop: név, legördülő menü: kapcsolódás fajtái vannak vagy egyéb, harmadik pedig egy link a rokon profiljára, 
# törlés, KÖLCSÖNÖS MEGJELENÍTÉS 
# A harmadik link-es oszlop az szükséges? 
# A Many2One mezőnek egy beépített funkciója az internal link.

# +TODO: contact extension blank space minimalizálás, 
# optimális elhelyezés, csoportosítás az rendben!
# +TODO - todo note: EntryDate-nél, hogy mikor lépett be a mozgalomba!
# +TODO - todo note: ExitReason-nél tűnjön el a field, ha nincs ExitDate
# +TODO - todo note: Backend-en vagy Frontend-en számloja? 
    # A válasz: A Backend-en számolódik, 
    # a kódon belül mindig újraszámolódik az @api.depends-nek köszönhetően 
    # és a Frontend-en csak szimplán megjelenik a böngészőn

# +TODO: időnként bug új felvitelnél a family relations-ben, 
# +TODO: JSON fájl-ba helyezni a kapcsolati típusokat és a reciprocal_map-et
# +TODO: Megmarad:- gyermek- szülő- testvér- grandparent- unokatestvér- unoka- other (MIND ANGOLUL)
# +TODO: Stakeholder: Multiselect Dropdown field!
# +TODO: BirthDate mező címkéje Date of Birth!
# +TODO: Alsó fülek: Sales and Purchases tűnjön el!
# +TODO: Family Relations-re átnevezni, nem Family Connections!
# +TODO: 3. oszlop a list view-ban: kommentelésre (ugyanúgy kölcsönös legyen, mint a másik 2 oszlop)
# +TODO: Hosszabb input mezők, ahol szükséges!
# +TODO: IsActive Boolean mező!
# +TODO: Phone mező formátum ellenőrző!
# +TODO: Valahol értesíteni a felhasználót, hogy minimum 16-os Odoo verzió szükséges a modulokhoz!
# TODO: Unit Tesztek lefuttatása! Family Connections Unit Teszt írása!
# TODO: Yetiforce adatmigrálás next! Kérdés: A Yetiforce-ban már megvan
#  adva, hogy kinek milyen családi kapcsolatai vannak, 
# ez már benne van a Yetiforce-ban és csak ezt kell beimportálni 
# az Odoo-ba a Family Relations modul segítségével?