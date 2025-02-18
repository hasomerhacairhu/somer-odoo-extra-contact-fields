# Szoftverkövetelmény Specifikáció  
**Projekt neve:** Odoo Contact Enhancement Module

## 1. Bevezetés  
Ez a dokumentum az Odoo ERP rendszer beépített kontakt moduljának kibővítésére készülő modul részletes követelményeit foglalja össze. A modul célja, hogy az alap kontakt funkciókat az alábbi bővítésekkel lássa el:
- Új adatmezők hozzáadása (beleértve a tagok részletes adatrögzítését)
- Dinamikus mezőmegjelenítés (pl. „ExitReason” csak akkor látható, ha „ExitDate” kitöltésre került)
- Automatikus kalkulációk a születési dátum változására (kor és következő születésnap)
- Családi kapcsolatok kezelése (kölcsönös megjelenítés és többszörös hozzárendelés)
- Dropdown mezők konfigurálhatósága JSON állományból
- A fejlesztést Git verziókövető rendszerrel végezzük, a kész kódot pedig Github nyilvános repozitóriumba töltjük fel  
A modul telepítése a „git clone” parancs segítségével történik.

## 2. Célkitűzés  
- **Bővítés:** A meglévő kontakt modul kibővítése új mezők és funkciók bevezetésével, melyek részletesebb adatrögzítést és -kezelést tesznek lehetővé.  
- **Dinamikus viselkedés:** Biztosítani kell, hogy a „Kilépés oka” (ExitReason) mező dinamikusan, újratöltés nélkül jelenjen meg kizárólag akkor, ha a „Kilépés dátuma” (ExitDate) kitöltésre került.  
- **Automatikus kalkulációk:** A születési dátum (BirthDate) mező módosításakor a rendszer automatikusan kalkulálja az aktuális kort (Age) és a következő születésnap dátumát (NextBirthday), majd frissíti az értékeket. A kalkulációs logika végrehajtható szerver oldalon az adatok beposztolásakor, ezzel biztosítva az adatkonzisztenciát.  
- **Családi kapcsolatok:** Minden kontakt esetében lehetőség legyen más kontaktok hozzárendelésére (családi kapcsolatok), melyek kölcsönösen megjelennek a kapcsolt profilokon.  
- **Dropdown konfiguráció:** Minden dropdown típusú mező (StakeholderGroup, MembershipLevel, TShirtSize) értékeit egy modul szintű JSON konfigurációs fájlból kell betölteni, így könnyen módosíthatóak a jövőben.  
- **Többszörös stakeholder kiválasztás:** A StakeholderGroup mező mostantól több érték egyidejű kiválasztását is támogassa, és a kategóriák angol nyelvű megfelelőjét jelenítse meg.

## 3. Funkcionális követelmények

### 3.1. Új adatmezők a kontakt modulban  
A modul az alábbi új mezőket adja hozzá, ahol a belső (angol) elnevezések kerülnek alkalmazásra:

- **EntryDate**: Belépés dátuma (date)  
- **MembershipLevel**: Tagsági szint besorolás (dropdown)  
  - **Lehetséges értékek:** "A", "B", "C" (értékek a konfigurálható JSON állományból)  
- **ExitDate**: Kilépés dátuma (date)  
- **ExitReason**: Kilépés oka (string)  
  - **Feltételes megjelenítés:** Ez a mező csak akkor jelenjen meg a felületen (dinamikus frissítéssel), ha az **ExitDate** mező tartalmaz értéket.
- **StakeholderGroup**: Stakeholder group (multiselect dropdown)  
  - **Lehetséges értékek:**  
    - "Alkalmi támogató"  
    - "Alumni"  
    - "Ellenző"  
    - "FIFE"  
    - "IFI"  
    - "Önkéntes"  
    - "Partner"  
    - "Rendszeres támogató"  
    - "Segítő"  
    - "Hivatalos"  
    - "Sajtó"  
    - "Szolgáltató"  
    - "Tanár"  
  - **Megjegyzés:** A dropdown értékeket a modulban tárolt JSON konfigurációs állományból kell betölteni.
