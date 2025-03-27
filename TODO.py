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
# TODO: Phone mező formátum ellenőrző! - REGEX: Regural Expression --> formátum szabályok kifejezése, sablon megfelelés (pl.: hosszúság, megengedett karatkerek, stb.) 
# https://trestleiq.com/phone-validation-regex-the-what-how-and-pros-and-cons/

# +TODO: Valahol értesíteni a felhasználót, hogy minimum 16-os Odoo verzió szükséges a modulokhoz!
# TODO: vizsgálat: életkor és következő szülinap számítás, adatmanipuláció csak azon a napon történjen, 
# amikor ténylegesen változás történik (egész szám az életkorban, új dátum a következő születésnapnál), hogy ne legyen tele a log felesleges adatokkal!

# TODO: Unit Tesztek lefuttatása! Family Connections Unit Teszt írása! (Nem megy bash-en commandokkal, a web-es interface-n belül meg nem találtam a saját Unit Test-jeimet)
# https://www.odoo.com/documentation/18.0/developer/reference/backend/testing.html
# TODO: Yetiforce adatmigrálás next! Kérdések: 
# 1# Csak gyerek:szülő kapcsolatok a YetiForce-ban?
# 2# Birthday field az miért nincsen a vtiger excel-ben?
# 3# A CSV az pontosan mire kell? (Ezt csak azért kérdezem, mert úgy tűnik, hogy a vtiger excel-ben benne van minden, ami kell az adatmigráláshoz) válasz: CSV majd az éles adatmigráláshoz kell, most csak a vtiger excel-t demo-hoz! 
# Komment: Legyen hiba üzenet, ha nem sikerül párt találni egy contact-hoz, és legyen loggolva (egy fájlban) minden kapcsolat felvitele. A script kimenet legyen olyan formátum, mint a script kimenet!