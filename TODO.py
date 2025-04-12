#+TODO - születésnap, stakeholder, entry, exit (csak, ha entry megvan)
# , nickname, membership level, 
# Egy új tabot hozz létre a többinek: SSN, TAX, Bool értékek stb... 
# logikus csoportosítás!

#+TODO - Változó nevek legyenek intuitívek!

#+TODO - Családi kapcsolatok: Odoo részek újrafelhasználásával: 
# LIST VIEW (- Meglévő táblázat vezérlőt próbáld újrahasználni - list_view): 
# 3 oszlop: név, legördülő menü: kapcsolódás fajtái vannak vagy egyéb, harmadik pedig egy link a rokon profiljára, 
# törlés, KÖLCSÖNÖS MEGJELENÍTÉS 
# A harmadik link-es oszlop az szükséges? 
# A Many2One mezőnek egy beépített funkciója az internal link.

#+TODO: contact extension blank space minimalizálás, 
# optimális elhelyezés, csoportosítás az rendben!
#+TODO - todo note: EntryDate-nél, hogy mikor lépett be a mozgalomba!
#+TODO - todo note: ExitReason-nél tűnjön el a field, ha nincs ExitDate
#+TODO - todo note: Backend-en vagy Frontend-en számloja? 
    # A válasz: A Backend-en számolódik, 
    # a kódon belül mindig újraszámolódik az @api.depends-nek köszönhetően 
    # és a Frontend-en csak szimplán megjelenik a böngészőn

#+TODO: időnként bug új felvitelnél a family relations-ben, 
#+TODO: JSON fájl-ba helyezni a kapcsolati típusokat és a reciprocal_map-et

#+TODO: Megmarad:- gyermek- szülő- testvér- grandparent- unokatestvér- unoka- other (MIND ANGOLUL)
#+TODO: Stakeholder: Multiselect Dropdown field!
#+TODO: BirthDate mező címkéje Date of Birth!
#+TODO: Alsó fülek: Sales and Purchases tűnjön el!
#+TODO: Family Relations-re átnevezni, nem Family Connections!
#+TODO: 3. oszlop a list view-ban: kommentelésre (ugyanúgy kölcsönös legyen, mint a másik 2 oszlop)
#+TODO: Hosszabb input mezők, ahol szükséges!
#+TODO: IsActive Boolean mező!
#+TODO: Phone mező formátum ellenőrző! - REGEX: Regural Expression --> 
# formátum szabályok kifejezése, sablon megfelelés (pl.: hosszúság, megengedett karatkerek, stb.) 
# https://trestleiq.com/phone-validation-regex-the-what-how-and-pros-and-cons/

#+TODO: Valahol értesíteni a felhasználót, hogy minimum 16-os Odoo verzió szükséges a modulokhoz!
#+TODO: vizsgálat: életkor és következő szülinap számítás, adatmanipuláció csak azon a napon történjen, 
# amikor ténylegesen változás történik (egész szám az életkorban, új dátum a következő születésnapnál), 
# hogy ne legyen tele a log felesleges adatokkal!

#TODO: Unit Tesztek lefuttatása! Family Connections Unit Teszt írása! (Nem megy bash-en commandokkal, 
# a web-es interface-n belül meg nem találtam a saját Unit Test-jeimet)
# https://www.odoo.com/documentation/18.0/developer/reference/backend/testing.html

# Yetiforce adatmigrálás next! Kérdések: 
# 1# Csak gyerek:szülő kapcsolatok a YetiForce-ban? válasz: igen
# 2# Birthday field az miért nincsen a vtiger excel-ben? válasz: van, csak nem abban az excel-ben, 
# amit eredetileg kaptam
# 3# A CSV az pontosan mire kell? (Ezt csak azért kérdezem, mert úgy tűnik, hogy a vtiger excel-ben benne van minden, 
# ami kell az adatmigráláshoz) válasz: CSV majd az éles adatmigráláshoz kell, most csak a vtiger excel demo-hoz!

#+TODO Komment: Legyen hiba üzenet, ha nem sikerül párt találni 
# egy contact-hoz, és legyen loggolva minden kapcsolat felvitele.
# A script kimenet legyen olyan formátum, mint a script bemenet!
#+TODO Ha nincs nickname, akkor legyen a firstname a nickname!
#+TODO Szkript: különálló, futtatandó kód, az Odoo API-n
# (JSON formátumú adat megy bele) keresztül hajtsa végre a szkript-et 
# (nem gomb, vagy akármilyen felületen megjelenő dolog). - 
# kell majd a jövőbeli feladatokhoz is, és biztonságosabb, 
# gyorsabb kezelni az error-okat vele
#+TODO: Family Relations része a szkript-nek
#+TODO: Hiba üzenet kiíása a family relations error-okhoz is
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# A segítség az API-hoz: https://www.odoo.com/documentation/18.0/developer/reference/external_api.html
#+TODO: A u_yf_contacts_contacts-nál minden sorban az első 
# vagy a második szám azonosítja a szülőket? 
# Azért fontos, mert a family relations úgy működik, hogy vagy 
# csak a parent vagy csak a child címkét kell átadni a kódnak, 
# a másik oldal elkészül automatikusan a kölcsönösségnek köszönhetően.

# A stakeholder címkék alapján van ahol az első szám a parent 
# (pl. 918 (ez a parent),"896" (és ez a gyermek)), mert ahhoz 
# a rekordhoz van megadva a szülő címke a stakeholdereknél, 
# de vannak olyan sorok is, ahol a második szám ismétlődik 
# (pl. a 2731) 4 soron keresztül és ahhoz kötődik 4 különböző első szám,
#  amelyek a gyerekek.
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#+TODO: DB-s modul az adatbázis visszaállításához, hogy ne keljen törölni manuálisan tesztek után! 
# Majd Marci-val együtt használjuk!!

#+TODO: név és e-mail együttes alapján legyen az existing partner!
#TODO: Stakeholder alapján dől el, hogy ki a szülő!
#TODO: A try and except legyen külön tömben a sikeres és sikertelen alapján (2 külön tömb), majd a végén ezek legyenek benne egy log fileban --> https://docs.python.org/3/howto/logging.html#logging-to-a-file
#TODO: kapcsoló --> script preflight (Olyan funkció, hogy végigmegy, de nincs adatmódosítás. Lépéseket lehet elvégezni, de nem történik adatbázisba rögzítés. Kapcsolatok létrehozásánál lesz jó. Nem kell módosítani az adatbázist, látni lehet előre a problémákat.)
#TODO: Belépési pont megjelölése --> rollback, visszagörgetés egy checkpoint-hoz --> két utasítás közötti történéseket vissza lehet csinálni. Benne van az Odoo-ban? - utánanézni (segítség: database transaction rollback commit)