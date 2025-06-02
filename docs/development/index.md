# 📁 NetBox Firmware Plugin – Documentatie

Deze folder bevat alle uitleg over de werking van de plugin [`netbox_firmware`](https://github.com/discedric/netbox_firmware). Dit document is bedoeld voor iedereen die de plugin wil gebruiken, begrijpen, onderhouden of uitbreiden. We leggen stap voor stap uit wat de plugin doet, hoe hij technisch in elkaar zit, en hoe je zelf aanpassingen kan doen.

---

## 📌 Inhoud

* [1. Wat doet deze plugin?](#1-wat-doet-deze-plugin)
* [2. Architectuur en modellen](models.md)
* [3. API-functionaliteit](api.md)
* [4. Gebruik in de UI](ui.md)
* [5. Filters](filters.md)
* [6. Forms](forms.md)
* [7. urls](urls.md)
* [8. Pluginstructuur en onderhoud](structure.md)
* [9. Veelvoorkomende fouten en debugging](debugging.md)
* [10. Nuttige links en bronnen](resources.md)

---

## 1. Wat doet deze plugin?

Deze plugin breidt NetBox uit met de mogelijkheid om **firmwareversies** te beheren en toe te wijzen aan **devices** of **modules**.

Je kan:

* Firmwareversies registreren (naam, beschrijving, fabrikant, bestand, status)
* Toewijzingen maken van firmware naar toestellen/modules
* Zien wanneer een firmware werd toegepast en bij welk ticketnummer

Doel: overzicht en historiek bewaren van firmware-updates in een infrastructuur.

Meer details vind je in [models.md](models.md).

---

Lees verder in de volgende documenten:

* [models.md](models.md) – uitleg over de datamodellen en validatie
* [api.md](api.md) – beschikbare API endpoints
* [ui.md](ui.md) – hoe de plugin eruitziet en werkt in de NetBox-interface
* [installation.md](installation.md) – hoe je de plugin installeert
* [structure.md](structure.md) – mappen en bestanden in de plugin
* [debugging.md](debugging.md) – tips bij fouten
* [resources.md](resources.md) – externe links en officiële bronnen