- **Nickname**: Nickname (string)  
- **BirthDate**: Date of birth (date)  
- **Age**: Age (integer)  
  - **Kalkuláció:** Automatikusan számolja ki a születési dátum (BirthDate) alapján az aktuális életkort.  
- **IDNumber**: ID number (string)  
- **SSN**: Social security number (string)  
- **TShirtSize**: T-shirt size (dropdown)  
  - **Lehetséges értékek:** XS, S, M, L, XL, XXL, 3XL, 4XL, 5XL  
  - **Megjegyzés:** Az értékek a JSON állományból kerülnek betöltésre.
- **TaxID**: Tax identification number (string)  
- **PassportNumber**: Passport number (string)  
- **PassportExpirationDate**: Passport expiration date (date)  
- **BankAccountNumber**: Bank account number (string)  
- **PlaceOfBirth**: Place of birth (string)  
- **IsVaccinated**: Is vaccinated (boolean)  
- **MadrichTraining**: Madrich training (boolean)  
- **NextBirthday**: Next birthday (date)  
  - **Kalkuláció:** Automatikusan számolja ki a következő születésnap dátumát a BirthDate mező értéke alapján, figyelembe véve az aktuális dátumot.

### 3.2. Dinamikus mezőfrissítések és kalkulációk  
- **ExitReason megjelenítés:** A kliens oldali logika gondoskodik arról, hogy az **ExitReason** mező csak akkor látszódjon, ha az **ExitDate** mező értéke kitöltött.
- **Automatikus kalkulációk:**  
  - Amikor a **BirthDate** mező értéke megváltozik, a rendszer automatikusan újraszámolja az **Age** mezőben tárolt kort, valamint meghatározza és frissíti a **NextBirthday** mező értékét.  
  - A kalkulációs logika végrehajtható kliens oldalon (onchange esemény) és szerver oldalon is, különösen az adatok beposztolásakor, hogy az adatkonzisztencia mindig garantált legyen.

### 3.3. Családi kapcsolatok kezelése  
- **Kapcsolódási lehetőség:** Minden kontakt esetében lehetőség van más kontaktok hozzárendelésére, amelyek a családi kapcsolatokat jelzik.  
- **Kölcsönös megjelenítés:** A hozzárendelés mindkét érintett kontakt profilján látható legyen.  
- **Többszörös hozzárendelhetőség:** Egy kontakt több családtagot is tartalmazhat.

### 3.4. Dropdown értékek konfigurálása  
- **JSON alapú konfiguráció:** Minden dropdown típusú mező (StakeholderGroup, MembershipLevel, TShirtSize) értékeit egy konfigurációs JSON fájl végzi, mely a modul gyökerében található.  
- **Rugalmasság:** Ez lehetővé teszi, hogy a jövőben a dropdown értékek módosítása a kód átalakítása nélkül, csupán a konfiguráció frissítésével történjen.

## 4. Nem funkcionális követelmények

### 4.1. Verziókövetés és fejlesztési folyamat  
- **Verziókövetés:** A modul fejlesztését Git verziókövető rendszerrel kell végezni, a verziókat tagolással kell ellátni, és a kódot Github nyilvános repozitóriumba kell feltölteni.  
- **Fejlesztési ciklus:** Javasolt a rendszeres commitolás, branch-ek használata (pl. feature-ágak, bugfix ágak) és pull request alapú integrációs folyamat.

### 4.2. Telepítés  
- **Telepítési mód:** A modul telepítése a „git clone” parancs használatával történik, ezért a modulnak kompatibilisnek kell lennie az Odoo telepítési eljárásaival.

### 4.3. Kódolási és dokumentációs best practice-ek  
- **PEP8 szabvány:** A Python kódot a PEP8 stílusirányelvek betartásával kell megírni.  
- **Odoo irányelvek:**  
  - Követni kell az Odoo modul fejlesztési standardjait (pl. modellek, nézetek, biztonsági szabályok helyes definiálása).  
  - Használni kell az Odoo API-kat és dekorátorokat a megfelelő működés érdekében.  
- **Dokumentáció:**  
  - A kód minden funkcionális egységéhez részletes docstring-eket kell készíteni, melyek megkönnyítik a későbbi karbantartást.  
  - Automatizált tesztek (unit, integrációs, regressziós tesztek) készítése erősen ajánlott.  
- **Kód olvashatóság:** A modul felépítése legyen moduláris, a változók, függvények, osztályok nevei pedig angol nyelvű, beszédes elnevezéseket kapjanak (a projektben meghatározott camelCase vagy snake_case szabvány szerint).

### 4.4. Rendszer kompatibilitás  
- A kiegészítő modulnak zökkenőmentesen kell integrálódnia az Odoo ERP rendszer aktuális verziójába, és nem szabad sértenie a meglévő kontakt modul funkcionalitását.

## 5. Rendszerarchitektúra és integráció  
- **Adatmodell bővítés:** Az új mezők bevezetése az Odoo adatmodelljének kiterjesztését jelenti. Az adatintegritás, a validáció és az adatkonzisztencia biztosítása érdekében megfelelő ORM modelleket kell létrehozni.  
- **Eseményvezérelt frissítések és kalkuláció:**  
  - A BirthDate mező változását eseményfigyelő mechanizmus (onchange) révén kell kezelni, amely automatikusan frissíti az Age és NextBirthday mezőket.  
  - Emellett a kalkulációs logikát szerver oldalon is végre lehet hajtani az adatok beposztolásakor, így garantálva a konzisztens és megbízható adatfeldolgozást.  
  - Az ExitDate és ExitReason mezők esetében hasonló logikát kell alkalmazni a dinamikus mezőmegjelenítés érdekében.
- **JSON konfiguráció:** A dropdown értékek betöltését egy konfigurációs JSON fájl végzi, mely a modul gyökerében található. Ez megkönnyíti a konfigurációs változtatásokat és a rendszer testreszabását.

## 6. Tesztelési követelmények  
- **Funkcionális tesztek:**  
  - Ellenőrizni kell, hogy minden új mező helyesen jelenik meg és működik (különös figyelemmel a dinamikus és automatikus kalkulációkra).  
  - A családi kapcsolatok kezelése esetén a kölcsönös megjelenés és a többszörös hozzárendelhetőség validálása.
- **Automatizált tesztek:**  
  - Unit tesztek írása ajánlott a Python kód validálására.  
  - Integrációs és regressziós tesztek alkalmazása a rendszer stabilitásának biztosítására.

## 7. Dokumentáció és karbantartás  
- **Fejlesztői dokumentáció:**  
  - A kód mellett részletes fejlesztői dokumentáció készül, amely tartalmazza a specifikációban szereplő követelményeket, a kód struktúráját, a telepítési lépéseket, a JSON konfiguráció kezelését és a tesztelési módszereket.  
- **Verziókövetési napló:** A Github repozitóriumban legyen elérhető a fejlesztés minden fázisa, ideértve a verziótagolást, a commit üzeneteket és a kapcsolódó dokumentációt.

## 8. Kérdések és pontosítások  
- **PlaceOfBirth típus:** Megerősítve, ez egy string típusú mező.  
- **MembershipLevel értékek:** Az értékek jelenleg "A", "B", és "C".  
- **Dropdown konfiguráció:** Minden dropdown értéket a modulban tárolt JSON állományból tölt be, ezáltal a jövőbeni konfiguráció egyszerűsíthető.  
- **Kalkulációs logika:** A BirthDate mező módosításakor történő automatikus kalkulációkat (Age, NextBirthday) lehet kliens oldalon (onchange esemény) megvalósítani, illetve szerver oldalon az adatok beposztolásakor, hogy az adatkonzisztencia mindig garantált legyen.

---

Ez a módosított specifikáció tartalmazza azt az új követelményt is, miszerint a kalkulációs logika szerver oldalon történhet az adatok beposztolásakor. Ha további pontosításokra vagy kérdésekre van szükség, kérem, jelezze!
