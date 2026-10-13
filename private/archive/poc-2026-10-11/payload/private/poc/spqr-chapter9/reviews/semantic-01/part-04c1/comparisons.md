# M-POC5A.4c1 — rzeczywiste porównania22 lokatorów /44 wystąpień

Po podziale obejrzano dostarczone pełne strony31–33, wszystkie22 pasy krótkich cytatów z granicą oryginalnego bbox oraz dokładne nieposzerzone wycinkiE916/E914cont/E873. Obejrzano powiększenia granicznych znakówE911a/E914priority/E915/E92 oraz uciętych descenderówE914cont/E873. Porównano22 oryginalne cytaty ze źródłem i diagnozą geometrii. Cytat i image identyczne w obu odpowiedziach, ale każdy wynik ma osobne surowe bajty. Skrypty przeszukują tylko istniejące krótkie cytaty/glify i tworzą diagnostyczne obrazy, bez ekstrakcji nowych reguł lub naprawy odpowiedzi.

44 geometrie poprawne i cytaty znalezione w pełnym dostarczonym źródle. Ścisłe pełne obwiednie glifów:0 pass/44 fail. Raster:38 krótkich czytelnych cytatów bez zaobserwowanej utraty tuszu,4 z przyciętymi descenderami,2 z brakującą ostatnią linią. To różne miary, nie liczba poprawnych reguł.

first-001: `3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307`, 617941 bajtów.
context-01: `95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b`, 712014 bajtów.

eval-v1 `7debb9edffd9e0256a0065be335a743ce796660c67d5c6cdcfdddf433d3e8dce`; source `e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e`.

[Pełne ślady JSON](comparisons.json), [decyzje po ludzku](owner-focus.md). Wszystkie nowe propozycje waiting_review.

## E911a

Dokładny zakres: oryginalny krótki cytat i jego prostokąt.

> Pass-Thru may be used by two defending infantry units if both units meet the preceding conditions.

Niezależny dosłowny helper:

> Pass-Thru may be used by two defending infantry units if both
> units meet the preceding conditions.

Helper `/regions/2/text`, znaki [1173, 1271], SHA-256 `9c9929dcedb1e4387851dad39d506903b3636f5cea9eb5989b67e5b88124bac0`.

Strona31; bbox piksele [875, 1325, 1575, 2067], PDFpt [315.0, 477.0, 567.0, 744.12]; wymiary [1700, 2200].

Rzeczywisty krótki cytat PDFpt [315.00000000000006, 624.3803, 567.018, 646.3803]; całe obwiednie NIE mieszczą się. Raster: readable_no_observed_ink_loss.

Ręczne porównanie: Pełny krótki cytat o dwóch defending infantry jest widoczny. Prawa granica narusza obwiednię końcowego h w both o0.018pt; powiększenie nie pokazuje utraty ciemnych pikseli tego znaku. Nie ocenia całego Pass-Thru ani innych warunków.

[Dokładny nieposzerzony crop](../../../measurement/M-POC5A-semantic-04c1/visual-02/E911a-exact.png) · [Referencja do porównania granicy](../../../measurement/M-POC5A-semantic-04c1/visual-02/E911a-quote-reference.png). Referencja nie naprawia lokatora.

**first-001:** `/evidence/0`, bajty [12824,13874), SHA-256 `8de5a93e1b630fc74cdcc5136eb838796b097adcd99b84d11a8dd5cbf633ab7a`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/0/quote/value`; bajty [13155,13255), hash `305c1e950bc665b2c536453be75a1256dd277566cb10c77349db58a7e69d19dd`; wartość "Pass-Thru may be used by two defending infantry units if both units meet the preceding conditions.".

Pole `/evidence/0/image/bbox`; bajty [13574,13647), hash `99d492fc3c80c9d85712c5ac6e244f5243bd777547401d07e46dae07a3cbf9aa`; wartość [875, 1325, 1575, 2067].

Pole `/evidence/0/image/path`; bajty [13442,13470), hash `1909a421ea87dce812086a96fcaf7ec4f2e7380b02b0a77eefc6ba8f0b8cf997`; wartość "inputs/v1/pages/pdf-31.png".

Pole `/evidence/0/image/sha256`; bajty [13490,13556), hash `f80ec790ece408b391067b57927588a3c9963331e236524997b9d50e8f6e053e`; wartość "9edf269af78629a8bbfd809c75695e6353f7614d82d217d48ea2ecca0fd06712".

**context-01:** `/evidence/0`, bajty [48593,49672), SHA-256 `a1615915280193f36cbacb1320730ba0d2a7a89c98167b4d70534bc57873acfe`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/0/quote/value`; bajty [48934,49034), hash `305c1e950bc665b2c536453be75a1256dd277566cb10c77349db58a7e69d19dd`; wartość "Pass-Thru may be used by two defending infantry units if both units meet the preceding conditions.".

Pole `/evidence/0/image/bbox`; bajty [49361,49439), hash `f8948ea7ac669f06d0e7dea5a0601676f826a016b4996319449041e78e486e5b`; wartość [875, 1325, 1575, 2067].

Pole `/evidence/0/image/path`; bajty [49227,49255), hash `1909a421ea87dce812086a96fcaf7ec4f2e7380b02b0a77eefc6ba8f0b8cf997`; wartość "inputs/v1/pages/pdf-31.png".

Pole `/evidence/0/image/sha256`; bajty [49276,49342), hash `f80ec790ece408b391067b57927588a3c9963331e236524997b9d50e8f6e053e`; wartość "9edf269af78629a8bbfd809c75695e6353f7614d82d217d48ea2ecca0fd06712".

Każdy naruszony glif:

{"index": 50, "text": "h", "bbox_pdf_points": [562.018, 624.3803, 567.018, 634.3803], "bbox_pixels": [1561.1611111111113, 1734.3897222222224, 1575.0500000000002, 1762.1675000000002], "overflow_pdf_points": {"left": 0, "right": 0.018000000000029104, "top": 0, "bottom": 0}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E911a-boundary-0.png", "bytes": 1420, "sha256": "128e857b0cd3d26056db05c15c5e427fd8a0cb53f33be8532c5f5408de485cc7"}}

Wyłączenia: pełny rekord/klauzula/pozostały crop, artwork/ratingi, wcześniejsze pending, brakujące procedury, automatyczne semantyczneFP/FN/gold.

## E912

Dokładny zakres: oryginalny krótki cytat i jego prostokąt.

> Elephant Screens can Missile Fire with Reaction Fire (8.2) only, using the Elephant Screen row on the MRRC.

Niezależny dosłowny helper:

> Elephant Screens can Missile Fire with Reaction Fire (8.2) only,
> using the Elephant Screen row on the MRRC.

Helper `/regions/3/text`, znaki [1059, 1166], SHA-256 `4301a1b58b4671232505c46b6e0843a5b02675c9d2032b243c6e68d9b40b2f0f`.

Strona32; bbox piksele [125, 620, 825, 1010], PDFpt [45.0, 223.2, 297.0, 363.6]; wymiary [1700, 2200].

Rzeczywisty krótki cytat PDFpt [45.0, 303.12690000000003, 297.0169999999998, 325.12690000000003]; całe obwiednie NIE mieszczą się. Raster: readable_no_observed_ink_loss.

Ręczne porównanie: Cytat zawiera Reaction Fire8.2 only i Elephant Screen row MRRC; przecinek kończący pierwszą linię narusza obwiednię o0.017pt. Krótki raster czytelny, without observable ink loss; nie nadaje wartości MRRC lub oceny artwork/supply.

[Dokładny nieposzerzony crop](../../../measurement/M-POC5A-semantic-04c1/visual-02/E912-exact.png) · [Referencja do porównania granicy](../../../measurement/M-POC5A-semantic-04c1/visual-02/E912-quote-reference.png). Referencja nie naprawia lokatora.

**first-001:** `/evidence/2`, bajty [14948,16002), SHA-256 `d64ae6995d47f77145f71535932798754ae93b22bebaecf3f6b2ac519e2f0f90`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/2/quote/value`; bajty [15276,15385), hash `0afe994db51be9430763d2a40f07d13fec576d322ab8b0b08651e171aea0e4d9`; wartość "Elephant Screens can Missile Fire with Reaction Fire (8.2) only, using the Elephant Screen row on the MRRC.".

Pole `/evidence/2/image/bbox`; bajty [15704,15775), hash `4683c5796f038049e38834d6a00af1f0600a19ebd99caa0242b950246280323b`; wartość [125, 620, 825, 1010].

Pole `/evidence/2/image/path`; bajty [15572,15600), hash `371c47ac8788034de616a7b9891532ba48a58743af43d9f516d46116bd7c9aae`; wartość "inputs/v1/pages/pdf-32.png".

Pole `/evidence/2/image/sha256`; bajty [15620,15686), hash `cbffa2f09aa8fb632365e06adff8de9b990f6214efae8dbea3cb73275c8e533f`; wartość "e80ea90e4a3a441416fd4624be73b2f97ca7185e6bb552d89454b6121fca394a".

**context-01:** `/evidence/2`, bajty [50777,51860), SHA-256 `b30fb5fc9ce9798b829f524d80503714526c05ed5c3a69d6966d18966370b7a4`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/2/quote/value`; bajty [51115,51224), hash `0afe994db51be9430763d2a40f07d13fec576d322ab8b0b08651e171aea0e4d9`; wartość "Elephant Screens can Missile Fire with Reaction Fire (8.2) only, using the Elephant Screen row on the MRRC.".

Pole `/evidence/2/image/bbox`; bajty [51551,51627), hash `a977537a63406058838952bc7890f1ca54f16cf3c58799436262ac8e84734854`; wartość [125, 620, 825, 1010].

Pole `/evidence/2/image/path`; bajty [51417,51445), hash `371c47ac8788034de616a7b9891532ba48a58743af43d9f516d46116bd7c9aae`; wartość "inputs/v1/pages/pdf-32.png".

Pole `/evidence/2/image/sha256`; bajty [51466,51532), hash `cbffa2f09aa8fb632365e06adff8de9b990f6214efae8dbea3cb73275c8e533f`; wartość "e80ea90e4a3a441416fd4624be73b2f97ca7185e6bb552d89454b6121fca394a".

Każdy naruszony glif:

{"index": 54, "text": ",", "bbox_pdf_points": [294.5169999999998, 303.12690000000003, 297.0169999999998, 313.12690000000003], "bbox_pixels": [818.1027777777772, 842.0191666666667, 825.0472222222216, 869.7969444444445], "overflow_pdf_points": {"left": 0, "right": 0.016999999999825377, "top": 0, "bottom": 0}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E912-boundary-0.png", "bytes": 1347, "sha256": "0702be794b7aac79a9cc42db686adfbce27e6e648715a614ea34c596bd9fe4ed"}}

Wyłączenia: pełny rekord/klauzula/pozostały crop, artwork/ratingi, wcześniejsze pending, brakujące procedury, automatyczne semantyczneFP/FN/gold.

## E913

Dokładny zakres: oryginalny krótki cytat i jego prostokąt.

> The Elephant unit may use Reaction Fire with both its javelins and its screen, with the player rolling separately for each.

Niezależny dosłowny helper:

> The Elephant unit may use Reaction Fire with both its
> javelins and its screen, with the player rolling separately for each.

Helper `/regions/3/text`, znaki [1456, 1579], SHA-256 `37c838f1ff46d60f8e8814a6b9aeefef102b5260dca1afda2219af8bb02f6c28`.

Strona32; bbox piksele [125, 1020, 825, 1155], PDFpt [45.0, 367.2, 297.0, 415.8]; wymiary [1700, 2200].

Rzeczywisty krótki cytat PDFpt [45.0, 392.5269, 297.019, 414.5269]; całe obwiednie NIE mieszczą się. Raster: readable_no_observed_ink_loss.

Ręczne porównanie: W pasie widoczne both its javelins and its screen oraz separately for each. Dwie prawe obwiednie s/kropka naruszone o maks0.019pt, bez widocznego przycięcia tuszu. Normalizacja łączenia linii nie zmienia separately/both.

[Dokładny nieposzerzony crop](../../../measurement/M-POC5A-semantic-04c1/visual-02/E913-exact.png) · [Referencja do porównania granicy](../../../measurement/M-POC5A-semantic-04c1/visual-02/E913-quote-reference.png). Referencja nie naprawia lokatora.

**first-001:** `/evidence/3`, bajty [16008,17079), SHA-256 `2df0042421c36ed7bebc32080edd4b1b7e7739e170ae98dc61c4a809b39db6ae`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/3/quote/value`; bajty [16336,16461), hash `d38b22d3272b5c038a3fe35c387670fa0d6a3c67c2a309787e3f490c4ac762b8`; wartość "The Elephant unit may use Reaction Fire with both its javelins and its screen, with the player rolling separately for each.".

Pole `/evidence/3/image/bbox`; bajty [16780,16852), hash `490877511c79d7b6d4c628d19b5dbf12d6ef2608f16556aaa369e37a8a944c7e`; wartość [125, 1020, 825, 1155].

Pole `/evidence/3/image/path`; bajty [16648,16676), hash `371c47ac8788034de616a7b9891532ba48a58743af43d9f516d46116bd7c9aae`; wartość "inputs/v1/pages/pdf-32.png".

Pole `/evidence/3/image/sha256`; bajty [16696,16762), hash `cbffa2f09aa8fb632365e06adff8de9b990f6214efae8dbea3cb73275c8e533f`; wartość "e80ea90e4a3a441416fd4624be73b2f97ca7185e6bb552d89454b6121fca394a".

**context-01:** `/evidence/3`, bajty [51867,52967), SHA-256 `def8466654ac03116654db37a678407e840075d5699dad79199412d71ee6d431`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/3/quote/value`; bajty [52205,52330), hash `d38b22d3272b5c038a3fe35c387670fa0d6a3c67c2a309787e3f490c4ac762b8`; wartość "The Elephant unit may use Reaction Fire with both its javelins and its screen, with the player rolling separately for each.".

Pole `/evidence/3/image/bbox`; bajty [52657,52734), hash `425962a20009a5d061bb01eeefb4e18fc923a0a89b65e21d34f681e2b95f3ac0`; wartość [125, 1020, 825, 1155].

Pole `/evidence/3/image/path`; bajty [52523,52551), hash `371c47ac8788034de616a7b9891532ba48a58743af43d9f516d46116bd7c9aae`; wartość "inputs/v1/pages/pdf-32.png".

Pole `/evidence/3/image/sha256`; bajty [52572,52638), hash `cbffa2f09aa8fb632365e06adff8de9b990f6214efae8dbea3cb73275c8e533f`; wartość "e80ea90e4a3a441416fd4624be73b2f97ca7185e6bb552d89454b6121fca394a".

Każdy naruszony glif:

{"index": 43, "text": "s", "bbox_pdf_points": [293.12399999999985, 392.5269, 297.01399999999984, 402.5269], "bbox_pixels": [814.2333333333329, 1090.3525, 825.0388888888884, 1118.1302777777778], "overflow_pdf_points": {"left": 0, "right": 0.013999999999839474, "top": 0, "bottom": 0}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E913-boundary-0.png", "bytes": 1510, "sha256": "a5d776e5c653d0398ff02db9325f47a8e31646795b7e48b4fc89daf430a70649"}}
{"index": 102, "text": ".", "bbox_pdf_points": [294.519, 404.5269, 297.019, 414.5269], "bbox_pixels": [818.1083333333333, 1123.6858333333334, 825.0527777777778, 1151.4636111111113], "overflow_pdf_points": {"left": 0, "right": 0.019000000000005457, "top": 0, "bottom": 0}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E913-boundary-1.png", "bytes": 997, "sha256": "f63320c6211606508bb64479d0fd1df0819c22d7be5cc19b94a6fd06a3b02d9a"}}

Wyłączenia: pełny rekord/klauzula/pozostały crop, artwork/ratingi, wcześniejsze pending, brakujące procedury, automatyczne semantyczneFP/FN/gold.

## E914start

Dokładny zakres: oryginalny krótki cytat i jego prostokąt.

> Each time an Elephant unit routs, its player rolls the die and does one of the following, depending on the DR:

Niezależny dosłowny helper:

> Each time an Elephant unit routs, its player
> rolls the die and does one of the following, depending on the DR:

Helper `/regions/3/text`, znaki [1849, 1959], SHA-256 `ac873a6a1f0d4b910d140c71c80cab5ce2551c39a2c559b8c3218070a06c7ca5`.

Strona32; bbox piksele [125, 1290, 825, 1440], PDFpt [45.0, 464.4, 297.0, 518.4]; wymiary [1700, 2200].

Rzeczywisty krótki cytat PDFpt [45.0, 490.2703, 297.0099999999999, 512.2703]; całe obwiednie NIE mieszczą się. Raster: readable_no_observed_ink_loss.

Ręczne porównanie: Widoczne Each time an Elephant unit routs oraz rzut player/depending onDR. Końcowe r w player wychodzi obwiednią0.010pt. Raster krótkiego cytatu czytelny; nie oznacza przyjęcia całej tabeli Rampage.

[Dokładny nieposzerzony crop](../../../measurement/M-POC5A-semantic-04c1/visual-02/E914start-exact.png) · [Referencja do porównania granicy](../../../measurement/M-POC5A-semantic-04c1/visual-02/E914start-quote-reference.png). Referencja nie naprawia lokatora.

**first-001:** `/evidence/5`, bajty [18090,19153), SHA-256 `1351875ae271d3414d9e7253ce205e371a6a2f9b18c9eaba90ab5c45836f17af`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/5/quote/value`; bajty [18423,18535), hash `f1597c0d85c2c2be9275451d92f80b8ff1aaeb20f28122ad7602ab916be65392`; wartość "Each time an Elephant unit routs, its player rolls the die and does one of the following, depending on the DR:".

Pole `/evidence/5/image/bbox`; bajty [18854,18926), hash `7c4e28a4eb38032dedc276941e35da7680310d14b0d97ad0458500f8b7a74e71`; wartość [125, 1290, 825, 1440].

Pole `/evidence/5/image/path`; bajty [18722,18750), hash `371c47ac8788034de616a7b9891532ba48a58743af43d9f516d46116bd7c9aae`; wartość "inputs/v1/pages/pdf-32.png".

Pole `/evidence/5/image/sha256`; bajty [18770,18836), hash `cbffa2f09aa8fb632365e06adff8de9b990f6214efae8dbea3cb73275c8e533f`; wartość "e80ea90e4a3a441416fd4624be73b2f97ca7185e6bb552d89454b6121fca394a".

**context-01:** `/evidence/5`, bajty [54009,55101), SHA-256 `550036ca880031b4bf991d1fc936e049dbdf7e1227ba108e18de83391c559af9`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/5/quote/value`; bajty [54352,54464), hash `f1597c0d85c2c2be9275451d92f80b8ff1aaeb20f28122ad7602ab916be65392`; wartość "Each time an Elephant unit routs, its player rolls the die and does one of the following, depending on the DR:".

Pole `/evidence/5/image/bbox`; bajty [54791,54868), hash `53d876473efaec0502577c85e5ee0f5872a771c92b2ce2bc51c8990821631249`; wartość [125, 1290, 825, 1440].

Pole `/evidence/5/image/path`; bajty [54657,54685), hash `371c47ac8788034de616a7b9891532ba48a58743af43d9f516d46116bd7c9aae`; wartość "inputs/v1/pages/pdf-32.png".

Pole `/evidence/5/image/sha256`; bajty [54706,54772), hash `cbffa2f09aa8fb632365e06adff8de9b990f6214efae8dbea3cb73275c8e533f`; wartość "e80ea90e4a3a441416fd4624be73b2f97ca7185e6bb552d89454b6121fca394a".

Każdy naruszony glif:

{"index": 36, "text": "r", "bbox_pdf_points": [293.6799999999999, 490.2703, 297.0099999999999, 500.2703], "bbox_pixels": [815.7777777777775, 1361.8619444444446, 825.0277777777774, 1389.6397222222224], "overflow_pdf_points": {"left": 0, "right": 0.009999999999877218, "top": 0, "bottom": 0}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914start-boundary-0.png", "bytes": 1273, "sha256": "5a449d156e7f869c592b95f672869754d949c465ed0744dafe980e0abf274a2d"}}

Wyłączenia: pełny rekord/klauzula/pozostały crop, artwork/ratingi, wcześniejsze pending, brakujące procedury, automatyczne semantyczneFP/FN/gold.

## E914priority

Dokładny zakres: oryginalny krótki cytat i jego prostokąt.

> Each Elephant Rampage is always resolved immediately, before any other game mechanic is addressed, except for Orderly Withdrawal in face of the rampaging elephant (6.51).

Niezależny dosłowny helper:

> Each Elephant Rampage is always resolved immediately, before
> any other game mechanic is addressed, except for Orderly With-
> drawal in face of the rampaging elephant (6.51).

Helper `/regions/4/text`, znaki [413, 585], SHA-256 `02a592c25340243d0386010589505f5e948b390e4350d9b3413db6f909ecac88`.

Strona32; bbox piksele [875, 490, 1575, 600], PDFpt [315.0, 176.4, 567.0, 216.0]; wymiary [1700, 2200].

Rzeczywisty krótki cytat PDFpt [315.005, 180.78250000000003, 567.1139999999999, 214.78250000000003]; całe obwiednie NIE mieszczą się. Raster: readable_no_observed_ink_loss.

Ręczne porównanie: Cytat priority natychmiast/before any other mechanism i exceptOW6.51 widoczny. Źródło dzieli Withdrawal na With-/drawal; normalizacja usuwa wyłącznie koniec linii. Obwiednie e/łącznika na prawej krawędzi, max0.114pt, raster bez zaobserwowanej utraty tuszu. Nie akceptuje wykonaniaOW.

[Dokładny nieposzerzony crop](../../../measurement/M-POC5A-semantic-04c1/visual-02/E914priority-exact.png) · [Referencja do porównania granicy](../../../measurement/M-POC5A-semantic-04c1/visual-02/E914priority-quote-reference.png). Referencja nie naprawia lokatora.

**first-001:** `/evidence/8`, bajty [21209,22335), SHA-256 `29fb69a3cc45ce58ef1f65b4bc2ec1e873a8638834015f074d0a2d8978c7bcfd`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/8/quote/value`; bajty [21546,21718), hash `2f9bf20e7678c446e835e361ea1d7db031c86aced7fdbfb9e522a872bd2ae774`; wartość "Each Elephant Rampage is always resolved immediately, before any other game mechanic is addressed, except for Orderly Withdrawal in face of the rampaging elephant (6.51).".

Pole `/evidence/8/image/bbox`; bajty [22037,22108), hash `d129355ef268bf474ff56b6196e584bea9b0e95ab67380309bb2521ced90644e`; wartość [875, 490, 1575, 600].

Pole `/evidence/8/image/path`; bajty [21905,21933), hash `371c47ac8788034de616a7b9891532ba48a58743af43d9f516d46116bd7c9aae`; wartość "inputs/v1/pages/pdf-32.png".

Pole `/evidence/8/image/sha256`; bajty [21953,22019), hash `cbffa2f09aa8fb632365e06adff8de9b990f6214efae8dbea3cb73275c8e533f`; wartość "e80ea90e4a3a441416fd4624be73b2f97ca7185e6bb552d89454b6121fca394a".

**context-01:** `/evidence/8`, bajty [57218,58373), SHA-256 `145fa408b0e876e2eb0c5277b336238bd03a06a09c40254024a85d79c94364c5`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/8/quote/value`; bajty [57565,57737), hash `2f9bf20e7678c446e835e361ea1d7db031c86aced7fdbfb9e522a872bd2ae774`; wartość "Each Elephant Rampage is always resolved immediately, before any other game mechanic is addressed, except for Orderly Withdrawal in face of the rampaging elephant (6.51).".

Pole `/evidence/8/image/bbox`; bajty [58064,58140), hash `f821feea80bcaceaf33e38b080b4e5659c23db582c033b38fdee04cab517e848`; wartość [875, 490, 1575, 600].

Pole `/evidence/8/image/path`; bajty [57930,57958), hash `371c47ac8788034de616a7b9891532ba48a58743af43d9f516d46116bd7c9aae`; wartość "inputs/v1/pages/pdf-32.png".

Pole `/evidence/8/image/sha256`; bajty [57979,58045), hash `cbffa2f09aa8fb632365e06adff8de9b990f6214efae8dbea3cb73275c8e533f`; wartość "e80ea90e4a3a441416fd4624be73b2f97ca7185e6bb552d89454b6121fca394a".

Każdy naruszony glif:

{"index": 52, "text": "e", "bbox_pdf_points": [562.6739999999999, 180.78250000000003, 567.1139999999999, 190.78250000000003], "bbox_pixels": [1562.9833333333331, 502.1736111111112, 1575.3166666666664, 529.9513888888889], "overflow_pdf_points": {"left": 0, "right": 0.11399999999991905, "top": 0, "bottom": 0}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914priority-boundary-0.png", "bytes": 1474, "sha256": "e4014c0d4a4fdb3132d0466c80005e50999080c497d027f1079fddd7996969cc"}}
{"index": 105, "text": "-", "bbox_pdf_points": [563.722, 192.78250000000003, 567.052, 202.78250000000003], "bbox_pixels": [1565.8944444444444, 535.5069444444446, 1575.1444444444444, 563.2847222222223], "overflow_pdf_points": {"left": 0, "right": 0.05200000000002092, "top": 0, "bottom": 0}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914priority-boundary-1.png", "bytes": 1015, "sha256": "b00a06bdf281eaccbc856c42a020217f8102348880dd61ff1389ad38065280d8"}}

Wyłączenia: pełny rekord/klauzula/pozostały crop, artwork/ratingi, wcześniejsze pending, brakujące procedury, automatyczne semantyczneFP/FN/gold.

## E914diagram

Dokładny zakres: oryginalny krótki cytat i jego prostokąt.

> This is just an example; use the compass on the map for each battle.

Niezależny dosłowny helper:

> This is just an example; use the
> compass on the map for each battle.

Helper `/regions/4/text`, znaki [676, 744], SHA-256 `cc3250420d810eb7254001d2d21ad0417fe65bb7e11fe7bde5bdb13ed6906bcf`.

Strona32; bbox piksele [875, 610, 1575, 935], PDFpt [315.0, 219.6, 567.0, 336.6]; wymiary [1700, 2200].

Rzeczywisty krótki cytat PDFpt [315.0, 315.7786, 567.0110000000001, 337.7786]; całe obwiednie NIE mieszczą się. Raster: readable_no_observed_ink_loss.

Ręczne porównanie: Cytat pochodzi z podpisu przykładu: użyj kompasu mapy każdej bitwy. Dolna obwiednia ostatniej linii wystaje1.1786pt, lecz tusz w cytacie pozostaje przed dolną granicą; prawa obwiedniae0.011pt. Ocena samego krótkiego podpisu; diagram, liczb żetonów i geometrii kierunków nie przyjmujemy.

[Dokładny nieposzerzony crop](../../../measurement/M-POC5A-semantic-04c1/visual-02/E914diagram-exact.png) · [Referencja do porównania granicy](../../../measurement/M-POC5A-semantic-04c1/visual-02/E914diagram-quote-reference.png). Referencja nie naprawia lokatora.

**first-001:** `/evidence/9`, bajty [22341,23367), SHA-256 `928ada82047f748429dad9bad3781f400d6358da1159e6d0c38b6128f0183c3b`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/9/quote/value`; bajty [22680,22750), hash `d3d7ef238fe825492345a91c9a194d104154ab2c97b32fa8c50dfa51b637018c`; wartość "This is just an example; use the compass on the map for each battle.".

Pole `/evidence/9/image/bbox`; bajty [23069,23140), hash `e1436efefc82e0de2405da5337ae60242e874f58bd30191a1f0390c7adc6d165`; wartość [875, 610, 1575, 935].

Pole `/evidence/9/image/path`; bajty [22937,22965), hash `371c47ac8788034de616a7b9891532ba48a58743af43d9f516d46116bd7c9aae`; wartość "inputs/v1/pages/pdf-32.png".

Pole `/evidence/9/image/sha256`; bajty [22985,23051), hash `cbffa2f09aa8fb632365e06adff8de9b990f6214efae8dbea3cb73275c8e533f`; wartość "e80ea90e4a3a441416fd4624be73b2f97ca7185e6bb552d89454b6121fca394a".

**context-01:** `/evidence/9`, bajty [58380,59435), SHA-256 `bcc8559d153a909ae85e613738fd463ed85d8804ce033e87550fd732abf0116b`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/9/quote/value`; bajty [58729,58799), hash `d3d7ef238fe825492345a91c9a194d104154ab2c97b32fa8c50dfa51b637018c`; wartość "This is just an example; use the compass on the map for each battle.".

Pole `/evidence/9/image/bbox`; bajty [59126,59202), hash `7787eb9e1ed2f8fbbe8025495de9669a7c456a3aeb085214f0a914dc57e071b7`; wartość [875, 610, 1575, 935].

Pole `/evidence/9/image/path`; bajty [58992,59020), hash `371c47ac8788034de616a7b9891532ba48a58743af43d9f516d46116bd7c9aae`; wartość "inputs/v1/pages/pdf-32.png".

Pole `/evidence/9/image/sha256`; bajty [59041,59107), hash `cbffa2f09aa8fb632365e06adff8de9b990f6214efae8dbea3cb73275c8e533f`; wartość "e80ea90e4a3a441416fd4624be73b2f97ca7185e6bb552d89454b6121fca394a".

Każdy naruszony glif:

{"index": 25, "text": "e", "bbox_pdf_points": [562.571, 315.7786, 567.0110000000001, 325.7786], "bbox_pixels": [1562.6972222222223, 877.1627777777777, 1575.0305555555558, 904.9405555555554], "overflow_pdf_points": {"left": 0, "right": 0.011000000000080945, "top": 0, "bottom": 0}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914diagram-boundary-0.png", "bytes": 1681, "sha256": "ed7298f13defef67279b37436826e6c079b34065efdc2ad2e4940a9718fab301"}}
{"index": 26, "text": "c", "bbox_pdf_points": [315.0, 327.7786, 319.44, 337.7786], "bbox_pixels": [875.0, 910.496111111111, 887.3333333333334, 938.2738888888888], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1785999999999603}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914diagram-boundary-1.png", "bytes": 1412, "sha256": "d8ef67315952aa994222c10ce96733af39164be8ca1ee3888d0a48443442901a"}}
{"index": 27, "text": "o", "bbox_pdf_points": [319.44, 327.7786, 324.44, 337.7786], "bbox_pixels": [887.3333333333334, 910.496111111111, 901.2222222222222, 938.2738888888888], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1785999999999603}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914diagram-boundary-2.png", "bytes": 1827, "sha256": "6507de31f8d7c137b7aef7ca8c8b0e1c4d6831d65eb9d2642f922863041847e1"}}
{"index": 28, "text": "m", "bbox_pdf_points": [324.44, 327.7786, 331.66, 337.7786], "bbox_pixels": [901.2222222222222, 910.496111111111, 921.2777777777778, 938.2738888888888], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1785999999999603}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914diagram-boundary-3.png", "bytes": 2286, "sha256": "1c89e8f778dc57c8bb944421141b86ca1eec7e212aed7d1efd2b0b239bc9fecf"}}
{"index": 29, "text": "p", "bbox_pdf_points": [331.66, 327.7786, 336.66, 337.7786], "bbox_pixels": [921.2777777777778, 910.496111111111, 935.1666666666666, 938.2738888888888], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1785999999999603}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914diagram-boundary-4.png", "bytes": 2086, "sha256": "2eb1acbdb28b3b53097f9fcf57f7d1c2509168ffa286dd8e84837b01f6730dfb"}}
{"index": 30, "text": "a", "bbox_pdf_points": [336.66, 327.7786, 341.66, 337.7786], "bbox_pixels": [935.1666666666666, 910.496111111111, 949.0555555555555, 938.2738888888888], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1785999999999603}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914diagram-boundary-5.png", "bytes": 2026, "sha256": "7691358aae6f78c9d7e28fb8f6d5779450c2b4778c8d39c23f032921d676d6d7"}}
{"index": 31, "text": "s", "bbox_pdf_points": [341.66, 327.7786, 345.55, 337.7786], "bbox_pixels": [949.0555555555555, 910.496111111111, 959.8611111111111, 938.2738888888888], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1785999999999603}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914diagram-boundary-6.png", "bytes": 1845, "sha256": "959c0b7f61aa3e866be9f3331b1be3781bf9e1e2c67761e744f6827d25916589"}}
{"index": 32, "text": "s", "bbox_pdf_points": [345.55, 327.7786, 349.44, 337.7786], "bbox_pixels": [959.8611111111111, 910.496111111111, 970.6666666666666, 938.2738888888888], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1785999999999603}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914diagram-boundary-7.png", "bytes": 1565, "sha256": "d13ed01199ed0d794d2fbc0601c742b30cd5e5a32c24251754246f5b8bac27b4"}}
{"index": 33, "text": "o", "bbox_pdf_points": [351.94, 327.7786, 356.94, 337.7786], "bbox_pixels": [977.6111111111111, 910.496111111111, 991.5, 938.2738888888888], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1785999999999603}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914diagram-boundary-8.png", "bytes": 1598, "sha256": "6a37d0de526971e397d5529d768eb2c3337c569365badac1aac25c65073b0b0f"}}
{"index": 34, "text": "n", "bbox_pdf_points": [356.94, 327.7786, 361.94, 337.7786], "bbox_pixels": [991.5, 910.496111111111, 1005.3888888888889, 938.2738888888888], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1785999999999603}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914diagram-boundary-9.png", "bytes": 1617, "sha256": "5f3d0892ad0e961eb60df0c92ebf4c5cf4c178ea502d51810aca48eca556ca19"}}
{"index": 35, "text": "t", "bbox_pdf_points": [364.44, 327.7786, 367.21999999999997, 337.7786], "bbox_pixels": [1012.3333333333334, 910.496111111111, 1020.0555555555555, 938.2738888888888], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1785999999999603}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914diagram-boundary-10.png", "bytes": 1468, "sha256": "d650a7781f0bcc0b5aa29c88a761527fca0f19a722ee17da9df5b39c338e15d2"}}
{"index": 36, "text": "h", "bbox_pdf_points": [367.22, 327.7786, 372.22, 337.7786], "bbox_pixels": [1020.0555555555555, 910.496111111111, 1033.9444444444443, 938.2738888888888], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1785999999999603}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914diagram-boundary-11.png", "bytes": 2003, "sha256": "c84d5ffd60d0ff4938d6fa8fbac52001f71d31241bf35cb20f5ac67b344cea12"}}
{"index": 37, "text": "e", "bbox_pdf_points": [372.22, 327.7786, 376.66, 337.7786], "bbox_pixels": [1033.9444444444443, 910.496111111111, 1046.2777777777778, 938.2738888888888], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1785999999999603}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914diagram-boundary-12.png", "bytes": 1750, "sha256": "dd6c8bb3b347f80e98e34b136915383793b893ffacf3ddc9779b5d8a3b48e3ba"}}
{"index": 38, "text": "m", "bbox_pdf_points": [379.15999999999997, 327.7786, 386.38, 337.7786], "bbox_pixels": [1053.2222222222222, 910.496111111111, 1073.2777777777778, 938.2738888888888], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1785999999999603}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914diagram-boundary-13.png", "bytes": 1916, "sha256": "e3dc1dbf54abd7544c0a6e130712bfd1781a2523fd7c169bef3e0fd5789f0695"}}
{"index": 39, "text": "a", "bbox_pdf_points": [386.38, 327.7786, 391.38, 337.7786], "bbox_pixels": [1073.2777777777778, 910.496111111111, 1087.1666666666667, 938.2738888888888], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1785999999999603}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914diagram-boundary-14.png", "bytes": 2026, "sha256": "e113df1005b2c2636e05e7dfd0e6ae697443dee5557cdd2ac62b0cd2c893aaae"}}
{"index": 40, "text": "p", "bbox_pdf_points": [391.38, 327.7786, 396.38, 337.7786], "bbox_pixels": [1087.1666666666667, 910.496111111111, 1101.0555555555557, 938.2738888888888], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1785999999999603}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914diagram-boundary-15.png", "bytes": 1893, "sha256": "4e7ffe11f422f6f96d85e49f18cd1d3438a92ed5ca59925a97b0c983a46bd67b"}}
{"index": 41, "text": "f", "bbox_pdf_points": [398.88, 327.7786, 401.65999999999997, 337.7786], "bbox_pixels": [1108.0, 910.496111111111, 1115.7222222222222, 938.2738888888888], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1785999999999603}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914diagram-boundary-16.png", "bytes": 1591, "sha256": "59792286e4c92d8b66572caa117a212721ad8da100b67d068372fb58007068fe"}}
{"index": 42, "text": "o", "bbox_pdf_points": [401.65999999999997, 327.7786, 406.65999999999997, 337.7786], "bbox_pixels": [1115.7222222222222, 910.496111111111, 1129.611111111111, 938.2738888888888], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1785999999999603}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914diagram-boundary-17.png", "bytes": 2028, "sha256": "9394b8fc547747906dee561f41cd5a3f01b63a49692b569e00c8fad132bf5db6"}}
{"index": 43, "text": "r", "bbox_pdf_points": [406.65999999999997, 327.7786, 410.54999999999995, 337.7786], "bbox_pixels": [1129.611111111111, 910.496111111111, 1140.4166666666665, 938.2738888888888], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1785999999999603}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914diagram-boundary-18.png", "bytes": 1412, "sha256": "a581563776acda89390b69989c2ae97ca1980a5a46d3c941f04e308321d53a23"}}
{"index": 44, "text": "e", "bbox_pdf_points": [413.05, 327.7786, 417.49, 337.7786], "bbox_pixels": [1147.361111111111, 910.496111111111, 1159.6944444444443, 938.2738888888888], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1785999999999603}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914diagram-boundary-19.png", "bytes": 1523, "sha256": "a78b371d208a1c7866d4133fddbee1def9c94c47250ac32186fcf5943c847f73"}}
{"index": 45, "text": "a", "bbox_pdf_points": [417.49, 327.7786, 422.49, 337.7786], "bbox_pixels": [1159.6944444444443, 910.496111111111, 1173.5833333333333, 938.2738888888888], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1785999999999603}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914diagram-boundary-20.png", "bytes": 1913, "sha256": "c1eb0f9badfba0bfba86161f429855b0e9517f9f5c6d03af24df9af4c62763ca"}}
{"index": 46, "text": "c", "bbox_pdf_points": [422.49, 327.7786, 426.93, 337.7786], "bbox_pixels": [1173.5833333333333, 910.496111111111, 1185.9166666666667, 938.2738888888888], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1785999999999603}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914diagram-boundary-21.png", "bytes": 1801, "sha256": "ddf515945f037f52c9d3de278128cf43d3b534fa8fba97ec6c8d22a2bc6b24f6"}}
{"index": 47, "text": "h", "bbox_pdf_points": [426.93, 327.7786, 431.93, 337.7786], "bbox_pixels": [1185.9166666666667, 910.496111111111, 1199.8055555555557, 938.2738888888888], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1785999999999603}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914diagram-boundary-22.png", "bytes": 1756, "sha256": "62e2152cfbae88a6fd7bc102f8f60dc96a5c69cc366165e8418593452e0aec65"}}
{"index": 48, "text": "b", "bbox_pdf_points": [434.43, 327.7786, 439.43, 337.7786], "bbox_pixels": [1206.75, 910.496111111111, 1220.638888888889, 938.2738888888888], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1785999999999603}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914diagram-boundary-23.png", "bytes": 1740, "sha256": "2b28c1b82fdbfe8ba95390bde2b27352ef10dfaec4da26153b5128e373851d9b"}}
{"index": 49, "text": "a", "bbox_pdf_points": [439.43, 327.7786, 444.43, 337.7786], "bbox_pixels": [1220.638888888889, 910.496111111111, 1234.5277777777778, 938.2738888888888], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1785999999999603}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914diagram-boundary-24.png", "bytes": 1994, "sha256": "8dd561a249f2cfccb136a1f3f74f78a74a463bcdd3d569b28975fdf3d4596625"}}
{"index": 50, "text": "t", "bbox_pdf_points": [444.43, 327.7786, 447.21, 337.7786], "bbox_pixels": [1234.5277777777778, 910.496111111111, 1242.25, 938.2738888888888], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1785999999999603}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914diagram-boundary-25.png", "bytes": 1662, "sha256": "6e9d990efc22a6e412303466dcfdd6d92bed079f2333b62a165c87e04e23f3b8"}}
{"index": 51, "text": "t", "bbox_pdf_points": [447.21000000000004, 327.7786, 449.99, 337.7786], "bbox_pixels": [1242.2500000000002, 910.496111111111, 1249.9722222222222, 938.2738888888888], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1785999999999603}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914diagram-boundary-26.png", "bytes": 1664, "sha256": "b428a924824b32e6f96af2f2dc7c1f5fb3fc30827bfba40fe81c2e619fd58977"}}
{"index": 52, "text": "l", "bbox_pdf_points": [449.99, 327.7786, 452.77, 337.7786], "bbox_pixels": [1249.9722222222222, 910.496111111111, 1257.6944444444443, 938.2738888888888], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1785999999999603}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914diagram-boundary-27.png", "bytes": 1736, "sha256": "41df166d824f95b78ffd2462929cbeef81a47a9eff5cb0feefe2e2eb23f025a6"}}
{"index": 53, "text": "e", "bbox_pdf_points": [452.77000000000004, 327.7786, 457.21000000000004, 337.7786], "bbox_pixels": [1257.6944444444446, 910.496111111111, 1270.027777777778, 938.2738888888888], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1785999999999603}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914diagram-boundary-28.png", "bytes": 1748, "sha256": "ef0c729f62fc9136e20d9e4aaed2a078a22a29969d494eb6712a93b418f9f6b0"}}
{"index": 54, "text": ".", "bbox_pdf_points": [457.21000000000004, 327.7786, 459.71000000000004, 337.7786], "bbox_pixels": [1270.027777777778, 910.496111111111, 1276.9722222222224, 938.2738888888888], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1785999999999603}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914diagram-boundary-29.png", "bytes": 1119, "sha256": "c5dd26f7745eebef44abbe7788830119288b6b7ea92c630c51f0c5416f13a719"}}

Wyłączenia: pełny rekord/klauzula/pozostały crop, artwork/ratingi, wcześniejsze pending, brakujące procedury, automatyczne semantyczneFP/FN/gold.

## E914move

Dokładny zakres: oryginalny krótki cytat i jego prostokąt.

> A cavalry unit incurs 2 Cohesion Hits regardless of the angle.

Niezależny dosłowny helper:

> A cavalry unit
> incurs 2 Cohesion Hits regardless of the angle.

Helper `/regions/4/text`, znaki [1245, 1307], SHA-256 `5f46478d4fe3846c74f44d41d4a7c5282d9b5d621ce90bb30066fe80409e6e82`.

Strona32; bbox piksele [875, 945, 1575, 1430], PDFpt [315.0, 340.2, 567.0, 514.8]; wymiary [1700, 2200].

Rzeczywisty krótki cytat PDFpt [315.00000000000006, 429.17859999999996, 567.0029999999998, 451.17859999999996]; całe obwiednie NIE mieszczą się. Raster: readable_no_observed_ink_loss.

Ręczne porównanie: Cytat o cavalry2CohesionHitsregardless ofangle znajduje się w dwóch liniach. Końcowe t w unit przekracza prawą obwiednią0.003pt, bez obserwowalnej utraty rastra. Nie ocenia całego ruchu słonia lub warunków innych klas.

[Dokładny nieposzerzony crop](../../../measurement/M-POC5A-semantic-04c1/visual-02/E914move-exact.png) · [Referencja do porównania granicy](../../../measurement/M-POC5A-semantic-04c1/visual-02/E914move-quote-reference.png). Referencja nie naprawia lokatora.

**first-001:** `/evidence/10`, bajty [23373,24388), SHA-256 `91963c5a9fa9bdec67236a494cc3cc8daf78503c01dccd55647bf39a97751330`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/10/quote/value`; bajty [23706,23770), hash `5f2d0dc16417f28ee2cfcdf5bbf8c89fe87ddb587cd6546abdfb41a20d7b680b`; wartość "A cavalry unit incurs 2 Cohesion Hits regardless of the angle.".

Pole `/evidence/10/image/bbox`; bajty [24089,24161), hash `67f8abb9548ccf07c6a0977e628a82595fe3f957387806e5a3b70c0e59351da8`; wartość [875, 945, 1575, 1430].

Pole `/evidence/10/image/path`; bajty [23957,23985), hash `371c47ac8788034de616a7b9891532ba48a58743af43d9f516d46116bd7c9aae`; wartość "inputs/v1/pages/pdf-32.png".

Pole `/evidence/10/image/sha256`; bajty [24005,24071), hash `cbffa2f09aa8fb632365e06adff8de9b990f6214efae8dbea3cb73275c8e533f`; wartość "e80ea90e4a3a441416fd4624be73b2f97ca7185e6bb552d89454b6121fca394a".

**context-01:** `/evidence/10`, bajty [59442,60486), SHA-256 `b9b7aa9cc2d1d12bea75f1bf6b4c40c004704b7aed747fec50c5b67bda7e6361`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/10/quote/value`; bajty [59785,59849), hash `5f2d0dc16417f28ee2cfcdf5bbf8c89fe87ddb587cd6546abdfb41a20d7b680b`; wartość "A cavalry unit incurs 2 Cohesion Hits regardless of the angle.".

Pole `/evidence/10/image/bbox`; bajty [60176,60253), hash `fbd6604d6cee0ca230ca669f7b8047184671ea3cfb53780321c359198af799ec`; wartość [875, 945, 1575, 1430].

Pole `/evidence/10/image/path`; bajty [60042,60070), hash `371c47ac8788034de616a7b9891532ba48a58743af43d9f516d46116bd7c9aae`; wartość "inputs/v1/pages/pdf-32.png".

Pole `/evidence/10/image/sha256`; bajty [60091,60157), hash `cbffa2f09aa8fb632365e06adff8de9b990f6214efae8dbea3cb73275c8e533f`; wartość "e80ea90e4a3a441416fd4624be73b2f97ca7185e6bb552d89454b6121fca394a".

Każdy naruszony glif:

{"index": 11, "text": "t", "bbox_pdf_points": [564.2229999999998, 429.17859999999996, 567.0029999999998, 439.17859999999996], "bbox_pixels": [1567.2861111111106, 1192.1627777777776, 1575.008333333333, 1219.9405555555554], "overflow_pdf_points": {"left": 0, "right": 0.0029999999998153726, "top": 0, "bottom": 0}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914move-boundary-0.png", "bytes": 1161, "sha256": "0a62b4d514757851e413cccc13ba06a58a762e1b1381bc3353cf3b3aa30e742b"}}

Wyłączenia: pełny rekord/klauzula/pozostały crop, artwork/ratingi, wcześniejsze pending, brakujące procedury, automatyczne semantyczneFP/FN/gold.

## E914end

Dokładny zakres: oryginalny krótki cytat i jego prostokąt.

> If none of the above, after the 4th consecutive Rampage DR, the Elephant unit is eliminated.

Niezależny dosłowny helper:

> If none of the above, after the 4th consecutive Rampage DR,
> the Elephant unit is eliminated.

Helper `/regions/4/text`, znaki [1891, 1983], SHA-256 `9acdc849244e060ec95ee328031f97c3a2650960e1030f67a41fd9e608446a70`.

Strona32; bbox piksele [875, 1440, 1575, 1915], PDFpt [315.0, 518.4, 567.0, 689.4]; wymiary [1700, 2200].

Rzeczywisty krótki cytat PDFpt [324.00000000000017, 591.1786, 567.0080000000003, 613.1786]; całe obwiednie NIE mieszczą się. Raster: readable_no_observed_ink_loss.

Ręczne porównanie: Widoczne if none ofabove, after4th consecutiveRampageDR oraz elimination. Obwiednia przecinka przy prawej granicy+0.008pt. Krótki raster czytelny; kontekst none ofabove nie daje całości czterech gałęzi i nie zastępuje ich oceny.

[Dokładny nieposzerzony crop](../../../measurement/M-POC5A-semantic-04c1/visual-02/E914end-exact.png) · [Referencja do porównania granicy](../../../measurement/M-POC5A-semantic-04c1/visual-02/E914end-quote-reference.png). Referencja nie naprawia lokatora.

**first-001:** `/evidence/11`, bajty [24394,25439), SHA-256 `6a9a98355f3e9abcfb5542d6334d5153bca6dc1fc23d944b47f23e86268b8e2f`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/11/quote/value`; bajty [24726,24820), hash `7311a51f7fd164402f8ef59f7e6bc107322ad2b3528b518b67121db50795ba58`; wartość "If none of the above, after the 4th consecutive Rampage DR, the Elephant unit is eliminated.".

Pole `/evidence/11/image/bbox`; bajty [25139,25212), hash `667ab0b4dbf73f477eb41234735f0202c42d9ec2a484200431e89c91089d82b3`; wartość [875, 1440, 1575, 1915].

Pole `/evidence/11/image/path`; bajty [25007,25035), hash `371c47ac8788034de616a7b9891532ba48a58743af43d9f516d46116bd7c9aae`; wartość "inputs/v1/pages/pdf-32.png".

Pole `/evidence/11/image/sha256`; bajty [25055,25121), hash `cbffa2f09aa8fb632365e06adff8de9b990f6214efae8dbea3cb73275c8e533f`; wartość "e80ea90e4a3a441416fd4624be73b2f97ca7185e6bb552d89454b6121fca394a".

**context-01:** `/evidence/11`, bajty [60493,61567), SHA-256 `a99176e74d56f7b143de42ec3c3e4db5b7186c6b40ed764fa394b7042ec67014`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/11/quote/value`; bajty [60835,60929), hash `7311a51f7fd164402f8ef59f7e6bc107322ad2b3528b518b67121db50795ba58`; wartość "If none of the above, after the 4th consecutive Rampage DR, the Elephant unit is eliminated.".

Pole `/evidence/11/image/bbox`; bajty [61256,61334), hash `493d7f928c1648f823685d811837ab16d9a9f9dbdb0546cbe609c1e27d1d475f`; wartość [875, 1440, 1575, 1915].

Pole `/evidence/11/image/path`; bajty [61122,61150), hash `371c47ac8788034de616a7b9891532ba48a58743af43d9f516d46116bd7c9aae`; wartość "inputs/v1/pages/pdf-32.png".

Pole `/evidence/11/image/sha256`; bajty [61171,61237), hash `cbffa2f09aa8fb632365e06adff8de9b990f6214efae8dbea3cb73275c8e533f`; wartość "e80ea90e4a3a441416fd4624be73b2f97ca7185e6bb552d89454b6121fca394a".

Każdy naruszony glif:

{"index": 48, "text": ",", "bbox_pdf_points": [564.5080000000003, 591.1786, 567.0080000000003, 601.1786], "bbox_pixels": [1568.0777777777785, 1642.1627777777776, 1575.022222222223, 1669.9405555555554], "overflow_pdf_points": {"left": 0, "right": 0.008000000000265572, "top": 0, "bottom": 0}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914end-boundary-0.png", "bytes": 1280, "sha256": "ede7352620497e27329809568feeba14445b53d944c45aa17e9e90b7b1d431dd"}}

Wyłączenia: pełny rekord/klauzula/pozostały crop, artwork/ratingi, wcześniejsze pending, brakujące procedury, automatyczne semantyczneFP/FN/gold.

## E914cont

Dokładny zakres: oryginalny krótki cytat i jego prostokąt.

> undertaken until its conclusion, so there may never be more than one rampaging Elephant unit at any one time.

Niezależny dosłowny helper:

> undertaken until its conclusion, so there may never be more than
> one rampaging Elephant unit at any one time.

Helper `/regions/5/text`, znaki [0, 109], SHA-256 `33092abd506c5d96784663c8deccc6cc08e44a7c6ca1fbc8f03c2d310d8e693a`.

Strona33; bbox piksele [125, 125, 825, 205], PDFpt [45.0, 45.0, 297.0, 73.8]; wymiary [1700, 2200].

Rzeczywisty krótki cytat PDFpt [45.0, 54.003600000000006, 297.0480000000001, 76.0036]; całe obwiednie NIE mieszczą się. Raster: readable_but_descender_ink_clipped.

Ręczne porównanie: Dokładny crop urywa dolne części p/g/y w drugiej linii continuation. Dolna obwiednia cytatu wystaje2.2036pt, a piksele descenderów widać pod oryginalną granicą w referencji i powiększeniu. Zdanie można odczytać i źródło potwierdza one rampaging Elephant at any one time, ale dowód nie zawiera całych znaków. Bez pewnego błędu odczytu reguły.

[Dokładny nieposzerzony crop](../../../measurement/M-POC5A-semantic-04c1/visual-02/E914cont-exact.png) · [Referencja do porównania granicy](../../../measurement/M-POC5A-semantic-04c1/visual-02/E914cont-quote-reference.png). Referencja nie naprawia lokatora.

**first-001:** `/evidence/13`, bajty [26508,27567), SHA-256 `f4da4c5d4acaa698470c58aa2505fa9e2bcf2d06dc84299b497f08dda750640f`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/13/quote/value`; bajty [26840,26951), hash `96ac9e5260557a2804a3a6ac5030c7118a85072e19527e059ed288b4eb321c59`; wartość "undertaken until its conclusion, so there may never be more than one rampaging Elephant unit at any one time.".

Pole `/evidence/13/image/bbox`; bajty [27270,27340), hash `c29e1183e0eb1086d8c0d0db8fabcb5619dfd7716ed6840ebd86ad9bf71e07b5`; wartość [125, 125, 825, 205].

Pole `/evidence/13/image/path`; bajty [27138,27166), hash `1c49839769a02a21298c8538d089fe44e0d18382b94e4d090a87a9fb965d9385`; wartość "inputs/v1/pages/pdf-33.png".

Pole `/evidence/13/image/sha256`; bajty [27186,27252), hash `c47d60a64b680805cd7eb4db56f02de372504566bd631f76f3ea50cd64e4fc1b`; wartość "ac53150f19a795383afe05e4fc668105b2b04d54fb9b2488e6557b12bd683983".

**context-01:** `/evidence/13`, bajty [62667,63755), SHA-256 `b84df2b8f0e1296c1e057f7e272a0c65d5f916a4397426252f7e76ef136b3241`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/13/quote/value`; bajty [63009,63120), hash `96ac9e5260557a2804a3a6ac5030c7118a85072e19527e059ed288b4eb321c59`; wartość "undertaken until its conclusion, so there may never be more than one rampaging Elephant unit at any one time.".

Pole `/evidence/13/image/bbox`; bajty [63447,63522), hash `722dd6c1d91b2dca869c28c6791c92bef1773fa1763cb843dcbac8443b23f756`; wartość [125, 125, 825, 205].

Pole `/evidence/13/image/path`; bajty [63313,63341), hash `1c49839769a02a21298c8538d089fe44e0d18382b94e4d090a87a9fb965d9385`; wartość "inputs/v1/pages/pdf-33.png".

Pole `/evidence/13/image/sha256`; bajty [63362,63428), hash `c47d60a64b680805cd7eb4db56f02de372504566bd631f76f3ea50cd64e4fc1b`; wartość "ac53150f19a795383afe05e4fc668105b2b04d54fb9b2488e6557b12bd683983".

Każdy naruszony glif:

{"index": 53, "text": "n", "bbox_pdf_points": [292.0480000000001, 54.003600000000006, 297.0480000000001, 64.0036], "bbox_pixels": [811.2444444444448, 150.01000000000002, 825.1333333333337, 177.7877777777778], "overflow_pdf_points": {"left": 0, "right": 0.048000000000115506, "top": 0, "bottom": 0}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-0.png", "bytes": 1439, "sha256": "ae5a808c6b43bda281dfa5395af4ecc9ec9facb74b8f30fa097b97dae89332f3"}}
{"index": 54, "text": "o", "bbox_pdf_points": [45.0, 66.0036, 50.0, 76.0036], "bbox_pixels": [125.0, 183.34333333333336, 138.88888888888889, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-1.png", "bytes": 1469, "sha256": "ff8a78108b1efd2e4045826b00417606779e4f7108afa7108bc27a27170fa5a0"}}
{"index": 55, "text": "n", "bbox_pdf_points": [50.0, 66.0036, 55.0, 76.0036], "bbox_pixels": [138.88888888888889, 183.34333333333336, 152.77777777777777, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-2.png", "bytes": 1734, "sha256": "50d3690183b23e91b801e0ce6ad4720357b4034dc6932a8f0df85269a03a7621"}}
{"index": 56, "text": "e", "bbox_pdf_points": [55.0, 66.0036, 59.44, 76.0036], "bbox_pixels": [152.77777777777777, 183.34333333333336, 165.11111111111111, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-3.png", "bytes": 1469, "sha256": "9a532702035ea1ba4f1c319715aa27e38f5ece707f2e156834f22f9d3b941950"}}
{"index": 57, "text": "r", "bbox_pdf_points": [61.94, 66.0036, 65.27, 76.0036], "bbox_pixels": [172.05555555555554, 183.34333333333336, 181.30555555555554, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-4.png", "bytes": 1362, "sha256": "0673ba8a8737004bce58c6f914c9db79e41771387e7e7ebcad138ad3370db873"}}
{"index": 58, "text": "a", "bbox_pdf_points": [65.27000000000001, 66.0036, 69.71000000000001, 76.0036], "bbox_pixels": [181.30555555555557, 183.34333333333336, 193.6388888888889, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-5.png", "bytes": 1611, "sha256": "fd96d5554a35b20f43a75dc9c487bb74275386a3183317ed3efb08854f13dbe6"}}
{"index": 59, "text": "m", "bbox_pdf_points": [69.71000000000001, 66.0036, 77.49000000000001, 76.0036], "bbox_pixels": [193.6388888888889, 183.34333333333336, 215.25000000000006, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-6.png", "bytes": 2062, "sha256": "f83f7d6e3d59c9c8c15ab942a4debe614862ceb89121b809c1ac4dbce3866408"}}
{"index": 60, "text": "p", "bbox_pdf_points": [77.49000000000001, 66.0036, 82.49000000000001, 76.0036], "bbox_pixels": [215.25000000000006, 183.34333333333336, 229.13888888888894, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 8, "dark_pixels_sample": [[217, 205], [218, 205], [217, 206], [218, 206], [216, 207], [217, 207], [218, 207], [219, 207]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-7.png", "bytes": 1885, "sha256": "9aaf7686ea9d4260978f177153531edd1b35e5bfc00a7120fb03d171bde58141"}}
{"index": 61, "text": "a", "bbox_pdf_points": [82.49000000000001, 66.0036, 86.93, 76.0036], "bbox_pixels": [229.13888888888894, 183.34333333333336, 241.47222222222223, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-8.png", "bytes": 1890, "sha256": "c55a6c0e25f1a729651355f740f833a126ea2f36d0528f8cd14524a5029444ff"}}
{"index": 62, "text": "g", "bbox_pdf_points": [86.93, 66.0036, 91.93, 76.0036], "bbox_pixels": [241.47222222222223, 183.34333333333336, 255.36111111111111, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 14, "dark_pixels_sample": [[242, 205], [243, 205], [244, 205], [243, 206], [244, 206], [245, 206], [246, 206], [250, 206], [251, 206], [245, 207], [246, 207], [247, 207]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-9.png", "bytes": 2036, "sha256": "27d991a3d387c5973c5ef4b5f2dbe3d247606dd14c72d6d9fbf2f69fe283516f"}}
{"index": 63, "text": "i", "bbox_pdf_points": [91.93, 66.0036, 94.71000000000001, 76.0036], "bbox_pixels": [255.36111111111111, 183.34333333333336, 263.0833333333333, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-10.png", "bytes": 1574, "sha256": "d96daf7ff486735edc91556ba12f497204796cf6d50b2deea980119185ac8cfd"}}
{"index": 64, "text": "n", "bbox_pdf_points": [94.71000000000001, 66.0036, 99.71000000000001, 76.0036], "bbox_pixels": [263.0833333333333, 183.34333333333336, 276.97222222222223, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-11.png", "bytes": 1769, "sha256": "9364cf865d32e2158b3eb33e20ba6f828a3b2fb469878ec0cc31786611a2562a"}}
{"index": 65, "text": "g", "bbox_pdf_points": [99.71000000000001, 66.0036, 104.71000000000001, 76.0036], "bbox_pixels": [276.97222222222223, 183.34333333333336, 290.8611111111111, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 15, "dark_pixels_sample": [[278, 205], [279, 205], [288, 205], [278, 206], [279, 206], [280, 206], [281, 206], [282, 206], [285, 206], [286, 206], [287, 206], [281, 207]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-12.png", "bytes": 1729, "sha256": "551d62834923d94dee54a6a7001783f1677a3868e7fe1d19519d7177ba565724"}}
{"index": 66, "text": "E", "bbox_pdf_points": [107.21000000000001, 66.0036, 113.32000000000001, 76.0036], "bbox_pixels": [297.80555555555554, 183.34333333333336, 314.77777777777777, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-13.png", "bytes": 1429, "sha256": "b6f69dbc90ee5d78e72d55a3140d5ccadbcfb40840998475b074c400fbffc6bc"}}
{"index": 67, "text": "l", "bbox_pdf_points": [113.32, 66.0036, 116.1, 76.0036], "bbox_pixels": [314.77777777777777, 183.34333333333336, 322.5, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-14.png", "bytes": 1483, "sha256": "63b85c0ed1f18b6a28d04e1e39717e054d5178846254691b3f387cda44fc095f"}}
{"index": 68, "text": "e", "bbox_pdf_points": [116.1, 66.0036, 120.53999999999999, 76.0036], "bbox_pixels": [322.5, 183.34333333333336, 334.8333333333333, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-15.png", "bytes": 1649, "sha256": "3b6ab741c159a76e74821d548c45d3527532ae60bc62192336f051139afbe2f1"}}
{"index": 69, "text": "p", "bbox_pdf_points": [120.53999999999999, 66.0036, 125.53999999999999, 76.0036], "bbox_pixels": [334.8333333333333, 183.34333333333336, 348.72222222222223, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 8, "dark_pixels_sample": [[337, 205], [338, 205], [337, 206], [338, 206], [336, 207], [337, 207], [338, 207], [339, 207]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-16.png", "bytes": 1861, "sha256": "3b54962b0c61967c8ce74f5352437dfb608a21866aa1570e9ddeeed1b36d5cfa"}}
{"index": 70, "text": "h", "bbox_pdf_points": [125.53999999999999, 66.0036, 130.54, 76.0036], "bbox_pixels": [348.72222222222223, 183.34333333333336, 362.6111111111111, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-17.png", "bytes": 1894, "sha256": "8e683084e220e588621d44fe2ff27cc25fc0f6ddbf51e96520fd1962e539e04e"}}
{"index": 71, "text": "a", "bbox_pdf_points": [130.54, 66.0036, 134.98, 76.0036], "bbox_pixels": [362.6111111111111, 183.34333333333336, 374.9444444444444, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-18.png", "bytes": 1626, "sha256": "11da00261dab7532e9c61fc198afa2fea9bdf218ecbd734c9d455c408f21f46f"}}
{"index": 72, "text": "n", "bbox_pdf_points": [134.98, 66.0036, 139.98, 76.0036], "bbox_pixels": [374.9444444444444, 183.34333333333336, 388.83333333333326, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-19.png", "bytes": 1736, "sha256": "ee1325d24b254b55995225c6c745aa01510dd19e436e021508451f67ccea4b58"}}
{"index": 73, "text": "t", "bbox_pdf_points": [139.98, 66.0036, 142.76, 76.0036], "bbox_pixels": [388.83333333333326, 183.34333333333336, 396.5555555555555, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-20.png", "bytes": 1192, "sha256": "0ce9cb45a748da905fcae9b6b8365adfec6e1a012c5749e943cc980d66fc41c5"}}
{"index": 74, "text": "u", "bbox_pdf_points": [145.26, 66.0036, 150.26, 76.0036], "bbox_pixels": [403.49999999999994, 183.34333333333336, 417.38888888888886, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-21.png", "bytes": 1395, "sha256": "ba5f605ae175f0cd8e885bb60d081529489f509cd2e38668348d5abdb0a7c51e"}}
{"index": 75, "text": "n", "bbox_pdf_points": [150.26, 66.0036, 155.26, 76.0036], "bbox_pixels": [417.38888888888886, 183.34333333333336, 431.27777777777777, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-22.png", "bytes": 1611, "sha256": "7835d3a5029e6e5249d1dace4b757882fdc2a6c11168bb86076e254a1ddf71a1"}}
{"index": 76, "text": "i", "bbox_pdf_points": [155.26, 66.0036, 158.04, 76.0036], "bbox_pixels": [431.27777777777777, 183.34333333333336, 439.0, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-23.png", "bytes": 1398, "sha256": "a64a29425b0e91e378af9d87bd71a9e0d3610afc92fd81b203270cbfd55caae9"}}
{"index": 77, "text": "t", "bbox_pdf_points": [158.04000000000002, 66.0036, 160.82000000000002, 76.0036], "bbox_pixels": [439.0000000000001, 183.34333333333336, 446.72222222222234, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-24.png", "bytes": 1234, "sha256": "c6702ec72a67423cf26a1ba1e2642aa8d8a1707ef299101961ee1c97ffc4f429"}}
{"index": 78, "text": "a", "bbox_pdf_points": [163.32, 66.0036, 167.76, 76.0036], "bbox_pixels": [453.6666666666667, 183.34333333333336, 466.0, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-25.png", "bytes": 1513, "sha256": "1f43b3555f5aacd512989347c8aa688b797376a239e861791d2011b76cd5ab7e"}}
{"index": 79, "text": "t", "bbox_pdf_points": [167.76000000000002, 66.0036, 170.54000000000002, 76.0036], "bbox_pixels": [466.0000000000001, 183.34333333333336, 473.72222222222234, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-26.png", "bytes": 1302, "sha256": "3c30f2c2e1b63379f041f97b157ea4bd723f64b404b9d265d8c35c495dabe541"}}
{"index": 80, "text": "a", "bbox_pdf_points": [173.04000000000002, 66.0036, 177.48000000000002, 76.0036], "bbox_pixels": [480.66666666666674, 183.34333333333336, 493.0000000000001, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-27.png", "bytes": 1532, "sha256": "c211fd514004c16b30f737bbc80e89c28c31f04f6432d8f1e9d526e2c9b5af72"}}
{"index": 81, "text": "n", "bbox_pdf_points": [177.48000000000002, 66.0036, 182.48000000000002, 76.0036], "bbox_pixels": [493.0000000000001, 183.34333333333336, 506.88888888888897, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-28.png", "bytes": 1775, "sha256": "abb2f9b3f5692ff83e42ae571790dac6a2f6af14c600cfbc154390b4e75d0bec"}}
{"index": 82, "text": "y", "bbox_pdf_points": [182.48000000000002, 66.0036, 187.48000000000002, 76.0036], "bbox_pixels": [506.88888888888897, 183.34333333333336, 520.7777777777778, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 8, "dark_pixels_sample": [[512, 205], [508, 206], [509, 206], [510, 206], [511, 206], [508, 207], [509, 207], [510, 207]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-29.png", "bytes": 1593, "sha256": "55595e3e16c982784ec2db2c91d1d42fb3cf56370fbe8fd9fa77d4e51c602f91"}}
{"index": 83, "text": "o", "bbox_pdf_points": [189.98000000000002, 66.0036, 194.98000000000002, 76.0036], "bbox_pixels": [527.7222222222223, 183.34333333333336, 541.6111111111112, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-30.png", "bytes": 1508, "sha256": "451751a686122fe53c8fdef62e69f0bd3912bba22009de0780042c8ca92a973d"}}
{"index": 84, "text": "n", "bbox_pdf_points": [194.98000000000002, 66.0036, 199.98000000000002, 76.0036], "bbox_pixels": [541.6111111111112, 183.34333333333336, 555.5000000000001, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-31.png", "bytes": 1737, "sha256": "3c56e97db802dba4070710c7a5893251449a566a5ce4a4fa701a3fd2430cb3f1"}}
{"index": 85, "text": "e", "bbox_pdf_points": [199.98000000000002, 66.0036, 204.42000000000002, 76.0036], "bbox_pixels": [555.5000000000001, 183.34333333333336, 567.8333333333334, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-32.png", "bytes": 1396, "sha256": "657d062581367e52314e6158d1ee3316666c7a943a49be5c9b43bb13eccd0da3"}}
{"index": 86, "text": "t", "bbox_pdf_points": [206.92000000000004, 66.0036, 209.70000000000005, 76.0036], "bbox_pixels": [574.7777777777778, 183.34333333333336, 582.5000000000001, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-33.png", "bytes": 1254, "sha256": "a830329c7c59f326452aebc390944592f23e4bedf565faeb27b6f662beb89c75"}}
{"index": 87, "text": "i", "bbox_pdf_points": [209.70000000000002, 66.0036, 212.48000000000002, 76.0036], "bbox_pixels": [582.5, 183.34333333333336, 590.2222222222223, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-34.png", "bytes": 1393, "sha256": "34fac5f966a3285f0c021638bde3677418638c72c982035ea20fa2f4a50f5f1d"}}
{"index": 88, "text": "m", "bbox_pdf_points": [212.48000000000002, 66.0036, 220.26000000000002, 76.0036], "bbox_pixels": [590.2222222222223, 183.34333333333336, 611.8333333333335, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-35.png", "bytes": 1923, "sha256": "8f54d82c4b259867c4e838288301ae0d2c412776aaed9bcdd182bdf29b30da19"}}
{"index": 89, "text": "e", "bbox_pdf_points": [220.26, 66.0036, 224.7, 76.0036], "bbox_pixels": [611.8333333333334, 183.34333333333336, 624.1666666666666, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-36.png", "bytes": 1531, "sha256": "f32425e8735c4050c151fa9c3630c1b24c4223ddf0b01fce4ff2a99667693ca7"}}
{"index": 90, "text": ".", "bbox_pdf_points": [224.7, 66.0036, 227.2, 76.0036], "bbox_pixels": [624.1666666666666, 183.34333333333336, 631.1111111111111, 211.12111111111113], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.2036000000000087}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E914cont-boundary-37.png", "bytes": 1093, "sha256": "00343ac6768902ee979ae275fb58cd8876df61ea002c3fb3491b4881a1bc2730"}}

Wyłączenia: pełny rekord/klauzula/pozostały crop, artwork/ratingi, wcześniejsze pending, brakujące procedury, automatyczne semantyczneFP/FN/gold.

## E915

Dokładny zakres: oryginalny krótki cytat i jego prostokąt.

> Cavalry units may never voluntarily move into the ZOC of an enemy Elephant unit.

Niezależny dosłowny helper:

> Cavalry units may never voluntarily
> move into the ZOC of an enemy Elephant unit.

Helper `/regions/5/text`, znaki [359, 439], SHA-256 `5cb6a57a7a1f55d9866524661666a27b6c0afdb660864cfa70351f794a3f2578`.

Strona33; bbox piksele [125, 385, 825, 685], PDFpt [45.0, 138.6, 297.0, 246.6]; wymiary [1700, 2200].

Rzeczywisty krótki cytat PDFpt [45.0, 139.74700000000007, 297.1300000000002, 161.74700000000007]; całe obwiednie NIE mieszczą się. Raster: readable_no_observed_ink_loss.

Ręczne porównanie: Cytat zakazu dobrowolnego wejścia cavalry do enemyElephantZOC widoczny. y w voluntarily przekracza prawą obwiednią0.130pt; powiększenie pokazuje tusz po wewnętrznej stronie granicy. Nie ocenia wszystkich kosztów/przewag9.15 lub geometriiZOC.

[Dokładny nieposzerzony crop](../../../measurement/M-POC5A-semantic-04c1/visual-02/E915-exact.png) · [Referencja do porównania granicy](../../../measurement/M-POC5A-semantic-04c1/visual-02/E915-quote-reference.png). Referencja nie naprawia lokatora.

**first-001:** `/evidence/14`, bajty [27573,28599), SHA-256 `b210007a9da2bec0fe3baad484b3968fdfdc57c736237ca27cecf6cf7f453102`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/14/quote/value`; bajty [27901,27983), hash `62fcfd629a26cb64a9bf60b4846eb52e33b29e0e49938dd19903c57ab1f03496`; wartość "Cavalry units may never voluntarily move into the ZOC of an enemy Elephant unit.".

Pole `/evidence/14/image/bbox`; bajty [28302,28372), hash `1846d92dc91d1787c84b528b7cccf5f3e6b689daebc5e9110ac7bcd045232cad`; wartość [125, 385, 825, 685].

Pole `/evidence/14/image/path`; bajty [28170,28198), hash `1c49839769a02a21298c8538d089fe44e0d18382b94e4d090a87a9fb965d9385`; wartość "inputs/v1/pages/pdf-33.png".

Pole `/evidence/14/image/sha256`; bajty [28218,28284), hash `c47d60a64b680805cd7eb4db56f02de372504566bd631f76f3ea50cd64e4fc1b`; wartość "ac53150f19a795383afe05e4fc668105b2b04d54fb9b2488e6557b12bd683983".

**context-01:** `/evidence/14`, bajty [63762,64817), SHA-256 `3c817e57aab1b3530584b15adb9dd94801215d54455484ae8995e2f9d889607f`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/14/quote/value`; bajty [64100,64182), hash `62fcfd629a26cb64a9bf60b4846eb52e33b29e0e49938dd19903c57ab1f03496`; wartość "Cavalry units may never voluntarily move into the ZOC of an enemy Elephant unit.".

Pole `/evidence/14/image/bbox`; bajty [64509,64584), hash `463cab4715309003b243e7aac7581ef28e764616d225ab1e7ec3fd72369c2c25`; wartość [125, 385, 825, 685].

Pole `/evidence/14/image/path`; bajty [64375,64403), hash `1c49839769a02a21298c8538d089fe44e0d18382b94e4d090a87a9fb965d9385`; wartość "inputs/v1/pages/pdf-33.png".

Pole `/evidence/14/image/sha256`; bajty [64424,64490), hash `c47d60a64b680805cd7eb4db56f02de372504566bd631f76f3ea50cd64e4fc1b`; wartość "ac53150f19a795383afe05e4fc668105b2b04d54fb9b2488e6557b12bd683983".

Każdy naruszony glif:

{"index": 30, "text": "y", "bbox_pdf_points": [292.1300000000002, 139.74700000000007, 297.1300000000002, 149.74700000000007], "bbox_pixels": [811.4722222222229, 388.1861111111113, 825.3611111111118, 415.9638888888891], "overflow_pdf_points": {"left": 0, "right": 0.13000000000022283, "top": 0, "bottom": 0}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E915-boundary-0.png", "bytes": 1560, "sha256": "4b9f8fecabe3fa55ded954b15ca880acd047b5b4c511d590f0c68b57a174c358"}}

Wyłączenia: pełny rekord/klauzula/pozostały crop, artwork/ratingi, wcześniejsze pending, brakujące procedury, automatyczne semantyczneFP/FN/gold.

## E916

Dokładny zakres: oryginalny krótki cytat i jego prostokąt.

> This rule does not apply to Leader Elephants.

Niezależny dosłowny helper:

> This rule does not
> apply to Leader Elephants.

Helper `/regions/5/text`, znaki [1426, 1471], SHA-256 `ecf3e4e3218f9e6d43469cfde428232915ab4a041dc6b4bd91fe0219996ef447`.

Strona33; bbox piksele [125, 700, 825, 1000], PDFpt [45.0, 252.0, 297.0, 360.0]; wymiary [1700, 2200].

Rzeczywisty krótki cytat PDFpt [45.0, 349.147, 297.001, 371.147]; całe obwiednie NIE mieszczą się. Raster: missing_final_quote_line.

Ręczne porównanie: Źródło zawiera This rule does not apply to Leader Elephants. Crop kończy się na This rule does not; następna linia apply to Leader Elephants. w całości wypada poza wskazanym obszarem. Dolna obwiednia ostatniej linii371.147pt przy bboxbottom360pt:11.147pt/~30.96px. Nie jest to drobny margines fontu; brak istotnej części cytatu. Wyjątek jest zapisany w odpowiedzi i na pełnej stronie, więc wada lokatora nie dowodzi semantycznego pominięcia albo złego odczytu; SEM-001/EXP-017 osobno.

[Dokładny nieposzerzony crop](../../../measurement/M-POC5A-semantic-04c1/visual-02/E916-exact.png) · [Referencja do porównania granicy](../../../measurement/M-POC5A-semantic-04c1/visual-02/E916-quote-reference.png). Referencja nie naprawia lokatora.

**first-001:** `/evidence/15`, bajty [28605,29597), SHA-256 `9e4f30da57821c33dd930a08581e936b9990433103927de53462965fd0a0baf7`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/15/quote/value`; bajty [28933,28980), hash `d7f4685fc12f57b4efa53487758dad7b4fd040575cb2bdfb31a8701a8477cbb5`; wartość "This rule does not apply to Leader Elephants.".

Pole `/evidence/15/image/bbox`; bajty [29299,29370), hash `6184eb97e1ad93f73c970aeb86fcc221b137950c51c67d037fd425809e587d9f`; wartość [125, 700, 825, 1000].

Pole `/evidence/15/image/path`; bajty [29167,29195), hash `1c49839769a02a21298c8538d089fe44e0d18382b94e4d090a87a9fb965d9385`; wartość "inputs/v1/pages/pdf-33.png".

Pole `/evidence/15/image/sha256`; bajty [29215,29281), hash `c47d60a64b680805cd7eb4db56f02de372504566bd631f76f3ea50cd64e4fc1b`; wartość "ac53150f19a795383afe05e4fc668105b2b04d54fb9b2488e6557b12bd683983".

**context-01:** `/evidence/15`, bajty [64824,65845), SHA-256 `b9ea1eb8048dde08eb59af663518460a7ac056c3419da5e46c58df1fdf78e4f8`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/15/quote/value`; bajty [65162,65209), hash `d7f4685fc12f57b4efa53487758dad7b4fd040575cb2bdfb31a8701a8477cbb5`; wartość "This rule does not apply to Leader Elephants.".

Pole `/evidence/15/image/bbox`; bajty [65536,65612), hash `a790098d10c3776c6a778f14b3c1b1348b40a5682f2e7d423c0be3e014c742ae`; wartość [125, 700, 825, 1000].

Pole `/evidence/15/image/path`; bajty [65402,65430), hash `1c49839769a02a21298c8538d089fe44e0d18382b94e4d090a87a9fb965d9385`; wartość "inputs/v1/pages/pdf-33.png".

Pole `/evidence/15/image/sha256`; bajty [65451,65517), hash `c47d60a64b680805cd7eb4db56f02de372504566bd631f76f3ea50cd64e4fc1b`; wartość "ac53150f19a795383afe05e4fc668105b2b04d54fb9b2488e6557b12bd683983".

Każdy naruszony glif:

{"index": 14, "text": "t", "bbox_pdf_points": [294.221, 349.147, 297.001, 359.147], "bbox_pixels": [817.2805555555556, 969.8527777777778, 825.0027777777777, 997.6305555555556], "overflow_pdf_points": {"left": 0, "right": 0.0009999999999763531, "top": 0, "bottom": 0}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E916-boundary-0.png", "bytes": 1274, "sha256": "cc16214379d1509a2d12726624febd09468d49749d6f97fa29b8d9ac30a97679"}}
{"index": 15, "text": "a", "bbox_pdf_points": [45.0, 361.147, 49.44, 371.147], "bbox_pixels": [125.0, 1003.1861111111111, 137.33333333333334, 1030.963888888889], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 11.146999999999991}, "dark_pixels_outside_original_crop": 48, "dark_pixels_sample": [[130, 1009], [131, 1009], [128, 1010], [132, 1010], [133, 1010], [127, 1011], [128, 1011], [133, 1011], [134, 1011], [127, 1012], [128, 1012], [133, 1012]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E916-boundary-1.png", "bytes": 1541, "sha256": "c65618838c48a413a4a47989da35e7975b8d28dff9139cde9eac9d1a81f35bfb"}}
{"index": 16, "text": "p", "bbox_pdf_points": [49.44, 361.147, 54.44, 371.147], "bbox_pixels": [137.33333333333334, 1003.1861111111111, 151.22222222222223, 1030.963888888889], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 11.146999999999991}, "dark_pixels_outside_original_crop": 60, "dark_pixels_sample": [[145, 1009], [138, 1010], [139, 1010], [140, 1010], [143, 1010], [144, 1010], [145, 1010], [146, 1010], [147, 1010], [139, 1011], [140, 1011], [142, 1011]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E916-boundary-2.png", "bytes": 1878, "sha256": "9804c1c05d03784719b500a9181b777cd8c9bbdd3adcea7b00f08926d7a187e9"}}
{"index": 17, "text": "p", "bbox_pdf_points": [54.44, 361.147, 59.44, 371.147], "bbox_pixels": [151.22222222222223, 1003.1861111111111, 165.11111111111111, 1030.963888888889], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 11.146999999999991}, "dark_pixels_outside_original_crop": 71, "dark_pixels_sample": [[159, 1009], [152, 1010], [153, 1010], [154, 1010], [157, 1010], [158, 1010], [159, 1010], [160, 1010], [161, 1010], [153, 1011], [154, 1011], [156, 1011]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E916-boundary-3.png", "bytes": 1802, "sha256": "b64a66be9564fc1e5f2a39638a93c32c6c41a8b9dca566e172e7fbed24160b64"}}
{"index": 18, "text": "l", "bbox_pdf_points": [59.44, 361.147, 62.22, 371.147], "bbox_pixels": [165.11111111111111, 1003.1861111111111, 172.83333333333334, 1030.963888888889], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 11.146999999999991}, "dark_pixels_outside_original_crop": 41, "dark_pixels_sample": [[168, 1003], [169, 1003], [167, 1004], [168, 1004], [169, 1004], [168, 1005], [169, 1005], [168, 1006], [169, 1006], [168, 1007], [169, 1007], [168, 1008]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E916-boundary-4.png", "bytes": 1615, "sha256": "f8d861d26b8f1606ba8418c05e3b38f29799c42fca2072d196fabee1d6a834e6"}}
{"index": 19, "text": "y", "bbox_pdf_points": [62.22, 361.147, 67.22, 371.147], "bbox_pixels": [172.83333333333334, 1003.1861111111111, 186.72222222222223, 1030.963888888889], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 11.146999999999991}, "dark_pixels_outside_original_crop": 44, "dark_pixels_sample": [[174, 1010], [175, 1010], [176, 1010], [184, 1010], [175, 1011], [176, 1011], [184, 1011], [175, 1012], [176, 1012], [183, 1012], [176, 1013], [177, 1013]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E916-boundary-5.png", "bytes": 1562, "sha256": "60e5fac4e66b3768d3161cd471e2eef22300b73eaad89565571093138422e8ea"}}
{"index": 20, "text": "t", "bbox_pdf_points": [69.72, 361.147, 72.5, 371.147], "bbox_pixels": [193.66666666666666, 1003.1861111111111, 201.38888888888889, 1030.963888888889], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 11.146999999999991}, "dark_pixels_outside_original_crop": 32, "dark_pixels_sample": [[197, 1006], [197, 1007], [196, 1008], [197, 1008], [195, 1009], [196, 1009], [197, 1009], [196, 1010], [197, 1010], [196, 1011], [197, 1011], [196, 1012]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E916-boundary-6.png", "bytes": 1271, "sha256": "82a5df980b42eada6d4351507eae036c3811248399064fdfb4b9e2a395c99f27"}}
{"index": 21, "text": "o", "bbox_pdf_points": [72.5, 361.147, 77.5, 371.147], "bbox_pixels": [201.38888888888889, 1003.1861111111111, 215.27777777777777, 1030.963888888889], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 11.146999999999991}, "dark_pixels_outside_original_crop": 51, "dark_pixels_sample": [[208, 1009], [205, 1010], [210, 1010], [211, 1010], [204, 1011], [210, 1011], [211, 1011], [212, 1011], [203, 1012], [204, 1012], [211, 1012], [212, 1012]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E916-boundary-7.png", "bytes": 1553, "sha256": "a895124f280f7ae52d0be7033714d251af03fb7b8c75b5c682d54d8f7d316d95"}}
{"index": 22, "text": "L", "bbox_pdf_points": [80.0, 361.147, 86.11, 371.147], "bbox_pixels": [222.22222222222223, 1003.1861111111111, 239.19444444444446, 1030.963888888889], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 11.146999999999991}, "dark_pixels_outside_original_crop": 67, "dark_pixels_sample": [[225, 1004], [226, 1004], [227, 1004], [225, 1005], [226, 1005], [227, 1005], [225, 1006], [226, 1006], [227, 1006], [225, 1007], [226, 1007], [227, 1007]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E916-boundary-8.png", "bytes": 1403, "sha256": "65c97ed3b0e58c9d9a983f3df88e32e54f8df238402a951f2de16140e84760cc"}}
{"index": 23, "text": "e", "bbox_pdf_points": [86.11, 361.147, 90.55, 371.147], "bbox_pixels": [239.19444444444446, 1003.1861111111111, 251.52777777777777, 1030.963888888889], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 11.146999999999991}, "dark_pixels_outside_original_crop": 41, "dark_pixels_sample": [[245, 1009], [246, 1009], [242, 1010], [247, 1010], [248, 1010], [241, 1011], [247, 1011], [248, 1011], [249, 1011], [241, 1012], [248, 1012], [249, 1012]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E916-boundary-9.png", "bytes": 1599, "sha256": "2a4e35e635e5cb339da1a146f2c7664bc92e73fe22b35759cdf49d0c161fe01e"}}
{"index": 24, "text": "a", "bbox_pdf_points": [90.55, 361.147, 94.99, 371.147], "bbox_pixels": [251.52777777777777, 1003.1861111111111, 263.8611111111111, 1030.963888888889], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 11.146999999999991}, "dark_pixels_outside_original_crop": 42, "dark_pixels_sample": [[257, 1009], [254, 1010], [255, 1010], [259, 1010], [260, 1010], [253, 1011], [254, 1011], [259, 1011], [260, 1011], [253, 1012], [254, 1012], [260, 1012]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E916-boundary-10.png", "bytes": 1755, "sha256": "b00a6a074236f29e74faaa92c988e50397d4096d29787de1e8618344b8891139"}}
{"index": 25, "text": "d", "bbox_pdf_points": [94.99, 361.147, 99.99, 371.147], "bbox_pixels": [263.8611111111111, 1003.1861111111111, 277.75, 1030.963888888889], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 11.146999999999991}, "dark_pixels_outside_original_crop": 57, "dark_pixels_sample": [[274, 1003], [273, 1004], [274, 1004], [273, 1005], [274, 1005], [274, 1006], [274, 1007], [274, 1008], [270, 1009], [271, 1009], [274, 1009], [268, 1010]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E916-boundary-11.png", "bytes": 1884, "sha256": "6521fa7c5aa7739481e3f2be964495ee2c8d42be5a5ef8e8f536aaeedfce9906"}}
{"index": 26, "text": "e", "bbox_pdf_points": [99.99, 361.147, 104.42999999999999, 371.147], "bbox_pixels": [277.75, 1003.1861111111111, 290.0833333333333, 1030.963888888889], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 11.146999999999991}, "dark_pixels_outside_original_crop": 44, "dark_pixels_sample": [[284, 1009], [281, 1010], [285, 1010], [286, 1010], [287, 1010], [280, 1011], [286, 1011], [287, 1011], [280, 1012], [287, 1012], [288, 1012], [279, 1013]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E916-boundary-12.png", "bytes": 1742, "sha256": "a1503fd85e0c2dbff533fe446dfc42da19aea398ed5a2a32925c332e6afc9f20"}}
{"index": 27, "text": "r", "bbox_pdf_points": [104.42999999999999, 361.147, 107.75999999999999, 371.147], "bbox_pixels": [290.0833333333333, 1003.1861111111111, 299.33333333333326, 1030.963888888889], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 11.146999999999991}, "dark_pixels_outside_original_crop": 36, "dark_pixels_sample": [[297, 1009], [291, 1010], [292, 1010], [293, 1010], [296, 1010], [297, 1010], [298, 1010], [292, 1011], [293, 1011], [297, 1011], [298, 1011], [292, 1012]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E916-boundary-13.png", "bytes": 1284, "sha256": "3fae2dafeda3cc80b5827c8f9e5ddb1246ea586d8a13bfaceb6c1578b21cc2e2"}}
{"index": 28, "text": "E", "bbox_pdf_points": [110.25999999999999, 361.147, 116.36999999999999, 371.147], "bbox_pixels": [306.2777777777777, 1003.1861111111111, 323.24999999999994, 1030.963888888889], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 11.146999999999991}, "dark_pixels_outside_original_crop": 64, "dark_pixels_sample": [[309, 1004], [310, 1004], [311, 1004], [318, 1004], [319, 1004], [320, 1004], [310, 1005], [311, 1005], [320, 1005], [310, 1006], [311, 1006], [310, 1007]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E916-boundary-14.png", "bytes": 1430, "sha256": "8b0bf6179b119c460f61ad8ca82dcc9b98d2181c0efd03cf15d0314b8efa59cb"}}
{"index": 29, "text": "l", "bbox_pdf_points": [116.36999999999999, 361.147, 119.14999999999999, 371.147], "bbox_pixels": [323.24999999999994, 1003.1861111111111, 330.97222222222223, 1030.963888888889], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 11.146999999999991}, "dark_pixels_outside_original_crop": 40, "dark_pixels_sample": [[326, 1003], [327, 1003], [326, 1004], [327, 1004], [326, 1005], [327, 1005], [326, 1006], [327, 1006], [326, 1007], [327, 1007], [326, 1008], [327, 1008]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E916-boundary-15.png", "bytes": 1461, "sha256": "d69832d3bda3470aa3f1cecd00d1605a4a588a6bebfb7f134b295f7c095ff84b"}}
{"index": 30, "text": "e", "bbox_pdf_points": [119.14999999999999, 361.147, 123.58999999999999, 371.147], "bbox_pixels": [330.97222222222223, 1003.1861111111111, 343.3055555555555, 1030.963888888889], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 11.146999999999991}, "dark_pixels_outside_original_crop": 44, "dark_pixels_sample": [[337, 1009], [334, 1010], [338, 1010], [339, 1010], [340, 1010], [333, 1011], [339, 1011], [340, 1011], [333, 1012], [340, 1012], [341, 1012], [332, 1013]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E916-boundary-16.png", "bytes": 1736, "sha256": "6bed4d7ffb062c0b6028d5a4ff6152af9d9bd235539b8dcc67818034acaad2a3"}}
{"index": 31, "text": "p", "bbox_pdf_points": [123.58999999999999, 361.147, 128.58999999999997, 371.147], "bbox_pixels": [343.3055555555555, 1003.1861111111111, 357.1944444444444, 1030.963888888889], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 11.146999999999991}, "dark_pixels_outside_original_crop": 60, "dark_pixels_sample": [[351, 1009], [344, 1010], [345, 1010], [346, 1010], [349, 1010], [350, 1010], [351, 1010], [352, 1010], [353, 1010], [345, 1011], [346, 1011], [348, 1011]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E916-boundary-17.png", "bytes": 1870, "sha256": "2f036af0fb86e5cc0a0353259bb6d590e3c25ce9704eeb66c763c685ceb8db67"}}
{"index": 32, "text": "h", "bbox_pdf_points": [128.58999999999997, 361.147, 133.58999999999997, 371.147], "bbox_pixels": [357.1944444444444, 1003.1861111111111, 371.08333333333326, 1030.963888888889], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 11.146999999999991}, "dark_pixels_outside_original_crop": 72, "dark_pixels_sample": [[359, 1003], [360, 1003], [359, 1004], [360, 1004], [359, 1005], [360, 1005], [359, 1006], [360, 1006], [359, 1007], [360, 1007], [359, 1008], [360, 1008]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E916-boundary-18.png", "bytes": 1847, "sha256": "e827acf9c4d50dcb8029574ea1d8279d430aa4fda8e2da85e5131a1c2e0f4e09"}}
{"index": 33, "text": "a", "bbox_pdf_points": [133.58999999999997, 361.147, 138.02999999999997, 371.147], "bbox_pixels": [371.08333333333326, 1003.1861111111111, 383.4166666666666, 1030.963888888889], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 11.146999999999991}, "dark_pixels_outside_original_crop": 48, "dark_pixels_sample": [[376, 1009], [377, 1009], [374, 1010], [378, 1010], [379, 1010], [373, 1011], [374, 1011], [379, 1011], [380, 1011], [373, 1012], [374, 1012], [379, 1012]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E916-boundary-19.png", "bytes": 1603, "sha256": "259b1e81f79a08b8aaf89fd9e5e7cede0138735d6378fd6f3f7d7ad76dd853ba"}}
{"index": 34, "text": "n", "bbox_pdf_points": [138.02999999999997, 361.147, 143.02999999999997, 371.147], "bbox_pixels": [383.4166666666666, 1003.1861111111111, 397.3055555555555, 1030.963888888889], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 11.146999999999991}, "dark_pixels_outside_original_crop": 61, "dark_pixels_sample": [[391, 1009], [384, 1010], [385, 1010], [386, 1010], [387, 1010], [389, 1010], [390, 1010], [391, 1010], [392, 1010], [393, 1010], [385, 1011], [386, 1011]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E916-boundary-20.png", "bytes": 1671, "sha256": "53448772932e1398de195fcd5206e751b8247b9ade0e88e0d3ebe3ce3ce41df6"}}
{"index": 35, "text": "t", "bbox_pdf_points": [143.02999999999997, 361.147, 145.80999999999997, 371.147], "bbox_pixels": [397.3055555555555, 1003.1861111111111, 405.02777777777766, 1030.963888888889], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 11.146999999999991}, "dark_pixels_outside_original_crop": 33, "dark_pixels_sample": [[401, 1006], [401, 1007], [400, 1008], [401, 1008], [399, 1009], [400, 1009], [401, 1009], [399, 1010], [400, 1010], [401, 1010], [400, 1011], [401, 1011]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E916-boundary-21.png", "bytes": 1574, "sha256": "7a0fa29c4790e80256801cb41ca80e66ac6459f8569376bd6d7f896055ffcdec"}}
{"index": 36, "text": "s", "bbox_pdf_points": [145.81, 361.147, 149.7, 371.147], "bbox_pixels": [405.02777777777777, 1003.1861111111111, 415.83333333333326, 1030.963888888889], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 11.146999999999991}, "dark_pixels_outside_original_crop": 32, "dark_pixels_sample": [[409, 1009], [410, 1009], [407, 1010], [412, 1010], [413, 1010], [407, 1011], [413, 1011], [407, 1012], [413, 1012], [407, 1013], [408, 1013], [407, 1014]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E916-boundary-22.png", "bytes": 1538, "sha256": "89c907552fbe76d5f76bba7c46db89a101a925b2443f3d881def9ff3fecd47cc"}}
{"index": 37, "text": ".", "bbox_pdf_points": [149.7, 361.147, 152.2, 371.147], "bbox_pixels": [415.83333333333326, 1003.1861111111111, 422.7777777777777, 1030.963888888889], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 11.146999999999991}, "dark_pixels_outside_original_crop": 4, "dark_pixels_sample": [[418, 1020], [419, 1020], [418, 1021], [419, 1021]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E916-boundary-23.png", "bytes": 1213, "sha256": "5989536230f136701561773e9c8711849b74e2fd15dc94798aa222b3d4d31e68"}}

Wyłączenia: pełny rekord/klauzula/pozostały crop, artwork/ratingi, wcześniejsze pending, brakujące procedury, automatyczne semantyczneFP/FN/gold.

## E918

Dokładny zakres: oryginalny krótki cytat i jego prostokąt.

> Unless the rules specifically state otherwise, Elephant units may be commanded by any leader.

Niezależny dosłowny helper:

> Unless the rules specifically state otherwise, Elephant units
> may be commanded by any leader.

Helper `/regions/5/text`, znaki [1761, 1854], SHA-256 `8e9afe85ea858c3ad148eeac9957ab5c93636bd75d78522716691bb0fd323ebe`.

Strona33; bbox piksele [125, 1250, 825, 1335], PDFpt [45.0, 450.0, 297.0, 480.6]; wymiary [1700, 2200].

Rzeczywisty krótki cytat PDFpt [45.0, 455.45029999999997, 297.00199999999995, 477.45029999999997]; całe obwiednie NIE mieszczą się. Raster: readable_no_observed_ink_loss.

Ręczne porównanie: Cytat unless rules specifically stateotherwise/commandedbyanyleader widoczny. Końcowe s w units ma obwiednię+0.002pt. Raster czytelny w swoim krótkim zakresie, nie nadaje commandeligibility/range z brakujących procedur.

[Dokładny nieposzerzony crop](../../../measurement/M-POC5A-semantic-04c1/visual-02/E918-exact.png) · [Referencja do porównania granicy](../../../measurement/M-POC5A-semantic-04c1/visual-02/E918-quote-reference.png). Referencja nie naprawia lokatora.

**first-001:** `/evidence/17`, bajty [30600,31641), SHA-256 `247f0a0809fc752fb7438540bacdddbcc165528145469c23458618eeeba2879d`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/17/quote/value`; bajty [30928,31023), hash `652eac621dc4e628a6558d20ffcbe18e6c0d91aa05c2145ad967f5bcde08db2d`; wartość "Unless the rules specifically state otherwise, Elephant units may be commanded by any leader.".

Pole `/evidence/17/image/bbox`; bajty [31342,31414), hash `994347437484a7083ab49f2c2f796dc20daec73139fb96fdd8bfbc668ef29741`; wartość [125, 1250, 825, 1335].

Pole `/evidence/17/image/path`; bajty [31210,31238), hash `1c49839769a02a21298c8538d089fe44e0d18382b94e4d090a87a9fb965d9385`; wartość "inputs/v1/pages/pdf-33.png".

Pole `/evidence/17/image/sha256`; bajty [31258,31324), hash `c47d60a64b680805cd7eb4db56f02de372504566bd631f76f3ea50cd64e4fc1b`; wartość "ac53150f19a795383afe05e4fc668105b2b04d54fb9b2488e6557b12bd683983".

**context-01:** `/evidence/17`, bajty [66879,67949), SHA-256 `a6a15ea040fcdc6200c65ae7879386945025f5eccc14e33156f1c6ea1d377356`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/17/quote/value`; bajty [67217,67312), hash `652eac621dc4e628a6558d20ffcbe18e6c0d91aa05c2145ad967f5bcde08db2d`; wartość "Unless the rules specifically state otherwise, Elephant units may be commanded by any leader.".

Pole `/evidence/17/image/bbox`; bajty [67639,67716), hash `5b971656dffd6456d3c61e36da88b6bb68fefaa2a4271236759b3c387b412e33`; wartość [125, 1250, 825, 1335].

Pole `/evidence/17/image/path`; bajty [67505,67533), hash `1c49839769a02a21298c8538d089fe44e0d18382b94e4d090a87a9fb965d9385`; wartość "inputs/v1/pages/pdf-33.png".

Pole `/evidence/17/image/sha256`; bajty [67554,67620), hash `c47d60a64b680805cd7eb4db56f02de372504566bd631f76f3ea50cd64e4fc1b`; wartość "ac53150f19a795383afe05e4fc668105b2b04d54fb9b2488e6557b12bd683983".

Każdy naruszony glif:

{"index": 53, "text": "s", "bbox_pdf_points": [293.11199999999997, 455.45029999999997, 297.00199999999995, 465.45029999999997], "bbox_pixels": [814.1999999999999, 1265.1397222222222, 825.0055555555554, 1292.9174999999998], "overflow_pdf_points": {"left": 0, "right": 0.0019999999999527063, "top": 0, "bottom": 0}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E918-boundary-0.png", "bytes": 1477, "sha256": "85feff951cea8584d9de3d207ab6dfa79a4376a3862ab9a2cd6c032796cda981"}}

Wyłączenia: pełny rekord/klauzula/pozostały crop, artwork/ratingi, wcześniejsze pending, brakujące procedury, automatyczne semantyczneFP/FN/gold.

## E919

Dokładny zakres: oryginalny krótki cytat i jego prostokąt.

> African Elephants incur a +1 DRM to their Pre-Shock die rolls (8.43).

Niezależny dosłowny helper:

> African Elephants incur a +1 DRM to their Pre-Shock die rolls
> (8.43).

Helper `/regions/5/text`, znaki [2050, 2119], SHA-256 `87f1807d2619a6e2be2feef7600cef3a8de1fd1c12f2e1cf12c7c7422df03da7`.

Strona33; bbox piksele [125, 1340, 825, 1510], PDFpt [45.0, 482.4, 297.0, 543.6]; wymiary [1700, 2200].

Rzeczywisty krótki cytat PDFpt [45.0, 520.8503, 297.00199999999984, 542.8503]; całe obwiednie NIE mieszczą się. Raster: readable_no_observed_ink_loss.

Ręczne porównanie: Cytat AfricanElephants+1DRMPre-Shock8.43 widoczny. s w rolls obwiednią+0.002pt przy prawej krawędzi; nie ma widocznej utraty tuszu. Akceptacja czytelności nie obejmuje całego dodatku doClash/Superiority ani źródła8.43.

[Dokładny nieposzerzony crop](../../../measurement/M-POC5A-semantic-04c1/visual-02/E919-exact.png) · [Referencja do porównania granicy](../../../measurement/M-POC5A-semantic-04c1/visual-02/E919-quote-reference.png). Referencja nie naprawia lokatora.

**first-001:** `/evidence/18`, bajty [31647,32664), SHA-256 `ff3740315de1ca850a2155f6e8641b39391bba0fcf15d58f93addb20f05eef0e`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/18/quote/value`; bajty [31975,32046), hash `111b72ea2054a4db8fb1c218a62c721ce1acb91a05d4e6e2359bb0278a5ed3cf`; wartość "African Elephants incur a +1 DRM to their Pre-Shock die rolls (8.43).".

Pole `/evidence/18/image/bbox`; bajty [32365,32437), hash `25ee7b7421ff902c07d51ccfc8c5fb27a8d5c0ba27116d86dae52783fe502812`; wartość [125, 1340, 825, 1510].

Pole `/evidence/18/image/path`; bajty [32233,32261), hash `1c49839769a02a21298c8538d089fe44e0d18382b94e4d090a87a9fb965d9385`; wartość "inputs/v1/pages/pdf-33.png".

Pole `/evidence/18/image/sha256`; bajty [32281,32347), hash `c47d60a64b680805cd7eb4db56f02de372504566bd631f76f3ea50cd64e4fc1b`; wartość "ac53150f19a795383afe05e4fc668105b2b04d54fb9b2488e6557b12bd683983".

**context-01:** `/evidence/18`, bajty [67956,69002), SHA-256 `c5a4050e199eddff384835dd7ec74a6282f220a510e82f0726cb94329198a2c2`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/18/quote/value`; bajty [68294,68365), hash `111b72ea2054a4db8fb1c218a62c721ce1acb91a05d4e6e2359bb0278a5ed3cf`; wartość "African Elephants incur a +1 DRM to their Pre-Shock die rolls (8.43).".

Pole `/evidence/18/image/bbox`; bajty [68692,68769), hash `f61fd9b872e54d7b6023f7ad11ffa65a04dca1e34fb1da562161810ec474efe0`; wartość [125, 1340, 825, 1510].

Pole `/evidence/18/image/path`; bajty [68558,68586), hash `1c49839769a02a21298c8538d089fe44e0d18382b94e4d090a87a9fb965d9385`; wartość "inputs/v1/pages/pdf-33.png".

Pole `/evidence/18/image/sha256`; bajty [68607,68673), hash `c47d60a64b680805cd7eb4db56f02de372504566bd631f76f3ea50cd64e4fc1b`; wartość "ac53150f19a795383afe05e4fc668105b2b04d54fb9b2488e6557b12bd683983".

Każdy naruszony glif:

{"index": 50, "text": "s", "bbox_pdf_points": [293.11199999999985, 520.8503, 297.00199999999984, 530.8503], "bbox_pixels": [814.1999999999996, 1446.8063888888887, 825.0055555555551, 1474.5841666666665], "overflow_pdf_points": {"left": 0, "right": 0.0019999999998390194, "top": 0, "bottom": 0}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E919-boundary-0.png", "bytes": 1423, "sha256": "c10e9245677884db1d32c1b7283a1f98606043dc9b51faed592d1bc64257bdef"}}

Wyłączenia: pełny rekord/klauzula/pozostały crop, artwork/ratingi, wcześniejsze pending, brakujące procedury, automatyczne semantyczneFP/FN/gold.

## E921

Dokładny zakres: oryginalny krótki cytat i jego prostokąt.

> Skirmishers may Orderly Withdraw up to 2 hexes before any units whose MA is the same or less

Niezależny dosłowny helper:

> Skirmishers may Orderly
> Withdraw up to 2 hexes before any units whose MA
> is the same or less

Helper `/regions/6/text`, znaki [773, 865], SHA-256 `a7d57ea34d26f06d9b35f032e53c2e559d19471c0cccf414c0d0aeb168eb8f8a`.

Strona33; bbox piksele [875, 650, 1575, 895], PDFpt [315.0, 234.0, 567.0, 322.2]; wymiary [1700, 2200].

Rzeczywisty krótki cytat PDFpt [360.4946, 235.9403000000001, 567.5826, 269.9403000000001]; całe obwiednie NIE mieszczą się. Raster: readable_no_observed_ink_loss.

Ręczne porównanie: Widoczne SkirmishersOWup to2hexesbeforeunits same/lowerMA. Krótki cytat jest oryginalnie fragmentem zdania, nie obejmuje jego całej końcówki i wyjątków. Obwiednie y zOrderly i A zMA wystają prawą krawędzią0.0136pt/0.5826pt; raster czytelny bez zaobserwowanej utraty tuszu. Nie dodaje brakującej końcówki do cytatu.

[Dokładny nieposzerzony crop](../../../measurement/M-POC5A-semantic-04c1/visual-02/E921-exact.png) · [Referencja do porównania granicy](../../../measurement/M-POC5A-semantic-04c1/visual-02/E921-quote-reference.png). Referencja nie naprawia lokatora.

**first-001:** `/evidence/20`, bajty [33738,34779), SHA-256 `69b88be4106897c5e0a1b372f8e81e53c4c9ca9a7f63ce075ca34e7a887f3b09`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/20/quote/value`; bajty [34068,34162), hash `893ab7434f6c5a640d1d824fe279150795259d67e5aca90b9bbf2c8e2daf08a8`; wartość "Skirmishers may Orderly Withdraw up to 2 hexes before any units whose MA is the same or less".

Pole `/evidence/20/image/bbox`; bajty [34481,34552), hash `2e060a963b4bb3ac99012ff5d27af6e6b53d9104966810c346384604f3e180ef`; wartość [875, 650, 1575, 895].

Pole `/evidence/20/image/path`; bajty [34349,34377), hash `1c49839769a02a21298c8538d089fe44e0d18382b94e4d090a87a9fb965d9385`; wartość "inputs/v1/pages/pdf-33.png".

Pole `/evidence/20/image/sha256`; bajty [34397,34463), hash `c47d60a64b680805cd7eb4db56f02de372504566bd631f76f3ea50cd64e4fc1b`; wartość "ac53150f19a795383afe05e4fc668105b2b04d54fb9b2488e6557b12bd683983".

**context-01:** `/evidence/20`, bajty [70107,71177), SHA-256 `d5a6f1d33d43bfea4b0bda62abd87748b3fbc51f13601abf6b21c16c0207244a`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/20/quote/value`; bajty [70447,70541), hash `893ab7434f6c5a640d1d824fe279150795259d67e5aca90b9bbf2c8e2daf08a8`; wartość "Skirmishers may Orderly Withdraw up to 2 hexes before any units whose MA is the same or less".

Pole `/evidence/20/image/bbox`; bajty [70868,70944), hash `9547948c8a6df5d7307c00236e35a83f6ae130d9f9d4f3d6b0edf5aef5db5c69`; wartość [875, 650, 1575, 895].

Pole `/evidence/20/image/path`; bajty [70734,70762), hash `1c49839769a02a21298c8538d089fe44e0d18382b94e4d090a87a9fb965d9385`; wartość "inputs/v1/pages/pdf-33.png".

Pole `/evidence/20/image/sha256`; bajty [70783,70849), hash `c47d60a64b680805cd7eb4db56f02de372504566bd631f76f3ea50cd64e4fc1b`; wartość "ac53150f19a795383afe05e4fc668105b2b04d54fb9b2488e6557b12bd683983".

Każdy naruszony glif:

{"index": 20, "text": "y", "bbox_pdf_points": [562.0136, 235.9403000000001, 567.0136, 245.9403000000001], "bbox_pixels": [1561.148888888889, 655.3897222222225, 1575.0377777777778, 683.1675000000001], "overflow_pdf_points": {"left": 0, "right": 0.013599999999996726, "top": 0, "bottom": 0}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E921-boundary-0.png", "bytes": 1615, "sha256": "76f6f290a242140c22fbd0ccae23ab99e6b9efd3d04f5aaa6a4eea97687ba379"}}
{"index": 59, "text": "A", "bbox_pdf_points": [560.3625999999999, 247.9403000000001, 567.5826, 257.9403000000001], "bbox_pixels": [1556.5627777777777, 688.7230555555558, 1576.618333333333, 716.5008333333335], "overflow_pdf_points": {"left": 0, "right": 0.5825999999999567, "top": 0, "bottom": 0}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E921-boundary-1.png", "bytes": 1719, "sha256": "3c2cd5dfeddfd60ab436e13b3ebd36d8ca34d37c4fc63563e2ba317f491cf258"}}

Wyłączenia: pełny rekord/klauzula/pozostały crop, artwork/ratingi, wcześniejsze pending, brakujące procedury, automatyczne semantyczneFP/FN/gold.

## E922

Dokładny zakres: oryginalny krótki cytat i jego prostokąt.

> There is a +2 DRM to the Missile Fire DR whenever a Skirmisher unit is the target.

Niezależny dosłowny helper:

> There is a +2 DRM to the Missile Fire DR
> whenever a Skirmisher unit is the target.

Helper `/regions/6/text`, znaki [1153, 1235], SHA-256 `c0e2820da8cbb08c311bd4f4d8fd6bad76dd72dce7b7ef6b5f38a43588dfe5f9`.

Strona33; bbox piksele [875, 900, 1575, 1055], PDFpt [315.0, 324.0, 567.0, 379.8]; wymiary [1700, 2200].

Rzeczywisty krótki cytat PDFpt [314.9946, 325.3403, 566.9935999999998, 347.3403]; całe obwiednie NIE mieszczą się. Raster: readable_no_observed_ink_loss.

Ręczne porównanie: Cytat+2doMissileFireDRwhenSKtarget widoczny. Pierwsze w w whenever wystaje lewą obwiednią0.0054pt. Raster czytelny; nie przyjmuje innych zakazówH&Dw tej klauzuli ani całego wyniku strzału.

[Dokładny nieposzerzony crop](../../../measurement/M-POC5A-semantic-04c1/visual-02/E922-exact.png) · [Referencja do porównania granicy](../../../measurement/M-POC5A-semantic-04c1/visual-02/E922-quote-reference.png). Referencja nie naprawia lokatora.

**first-001:** `/evidence/21`, bajty [34785,35816), SHA-256 `d624e3ec481991ed9df42052e4fa235dfced797e11ea852ff877c4725d6194f6`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/21/quote/value`; bajty [35114,35198), hash `fd8c105ec531e9b60c11527e9392aa6fa3b1fc178c33bcc7f0028f2254485464`; wartość "There is a +2 DRM to the Missile Fire DR whenever a Skirmisher unit is the target.".

Pole `/evidence/21/image/bbox`; bajty [35517,35589), hash `7ea3d219fb07fcaeeaa68d4b98a7523633a27bd30a16ff0811090d6f9f98cf09`; wartość [875, 900, 1575, 1055].

Pole `/evidence/21/image/path`; bajty [35385,35413), hash `1c49839769a02a21298c8538d089fe44e0d18382b94e4d090a87a9fb965d9385`; wartość "inputs/v1/pages/pdf-33.png".

Pole `/evidence/21/image/sha256`; bajty [35433,35499), hash `c47d60a64b680805cd7eb4db56f02de372504566bd631f76f3ea50cd64e4fc1b`; wartość "ac53150f19a795383afe05e4fc668105b2b04d54fb9b2488e6557b12bd683983".

**context-01:** `/evidence/21`, bajty [71184,72244), SHA-256 `381c2ddd0f2e23f0c9ac058164612a10ff1362046576a0eaca600629a00e13dc`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/21/quote/value`; bajty [71523,71607), hash `fd8c105ec531e9b60c11527e9392aa6fa3b1fc178c33bcc7f0028f2254485464`; wartość "There is a +2 DRM to the Missile Fire DR whenever a Skirmisher unit is the target.".

Pole `/evidence/21/image/bbox`; bajty [71934,72011), hash `689d0ba091298607bb65bcf7acb99ce433f1b0282c901475e9073072a46221e0`; wartość [875, 900, 1575, 1055].

Pole `/evidence/21/image/path`; bajty [71800,71828), hash `1c49839769a02a21298c8538d089fe44e0d18382b94e4d090a87a9fb965d9385`; wartość "inputs/v1/pages/pdf-33.png".

Pole `/evidence/21/image/sha256`; bajty [71849,71915), hash `c47d60a64b680805cd7eb4db56f02de372504566bd631f76f3ea50cd64e4fc1b`; wartość "ac53150f19a795383afe05e4fc668105b2b04d54fb9b2488e6557b12bd683983".

Każdy naruszony glif:

{"index": 31, "text": "w", "bbox_pdf_points": [314.9946, 337.3403, 322.2146, 347.3403], "bbox_pixels": [874.9849999999999, 937.0563888888889, 895.0405555555557, 964.8341666666668], "overflow_pdf_points": {"left": 0.005400000000008731, "right": 0, "top": 0, "bottom": 0}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E922-boundary-0.png", "bytes": 1830, "sha256": "9d4ce5794cc08624720b5c63bcff1588bb850cd72927b2e60d8036ebd444cff6"}}

Wyłączenia: pełny rekord/klauzula/pozostały crop, artwork/ratingi, wcześniejsze pending, brakujące procedury, automatyczne semantyczneFP/FN/gold.

## E923

Dokładny zakres: oryginalny krótki cytat i jego prostokąt.

> Any Cohesion Hits inflicted by Skirmishers in Shock Combat are halved (round down) with a maximum of 1 Cohesion Hit.

Niezależny dosłowny helper:

> Any Cohesion Hits inflicted by Skirmishers in Shock Combat
> are halved (round down) with a maximum of 1 Cohesion Hit.

Helper `/regions/6/text`, znaki [1810, 1926], SHA-256 `da46ed888704e64957e80df0ad64b12d0e074dde86e3e6f17fdfd9a7b1b6557a`.

Strona33; bbox piksele [875, 1060, 1575, 1645], PDFpt [315.0, 381.6, 567.0, 592.2]; wymiary [1700, 2200].

Rzeczywisty krótki cytat PDFpt [323.9946, 493.9403, 567.0096000000001, 515.9403]; całe obwiednie NIE mieszczą się. Raster: readable_no_observed_ink_loss.

Ręczne porównanie: Pełny krótki cytat half/floor/max1Hits inflictedbySKw dwóch liniach widoczny. Końcowa kropka obwiednią+0.0096pt; raster bez widocznej utraty. To sprawdzenie cytatu, nie rozstrzygnięcie wcześniejszej semantyki mixeddefense/SEM-004.

[Dokładny nieposzerzony crop](../../../measurement/M-POC5A-semantic-04c1/visual-02/E923-exact.png) · [Referencja do porównania granicy](../../../measurement/M-POC5A-semantic-04c1/visual-02/E923-quote-reference.png). Referencja nie naprawia lokatora.

**first-001:** `/evidence/22`, bajty [35822,36888), SHA-256 `d8335119f9800b06329ad9fdba737b50bb9a4dc77dc158dbd45e15d2c5b0d601`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/22/quote/value`; bajty [36151,36269), hash `c28840acb4f4ec0ee2b98d4a1b2d661825d3b1b6774b573a44941145f71b48d9`; wartość "Any Cohesion Hits inflicted by Skirmishers in Shock Combat are halved (round down) with a maximum of 1 Cohesion Hit.".

Pole `/evidence/22/image/bbox`; bajty [36588,36661), hash `9ecd15ee2e34c3fd92ebb5d21481e9dfbab29f0a54c3f360aa518d73797ef2ce`; wartość [875, 1060, 1575, 1645].

Pole `/evidence/22/image/path`; bajty [36456,36484), hash `1c49839769a02a21298c8538d089fe44e0d18382b94e4d090a87a9fb965d9385`; wartość "inputs/v1/pages/pdf-33.png".

Pole `/evidence/22/image/sha256`; bajty [36504,36570), hash `c47d60a64b680805cd7eb4db56f02de372504566bd631f76f3ea50cd64e4fc1b`; wartość "ac53150f19a795383afe05e4fc668105b2b04d54fb9b2488e6557b12bd683983".

**context-01:** `/evidence/22`, bajty [72251,73346), SHA-256 `11c290e2bba967856a8a11727d478685a6c1a5ec300691feca74a8456a8ad6ae`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/22/quote/value`; bajty [72590,72708), hash `c28840acb4f4ec0ee2b98d4a1b2d661825d3b1b6774b573a44941145f71b48d9`; wartość "Any Cohesion Hits inflicted by Skirmishers in Shock Combat are halved (round down) with a maximum of 1 Cohesion Hit.".

Pole `/evidence/22/image/bbox`; bajty [73035,73113), hash `f6351a1b6f65e7bce07e0d3adf86c2e4852ac8658fa19575e6b0ae7d7ef8d541`; wartość [875, 1060, 1575, 1645].

Pole `/evidence/22/image/path`; bajty [72901,72929), hash `1c49839769a02a21298c8538d089fe44e0d18382b94e4d090a87a9fb965d9385`; wartość "inputs/v1/pages/pdf-33.png".

Pole `/evidence/22/image/sha256`; bajty [72950,73016), hash `c47d60a64b680805cd7eb4db56f02de372504566bd631f76f3ea50cd64e4fc1b`; wartość "ac53150f19a795383afe05e4fc668105b2b04d54fb9b2488e6557b12bd683983".

Każdy naruszony glif:

{"index": 96, "text": ".", "bbox_pdf_points": [564.5096000000001, 505.9403, 567.0096000000001, 515.9403], "bbox_pixels": [1568.0822222222225, 1405.3897222222222, 1575.0266666666669, 1433.1674999999998], "overflow_pdf_points": {"left": 0, "right": 0.009600000000091313, "top": 0, "bottom": 0}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E923-boundary-0.png", "bytes": 1010, "sha256": "8305f7623c2bed1f7f6b55d7c4f7e44940238211a36ac3fa10058452a4c60fa8"}}

Wyłączenia: pełny rekord/klauzula/pozostały crop, artwork/ratingi, wcześniejsze pending, brakujące procedury, automatyczne semantyczneFP/FN/gold.

## E923ex

Dokładny zakres: oryginalny krótki cytat i jego prostokąt.

> of 1(4), the actual result would be 0(4).

Niezależny dosłowny helper:

> of 1(4), the actual result would be 0(4).

Helper `/regions/6/text`, znaki [2389, 2430], SHA-256 `dfcc0ca93b28c886eded93161b823bfdb9f99787ce9f0da0b048fda0b961b02e`.

Strona33; bbox piksele [875, 1650, 1575, 1755], PDFpt [315.0, 594.0, 567.0, 631.8]; wymiary [1700, 2200].

Rzeczywisty krótki cytat PDFpt [314.9946, 620.6003, 472.10560000000004, 630.6003]; całe obwiednie NIE mieszczą się. Raster: readable_no_observed_ink_loss.

Ręczne porównanie: Cytowany fragment przykładu1(4)→0(4) widoczny, liczby/nawiasy zachowane. Pierwsze o w of wystaje lewą obwiednią0.0054pt, bez zaobserwowanej utraty tuszu. Oryginalny fragment nie jest całą interpretacją przykładu/walki.

[Dokładny nieposzerzony crop](../../../measurement/M-POC5A-semantic-04c1/visual-02/E923ex-exact.png) · [Referencja do porównania granicy](../../../measurement/M-POC5A-semantic-04c1/visual-02/E923ex-quote-reference.png). Referencja nie naprawia lokatora.

**first-001:** `/evidence/23`, bajty [36894,37887), SHA-256 `bae65a04aeed14d64064722998de6f25cd4ec9fb336098bb040c3f3e0924d22b`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/23/quote/value`; bajty [37225,37268), hash `9a6d1800b55a28f9f5fd44923ccba086f4cdef904182aef2791a9325a64288e1`; wartość "of 1(4), the actual result would be 0(4).".

Pole `/evidence/23/image/bbox`; bajty [37587,37660), hash `aaa828291eb78761dd0110ddd263d101a50645d737f2d6a85bbe86a1ce62c5b4`; wartość [875, 1650, 1575, 1755].

Pole `/evidence/23/image/path`; bajty [37455,37483), hash `1c49839769a02a21298c8538d089fe44e0d18382b94e4d090a87a9fb965d9385`; wartość "inputs/v1/pages/pdf-33.png".

Pole `/evidence/23/image/sha256`; bajty [37503,37569), hash `c47d60a64b680805cd7eb4db56f02de372504566bd631f76f3ea50cd64e4fc1b`; wartość "ac53150f19a795383afe05e4fc668105b2b04d54fb9b2488e6557b12bd683983".

**context-01:** `/evidence/23`, bajty [73353,74375), SHA-256 `adfaf1e41d822511ff93deb4398f6d0c6c6aa315d6184d8973c35ac7a0f6fa70`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/23/quote/value`; bajty [73694,73737), hash `9a6d1800b55a28f9f5fd44923ccba086f4cdef904182aef2791a9325a64288e1`; wartość "of 1(4), the actual result would be 0(4).".

Pole `/evidence/23/image/bbox`; bajty [74064,74142), hash `d307bed0bfdd12af252e4b85223153eeb5bb943ddfc1b7b7a3297ea98dcb6ed0`; wartość [875, 1650, 1575, 1755].

Pole `/evidence/23/image/path`; bajty [73930,73958), hash `1c49839769a02a21298c8538d089fe44e0d18382b94e4d090a87a9fb965d9385`; wartość "inputs/v1/pages/pdf-33.png".

Pole `/evidence/23/image/sha256`; bajty [73979,74045), hash `c47d60a64b680805cd7eb4db56f02de372504566bd631f76f3ea50cd64e4fc1b`; wartość "ac53150f19a795383afe05e4fc668105b2b04d54fb9b2488e6557b12bd683983".

Każdy naruszony glif:

{"index": 0, "text": "o", "bbox_pdf_points": [314.9946, 620.6003, 319.9946, 630.6003], "bbox_pixels": [874.9849999999999, 1723.8897222222222, 888.8738888888888, 1751.6674999999998], "overflow_pdf_points": {"left": 0.005400000000008731, "right": 0, "top": 0, "bottom": 0}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E923ex-boundary-0.png", "bytes": 1714, "sha256": "967516dfde8f70ef84ecb98db11216e4a71099636cc428954c1b5c6c7f33f057"}}

Wyłączenia: pełny rekord/klauzula/pozostały crop, artwork/ratingi, wcześniejsze pending, brakujące procedury, automatyczne semantyczneFP/FN/gold.

## E92

Dokładny zakres: oryginalny krótki cytat i jego prostokąt.

> 9.2 SKIRMISHERS, VELITES, AND LIGHT INFANTRY

Niezależny dosłowny helper:

> 9.2 SKIRMISHERS, VELITES, AND LIGHT
> INFANTRY

Helper `/regions/6/text`, znaki [0, 44], SHA-256 `1b2dc0eb484dc8ce2c97a46aa98dcc183b90b21a1d99a6ae688e5d8a69cf951b`.

Strona33; bbox piksele [875, 125, 1575, 215], PDFpt [315.0, 45.0, 567.0, 77.4]; wymiary [1700, 2200].

Rzeczywisty krótki cytat PDFpt [315.0, 53.81099999999992, 549.1776, 80.2109999999999]; całe obwiednie NIE mieszczą się. Raster: readable_no_observed_ink_loss.

Ręczne porównanie: Nagłówek SKIRMISHERS/VELITES/ANDLIGHTINFANTRY rozłożony na dwie linie widoczny. Druga linia obwiednią przekracza dół2.811pt; tusz liter pozostaje wewnątrz granicy. Powiększenie narożnikaIczytelne. To nazwa sekcji, bez nowej oceny reguły.

[Dokładny nieposzerzony crop](../../../measurement/M-POC5A-semantic-04c1/visual-02/E92-exact.png) · [Referencja do porównania granicy](../../../measurement/M-POC5A-semantic-04c1/visual-02/E92-quote-reference.png). Referencja nie naprawia lokatora.

**first-001:** `/evidence/72`, bajty [86675,87666), SHA-256 `c2c4b6a156197fdfb78c9a17aeb5af17c2ec120d2bde854148dd8d49cccd4051`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/72/quote/value`; bajty [87003,87049), hash `e700335b180a7a96e60701ea1c29bbed77572ce6e90337d19378a8dd156204ca`; wartość "9.2 SKIRMISHERS, VELITES, AND LIGHT INFANTRY".

Pole `/evidence/72/image/bbox`; bajty [87368,87439), hash `cf35609c01efa7a95e03e07469b32744b66b77cf9a38fad2e6d592aea9d89b9e`; wartość [875, 125, 1575, 215].

Pole `/evidence/72/image/path`; bajty [87236,87264), hash `1c49839769a02a21298c8538d089fe44e0d18382b94e4d090a87a9fb965d9385`; wartość "inputs/v1/pages/pdf-33.png".

Pole `/evidence/72/image/sha256`; bajty [87284,87350), hash `c47d60a64b680805cd7eb4db56f02de372504566bd631f76f3ea50cd64e4fc1b`; wartość "ac53150f19a795383afe05e4fc668105b2b04d54fb9b2488e6557b12bd683983".

**context-01:** `/evidence/72`, bajty [124604,125624), SHA-256 `e0cdc4eeb06a90aacff63e2a5512a672ed3a1146e77fdf98da04cf0aaad18aef`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/72/quote/value`; bajty [124942,124988), hash `e700335b180a7a96e60701ea1c29bbed77572ce6e90337d19378a8dd156204ca`; wartość "9.2 SKIRMISHERS, VELITES, AND LIGHT INFANTRY".

Pole `/evidence/72/image/bbox`; bajty [125315,125391), hash `f9669280edb2def5f67692e91580024bf4145c772b8e5cb4fb4a564c94f2d2d3`; wartość [875, 125, 1575, 215].

Pole `/evidence/72/image/path`; bajty [125181,125209), hash `1c49839769a02a21298c8538d089fe44e0d18382b94e4d090a87a9fb965d9385`; wartość "inputs/v1/pages/pdf-33.png".

Pole `/evidence/72/image/sha256`; bajty [125230,125296), hash `c47d60a64b680805cd7eb4db56f02de372504566bd631f76f3ea50cd64e4fc1b`; wartość "ac53150f19a795383afe05e4fc668105b2b04d54fb9b2488e6557b12bd683983".

Każdy naruszony glif:

{"index": 31, "text": "I", "bbox_pdf_points": [315.0, 68.2109999999999, 319.668, 80.2109999999999], "bbox_pixels": [875.0, 189.4749999999997, 887.9666666666666, 222.80833333333305], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.8109999999998934}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E92-boundary-0.png", "bytes": 1133, "sha256": "831c28a0ad09ac54d6869d47e882a17cae82a198dc8210ae1eac41fd24606b8d"}}
{"index": 32, "text": "N", "bbox_pdf_points": [319.668, 68.2109999999999, 328.332, 80.2109999999999], "bbox_pixels": [887.9666666666666, 189.4749999999997, 912.0333333333334, 222.80833333333305], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.8109999999998934}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E92-boundary-1.png", "bytes": 1979, "sha256": "8f12a8e1c9e9657422ffe273bbadbc2797edcc1fced44484ac6931c9a9e9bd08"}}
{"index": 33, "text": "F", "bbox_pdf_points": [328.332, 68.2109999999999, 335.664, 80.2109999999999], "bbox_pixels": [912.0333333333334, 189.4749999999997, 932.3999999999999, 222.80833333333305], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.8109999999998934}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E92-boundary-2.png", "bytes": 1955, "sha256": "aa01c441bcfc37ac029a59f6d1710e815e30e09ebfc5a46e63c68b1220531a82"}}
{"index": 34, "text": "A", "bbox_pdf_points": [334.776, 68.2109999999999, 343.44, 80.2109999999999], "bbox_pixels": [929.9333333333334, 189.4749999999997, 954.0, 222.80833333333305], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.8109999999998934}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E92-boundary-3.png", "bytes": 2285, "sha256": "46b8379cac4e002e79db3b183423a8b3bc38c2d87369e3e1389e9b545fffb30e"}}
{"index": 35, "text": "N", "bbox_pdf_points": [343.44, 68.2109999999999, 352.104, 80.2109999999999], "bbox_pixels": [954.0, 189.4749999999997, 978.0666666666666, 222.80833333333305], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.8109999999998934}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E92-boundary-4.png", "bytes": 2121, "sha256": "b47befb6223216ef4968bff2dde4a66ab167c861ece036a96026bf3c5f94d052"}}
{"index": 36, "text": "T", "bbox_pdf_points": [352.104, 68.2109999999999, 360.108, 80.2109999999999], "bbox_pixels": [978.0666666666666, 189.4749999999997, 1000.3, 222.80833333333305], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.8109999999998934}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E92-boundary-5.png", "bytes": 1608, "sha256": "365def510366452530edd87845b55f2d6f017ec55ed8b5932e00d26fb31285c9"}}
{"index": 37, "text": "R", "bbox_pdf_points": [360.108, 68.2109999999999, 368.772, 80.2109999999999], "bbox_pixels": [1000.3, 189.4749999999997, 1024.3666666666668, 222.80833333333305], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.8109999999998934}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E92-boundary-6.png", "bytes": 2185, "sha256": "47aaaf84473679edf05a23694735fae14a983d9295b21ac02bd5a1bb62be3d7a"}}
{"index": 38, "text": "Y", "bbox_pdf_points": [368.3556, 68.2109999999999, 377.01959999999997, 80.2109999999999], "bbox_pixels": [1023.21, 189.4749999999997, 1047.2766666666666, 222.80833333333305], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.8109999999998934}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E92-boundary-7.png", "bytes": 2116, "sha256": "08c49400b84e9ab47941e9b7bee8bd159cc0c6dd1dcf445fc66af1257e62e822"}}

Wyłączenia: pełny rekord/klauzula/pozostały crop, artwork/ratingi, wcześniejsze pending, brakujące procedury, automatyczne semantyczneFP/FN/gold.

## E871

Dokładny zakres: oryginalny krótki cytat i jego prostokąt.

> This table is used to determine the strength of a missile unit firing at a given range.

Niezależny dosłowny helper:

> This table is used
> to determine the strength of a missile unit firing at a given range.

Helper `/regions/1/text`, znaki [64, 151], SHA-256 `4e82be9577fae08db5b6ff20f770c5e0935302f5708d2de148438b8240b6c7c2`.

Strona31; bbox piksele [875, 190, 1575, 255], PDFpt [315.0, 68.4, 567.0, 91.8]; wymiary [1700, 2200].

Rzeczywisty krótki cytat PDFpt [315.0, 69.197, 567.0029999999999, 91.197]; całe obwiednie NIE mieszczą się. Raster: readable_no_observed_ink_loss.

Ręczne porównanie: Cytat o sile missileunit przy zadanymrange widoczny. Końcowa kropka prawej obwiedni+0.003pt. Raster czytelny; opis tabeli nie staje się actualMRRCrow/headers/values.

[Dokładny nieposzerzony crop](../../../measurement/M-POC5A-semantic-04c1/visual-02/E871-exact.png) · [Referencja do porównania granicy](../../../measurement/M-POC5A-semantic-04c1/visual-02/E871-quote-reference.png). Referencja nie naprawia lokatora.

**first-001:** `/evidence/97`, bajty [111614,112661), SHA-256 `779e3238caa9a07a132d3ac7b5fc2400ae4db4b96e5b7eafcd8e21052b4a9a80`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/97/quote/value`; bajty [111955,112044), hash `bdd45b876353cce64d90b3e5b27374b79cd06857af0633821b21277f1f90ac63`; wartość "This table is used to determine the strength of a missile unit firing at a given range.".

Pole `/evidence/97/image/bbox`; bajty [112363,112434), hash `505e58be2fb72f6267e5eac333af682ebee912c7483d518658867a14841cd52b`; wartość [875, 190, 1575, 255].

Pole `/evidence/97/image/path`; bajty [112231,112259), hash `1909a421ea87dce812086a96fcaf7ec4f2e7380b02b0a77eefc6ba8f0b8cf997`; wartość "inputs/v1/pages/pdf-31.png".

Pole `/evidence/97/image/sha256`; bajty [112279,112345), hash `f80ec790ece408b391067b57927588a3c9963331e236524997b9d50e8f6e053e`; wartość "9edf269af78629a8bbfd809c75695e6353f7614d82d217d48ea2ecca0fd06712".

**context-01:** `/evidence/97`, bajty [150293,151369), SHA-256 `94bd9c7b5a8770e98472c97e90ebca2f39046074abf1b85e6358724734a95e91`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/97/quote/value`; bajty [150644,150733), hash `bdd45b876353cce64d90b3e5b27374b79cd06857af0633821b21277f1f90ac63`; wartość "This table is used to determine the strength of a missile unit firing at a given range.".

Pole `/evidence/97/image/bbox`; bajty [151060,151136), hash `3f79d7e72037adee4921d75659c3a3fcfd5399cbd6961798e8c46593fbf88a99`; wartość [875, 190, 1575, 255].

Pole `/evidence/97/image/path`; bajty [150926,150954), hash `1909a421ea87dce812086a96fcaf7ec4f2e7380b02b0a77eefc6ba8f0b8cf997`; wartość "inputs/v1/pages/pdf-31.png".

Pole `/evidence/97/image/sha256`; bajty [150975,151041), hash `f80ec790ece408b391067b57927588a3c9963331e236524997b9d50e8f6e053e`; wartość "9edf269af78629a8bbfd809c75695e6353f7614d82d217d48ea2ecca0fd06712".

Każdy naruszony glif:

{"index": 70, "text": ".", "bbox_pdf_points": [564.5029999999999, 81.197, 567.0029999999999, 91.197], "bbox_pixels": [1568.0638888888886, 225.54722222222222, 1575.0083333333332, 253.325], "overflow_pdf_points": {"left": 0, "right": 0.0029999999999290594, "top": 0, "bottom": 0}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E871-boundary-0.png", "bytes": 1072, "sha256": "7d9ba72609d2c301aafe756460320146c0b27b4f4c33e1a0789c2349a81e4992"}}

Wyłączenia: pełny rekord/klauzula/pozostały crop, artwork/ratingi, wcześniejsze pending, brakujące procedury, automatyczne semantyczneFP/FN/gold.

## E873

Dokładny zakres: oryginalny krótki cytat i jego prostokąt.

> This chart is used to determine which Column will be used on the Shock Combat Results Table (subject to adjustments).

Niezależny dosłowny helper:

> This chart is used
> to determine which Column will be used on the Shock Combat
> Results Table (subject to adjustments).

Helper `/regions/1/text`, znaki [531, 648], SHA-256 `d03cfea4eb764afebc7e5d145be7c7492caa9c6aea8212cc88a50e7170bde755`.

Strona31; bbox piksele [875, 480, 1575, 575], PDFpt [315.0, 172.8, 567.0, 207.0]; wymiary [1700, 2200].

Rzeczywisty krótki cytat PDFpt [315.0, 175.99699999999996, 567.02, 209.99699999999996]; całe obwiednie NIE mieszczą się. Raster: readable_but_descender_ink_clipped.

Ręczne porównanie: Cytat o wyborze Column naShockCombatResultsTable i subject toadjustments jest na właściwym miejscu. Dolna granica ucina części b/j/d oraz nawiasów ostatniej linii; obwiednia+2.997pt. Referencja/powiększenie pokazują piksele pod ramką. Zdanie pozostaje czytelne, ale obraz nie zawiera całych glifów. Nie zmienia to roli opisowejClashchart w source ani nie daje jego komórek.

[Dokładny nieposzerzony crop](../../../measurement/M-POC5A-semantic-04c1/visual-02/E873-exact.png) · [Referencja do porównania granicy](../../../measurement/M-POC5A-semantic-04c1/visual-02/E873-quote-reference.png). Referencja nie naprawia lokatora.

**first-001:** `/evidence/99`, bajty [113699,114776), SHA-256 `707f9cb73451d09eb4eb83cf396e8efe722538323959456825250095b0aeb9ff`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/99/quote/value`; bajty [114040,114159), hash `591b47cf09425881a1b9d91247fe241864e50ac452254421a5141cad0cdcc87b`; wartość "This chart is used to determine which Column will be used on the Shock Combat Results Table (subject to adjustments).".

Pole `/evidence/99/image/bbox`; bajty [114478,114549), hash `26289281f6b959058ad722de985c6cfffc7ac3013cf7310335f41f19ec69f737`; wartość [875, 480, 1575, 575].

Pole `/evidence/99/image/path`; bajty [114346,114374), hash `1909a421ea87dce812086a96fcaf7ec4f2e7380b02b0a77eefc6ba8f0b8cf997`; wartość "inputs/v1/pages/pdf-31.png".

Pole `/evidence/99/image/sha256`; bajty [114394,114460), hash `f80ec790ece408b391067b57927588a3c9963331e236524997b9d50e8f6e053e`; wartość "9edf269af78629a8bbfd809c75695e6353f7614d82d217d48ea2ecca0fd06712".

**context-01:** `/evidence/99`, bajty [152438,153544), SHA-256 `141b3909e22da1d311515bdef742b815fc642e794a1bee5ea7e2f1e8e10b739f`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/99/quote/value`; bajty [152789,152908), hash `591b47cf09425881a1b9d91247fe241864e50ac452254421a5141cad0cdcc87b`; wartość "This chart is used to determine which Column will be used on the Shock Combat Results Table (subject to adjustments).".

Pole `/evidence/99/image/bbox`; bajty [153235,153311), hash `076bef862f1a4780c2c7491167da4cec2f5f5ee5070b3cd1ac08b84008772607`; wartość [875, 480, 1575, 575].

Pole `/evidence/99/image/path`; bajty [153101,153129), hash `1909a421ea87dce812086a96fcaf7ec4f2e7380b02b0a77eefc6ba8f0b8cf997`; wartość "inputs/v1/pages/pdf-31.png".

Pole `/evidence/99/image/sha256`; bajty [153150,153216), hash `f80ec790ece408b391067b57927588a3c9963331e236524997b9d50e8f6e053e`; wartość "9edf269af78629a8bbfd809c75695e6353f7614d82d217d48ea2ecca0fd06712".

Każdy naruszony glif:

{"index": 14, "text": "d", "bbox_pdf_points": [562.0039999999999, 175.99699999999996, 567.0039999999999, 185.99699999999996], "bbox_pixels": [1561.1222222222218, 488.8805555555554, 1575.0111111111107, 516.6583333333332], "overflow_pdf_points": {"left": 0, "right": 0.0039999999999054126, "top": 0, "bottom": 0}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-0.png", "bytes": 1634, "sha256": "095541def56160943b17762753ae088c43ece34d7872da3e95ce2bc213758dc4"}}
{"index": 62, "text": "t", "bbox_pdf_points": [564.24, 187.99699999999996, 567.02, 197.99699999999996], "bbox_pixels": [1567.3333333333333, 522.2138888888887, 1575.0555555555557, 549.9916666666666], "overflow_pdf_points": {"left": 0, "right": 0.01999999999998181, "top": 0, "bottom": 0}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-1.png", "bytes": 1240, "sha256": "67189529ce09c320d2a66c8c73cefde1ce426661cee1f7e6124d53183d5c0e0d"}}
{"index": 63, "text": "R", "bbox_pdf_points": [315.0, 199.99699999999996, 321.67, 209.99699999999996], "bbox_pixels": [875.0, 555.5472222222221, 893.5277777777778, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-2.png", "bytes": 1808, "sha256": "a454f0b70364d35c51d0eb1beaaef25ecfbc6b4c20a9dfafa2cceab6258e45c9"}}
{"index": 64, "text": "e", "bbox_pdf_points": [321.67, 199.99699999999996, 326.11, 209.99699999999996], "bbox_pixels": [893.5277777777778, 555.5472222222221, 905.8611111111111, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-3.png", "bytes": 1892, "sha256": "3d0ff8bf07157237eec4758862b42cfa130aa6538f55f7cb86f6acda0ffaf368"}}
{"index": 65, "text": "s", "bbox_pdf_points": [326.11, 199.99699999999996, 330.0, 209.99699999999996], "bbox_pixels": [905.8611111111111, 555.5472222222221, 916.6666666666666, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-4.png", "bytes": 1733, "sha256": "875998005b76c2ed9d10e5718ffd560f8ae6b207b8527057287969def8d8903a"}}
{"index": 66, "text": "u", "bbox_pdf_points": [330.0, 199.99699999999996, 335.0, 209.99699999999996], "bbox_pixels": [916.6666666666666, 555.5472222222221, 930.5555555555555, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-5.png", "bytes": 1730, "sha256": "0364fdcc522693f9e15f94ab5e992668ab0d773d8589091af09d34011236afe9"}}
{"index": 67, "text": "l", "bbox_pdf_points": [335.0, 199.99699999999996, 337.78, 209.99699999999996], "bbox_pixels": [930.5555555555555, 555.5472222222221, 938.2777777777778, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-6.png", "bytes": 1282, "sha256": "5e86d85d5f18a9517c6f42664c93549410b68cea32e139f4a2b4855ba33ef13c"}}
{"index": 68, "text": "t", "bbox_pdf_points": [337.78, 199.99699999999996, 340.55999999999995, 209.99699999999996], "bbox_pixels": [938.2777777777778, 555.5472222222221, 945.9999999999998, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-7.png", "bytes": 1527, "sha256": "dcf3ed25e957cfc007318c2127f75298cfa3eef2754ee974eb51153f53c2e468"}}
{"index": 69, "text": "s", "bbox_pdf_points": [340.56, 199.99699999999996, 344.45, 209.99699999999996], "bbox_pixels": [946.0, 555.5472222222221, 956.8055555555555, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-8.png", "bytes": 1552, "sha256": "49343618236e89db280ac50bc0e8cdc95a0358adbd039e56ffc41125a09f2532"}}
{"index": 70, "text": "T", "bbox_pdf_points": [346.76800000000003, 199.99699999999996, 352.87800000000004, 209.99699999999996], "bbox_pixels": [963.2444444444446, 555.5472222222221, 980.2166666666668, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-9.png", "bytes": 1588, "sha256": "a43fcc35329499ac048de4ed029fb60f1b2aebfef9724cbe654d015297c0ec7c"}}
{"index": 71, "text": "a", "bbox_pdf_points": [352.178, 199.99699999999996, 356.618, 209.99699999999996], "bbox_pixels": [978.2722222222222, 555.5472222222221, 990.6055555555555, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-10.png", "bytes": 1637, "sha256": "af867f4725414e0e59fd6d1223601eb405e2675fb8f46753801512e074530c88"}}
{"index": 72, "text": "b", "bbox_pdf_points": [356.618, 199.99699999999996, 361.618, 209.99699999999996], "bbox_pixels": [990.6055555555555, 555.5472222222221, 1004.4944444444444, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-11.png", "bytes": 1750, "sha256": "f52eec702a16f870f1ef2f27db2df1e266ac2a95af1cd6c58a2425264c352c90"}}
{"index": 73, "text": "l", "bbox_pdf_points": [361.618, 199.99699999999996, 364.39799999999997, 209.99699999999996], "bbox_pixels": [1004.4944444444444, 555.5472222222221, 1012.2166666666666, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-12.png", "bytes": 1529, "sha256": "dfefc1e2645ea04e5f8d99c69bdf360527443a54859911c61f2cde9c3e7b6177"}}
{"index": 74, "text": "e", "bbox_pdf_points": [364.398, 199.99699999999996, 368.838, 209.99699999999996], "bbox_pixels": [1012.2166666666668, 555.5472222222221, 1024.5500000000002, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-13.png", "bytes": 1389, "sha256": "faf7398bcacc6d88a98348ab83fe71a09be74f06191f35173f4c14140dbb588e"}}
{"index": 75, "text": "(", "bbox_pdf_points": [371.338, 199.99699999999996, 374.668, 209.99699999999996], "bbox_pixels": [1031.4944444444445, 555.5472222222221, 1040.7444444444443, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 3, "dark_pixels_sample": [[1035, 575], [1036, 576], [1037, 577]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-14.png", "bytes": 1624, "sha256": "ddfea5f0e7f11b1205d2e03c462d367d9473b387cefd32127a411118c50e9ed6"}}
{"index": 76, "text": "s", "bbox_pdf_points": [374.668, 199.99699999999996, 378.558, 209.99699999999996], "bbox_pixels": [1040.7444444444443, 555.5472222222221, 1051.55, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-15.png", "bytes": 1885, "sha256": "fd76cb1e527174932024bb4d68b1192db70bb2d8ca43cf04b217316b6ff9bda6"}}
{"index": 77, "text": "u", "bbox_pdf_points": [378.558, 199.99699999999996, 383.558, 209.99699999999996], "bbox_pixels": [1051.55, 555.5472222222221, 1065.4388888888889, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-16.png", "bytes": 1794, "sha256": "3cb12fefd25374d19416288f0e91e29bb9d0f8ef921e8a81bed3f8e0981080c0"}}
{"index": 78, "text": "b", "bbox_pdf_points": [383.558, 199.99699999999996, 388.558, 209.99699999999996], "bbox_pixels": [1065.4388888888889, 555.5472222222221, 1079.3277777777778, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 5, "dark_pixels_sample": [[1077, 578], [1078, 578], [1079, 578], [1078, 579], [1079, 579]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-17.png", "bytes": 1789, "sha256": "d5be0f09969fbb8eda432085803a340f05ae0e5d83f95ccd351bcd5af76c4e33"}}
{"index": 79, "text": "j", "bbox_pdf_points": [388.558, 199.99699999999996, 391.33799999999997, 209.99699999999996], "bbox_pixels": [1079.3277777777778, 555.5472222222221, 1087.05, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 9, "dark_pixels_sample": [[1082, 575], [1083, 575], [1082, 576], [1083, 576], [1082, 577], [1079, 578], [1082, 578], [1079, 579], [1080, 579]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-18.png", "bytes": 1705, "sha256": "37537cf314aac4a56416679289679cec3fb2a4cc3f4235f48d00d433e7d6a4dc"}}
{"index": 80, "text": "e", "bbox_pdf_points": [391.338, 199.99699999999996, 395.778, 209.99699999999996], "bbox_pixels": [1087.0500000000002, 555.5472222222221, 1099.3833333333332, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-19.png", "bytes": 1797, "sha256": "b8a8b40c87f774d9e35129b29d81b1af1e92e4449e509c9759cbbc60dcf96de0"}}
{"index": 81, "text": "c", "bbox_pdf_points": [395.778, 199.99699999999996, 400.218, 209.99699999999996], "bbox_pixels": [1099.3833333333332, 555.5472222222221, 1111.7166666666667, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-20.png", "bytes": 1720, "sha256": "e87ab165c9641f7cae83e1646223edee5a83febd58317825263f9c5e29f32f34"}}
{"index": 82, "text": "t", "bbox_pdf_points": [400.218, 199.99699999999996, 402.998, 209.99699999999996], "bbox_pixels": [1111.7166666666667, 555.5472222222221, 1119.4388888888889, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-21.png", "bytes": 1302, "sha256": "48eb391e9ccb09e54fec1d6a50c7a74af93fd10f9cc626f73dc6bb40d0de1726"}}
{"index": 83, "text": "t", "bbox_pdf_points": [405.49800000000005, 199.99699999999996, 408.278, 209.99699999999996], "bbox_pixels": [1126.3833333333334, 555.5472222222221, 1134.1055555555556, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-22.png", "bytes": 1295, "sha256": "fa942344575873a91d5bd35f2172eaf4ab9e58cdb642401bbaa715492f9c474a"}}
{"index": 84, "text": "o", "bbox_pdf_points": [408.278, 199.99699999999996, 413.278, 209.99699999999996], "bbox_pixels": [1134.1055555555556, 555.5472222222221, 1147.9944444444443, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-23.png", "bytes": 1524, "sha256": "a8718c68c4f4e1057dd4ec2ef983c7ea95a241d9b749b5ef149bf6c13eb09b73"}}
{"index": 85, "text": "a", "bbox_pdf_points": [415.778, 199.99699999999996, 420.218, 209.99699999999996], "bbox_pixels": [1154.9388888888889, 555.5472222222221, 1167.2722222222221, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-24.png", "bytes": 1561, "sha256": "3a147ca10d2a9ec2deb07735b8dd7bb2c7fd34110ed088ca3d0e6930dc574ad0"}}
{"index": 86, "text": "d", "bbox_pdf_points": [420.2180000000001, 199.99699999999996, 425.2180000000001, 209.99699999999996], "bbox_pixels": [1167.2722222222224, 555.5472222222221, 1181.1611111111113, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 5, "dark_pixels_sample": [[1179, 578], [1180, 578], [1181, 578], [1180, 579], [1181, 579]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-25.png", "bytes": 1930, "sha256": "652950470328493f737d902ce46f7cf23c19917cfad7505ff4973ff9a1d47755"}}
{"index": 87, "text": "j", "bbox_pdf_points": [425.2180000000001, 199.99699999999996, 427.99800000000005, 209.99699999999996], "bbox_pixels": [1181.1611111111113, 555.5472222222221, 1188.8833333333334, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 9, "dark_pixels_sample": [[1184, 575], [1185, 575], [1184, 576], [1185, 576], [1184, 577], [1181, 578], [1184, 578], [1181, 579], [1182, 579]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-26.png", "bytes": 1529, "sha256": "2959316843f52fa6d1c4df398ac707756979b2776ee27f61803fcf60be5025d7"}}
{"index": 88, "text": "u", "bbox_pdf_points": [427.99800000000005, 199.99699999999996, 432.99800000000005, 209.99699999999996], "bbox_pixels": [1188.8833333333334, 555.5472222222221, 1202.7722222222224, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-27.png", "bytes": 1848, "sha256": "40985609655e9e1b3189079d8c8eb284aa0eed28325b316ba3f1550ba3cb1e18"}}
{"index": 89, "text": "s", "bbox_pdf_points": [432.99800000000005, 199.99699999999996, 436.88800000000003, 209.99699999999996], "bbox_pixels": [1202.7722222222224, 555.5472222222221, 1213.577777777778, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-28.png", "bytes": 1734, "sha256": "f3cc1017e64245da4bafa4833136755fb5e6b50dc71eba07459011353b65a615"}}
{"index": 90, "text": "t", "bbox_pdf_points": [436.88800000000003, 199.99699999999996, 439.668, 209.99699999999996], "bbox_pixels": [1213.577777777778, 555.5472222222221, 1221.3, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-29.png", "bytes": 1606, "sha256": "841d64cfc917c204b72dcf45070112fa3d66d461d405285e525083a117d360d3"}}
{"index": 91, "text": "m", "bbox_pdf_points": [439.66800000000006, 199.99699999999996, 447.44800000000004, 209.99699999999996], "bbox_pixels": [1221.3000000000002, 555.5472222222221, 1242.9111111111113, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-30.png", "bytes": 1952, "sha256": "b06a3f229e53da7503ac3f592218a71d9b04581be8b821c982925c60c30a4d63"}}
{"index": 92, "text": "e", "bbox_pdf_points": [447.44800000000004, 199.99699999999996, 451.88800000000003, 209.99699999999996], "bbox_pixels": [1242.9111111111113, 555.5472222222221, 1255.2444444444445, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-31.png", "bytes": 1675, "sha256": "3bc92cfef67b88da178205184d8c6a64e6849262f58b0784e968f3e1911b4b6a"}}
{"index": 93, "text": "n", "bbox_pdf_points": [451.88800000000003, 199.99699999999996, 456.88800000000003, 209.99699999999996], "bbox_pixels": [1255.2444444444445, 555.5472222222221, 1269.1333333333334, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-32.png", "bytes": 1697, "sha256": "20eb3f2409ba066d98e6f68687cdf50c71e830702a8f3d3d664096ff91258f4d"}}
{"index": 94, "text": "t", "bbox_pdf_points": [456.88800000000003, 199.99699999999996, 459.668, 209.99699999999996], "bbox_pixels": [1269.1333333333334, 555.5472222222221, 1276.8555555555556, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-33.png", "bytes": 1571, "sha256": "daf1dfbf6878b9cae5b3f713274e2726ef4fdc8021730473e95e215a0e210c1a"}}
{"index": 95, "text": "s", "bbox_pdf_points": [459.66800000000006, 199.99699999999996, 463.55800000000005, 209.99699999999996], "bbox_pixels": [1276.8555555555556, 555.5472222222221, 1287.6611111111113, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-34.png", "bytes": 1922, "sha256": "440562df14193c4543bcb76e2d0a463786a553baee0bed6bd10f6ee1115a6347"}}
{"index": 96, "text": ")", "bbox_pdf_points": [463.55800000000005, 199.99699999999996, 466.88800000000003, 209.99699999999996], "bbox_pixels": [1287.6611111111113, 555.5472222222221, 1296.9111111111113, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 2, "dark_pixels_sample": [[1292, 575], [1291, 576]], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-35.png", "bytes": 1648, "sha256": "7f5f5b8d98114bdff38050902d6a28f31f7dabd067957bfd72e5d946b7a4fe48"}}
{"index": 97, "text": ".", "bbox_pdf_points": [466.88800000000003, 199.99699999999996, 469.38800000000003, 209.99699999999996], "bbox_pixels": [1296.9111111111113, 555.5472222222221, 1303.8555555555556, 583.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 2.9969999999999573}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E873-boundary-36.png", "bytes": 1230, "sha256": "a63cadbfd4bc14a8fa08401eb5b34f31e942090f9a2e628079375464ff7a5684"}}

Wyłączenia: pełny rekord/klauzula/pozostały crop, artwork/ratingi, wcześniejsze pending, brakujące procedury, automatyczne semantyczneFP/FN/gold.

## E874

Dokładny zakres: oryginalny krótki cytat i jego prostokąt.

> This Table is used to resolve Shock Combat in terms of Cohesion Hits to both attacker and defender.

Niezależny dosłowny helper:

> This Table is used to resolve
> Shock Combat in terms of Cohesion Hits to both attacker and
> defender.

Helper `/regions/1/text`, znaki [682, 781], SHA-256 `6b716e6694a298821933ac8aa4ae4c260abe875c1cd598facf21316f08d20fd9`.

Strona31; bbox piksele [875, 595, 1575, 695], PDFpt [315.0, 214.2, 567.0, 250.2]; wymiary [1700, 2200].

Rzeczywisty krótki cytat PDFpt [315.0, 217.39699999999993, 567.1320000000001, 251.39699999999993]; całe obwiednie NIE mieszczą się. Raster: readable_no_observed_ink_loss.

Ręczne porównanie: Cytat resolveShockCombatinHitsbothattacker/defender widoczny. Ostatnia linia defender obwiednią+1.197pt i prawa e+0.132pt; raster nie pokazuje utraty cytowanego tuszu. Dalsze See10.11/10.14 poza krótkim cytatem nie jest przedmiotem nowej akceptacji.

[Dokładny nieposzerzony crop](../../../measurement/M-POC5A-semantic-04c1/visual-02/E874-exact.png) · [Referencja do porównania granicy](../../../measurement/M-POC5A-semantic-04c1/visual-02/E874-quote-reference.png). Referencja nie naprawia lokatora.

**first-001:** `/evidence/100`, bajty [114782,115841), SHA-256 `73871763ee2dfafd4cd9ee2eb5983b3ae40b4b6b2c85f95964c9d1cf84928227`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/100/quote/value`; bajty [115123,115224), hash `8ac9e265424240c03ec38b499be72630d70d356920a71fd3b1f8587e55bf43b0`; wartość "This Table is used to resolve Shock Combat in terms of Cohesion Hits to both attacker and defender.".

Pole `/evidence/100/image/bbox`; bajty [115543,115614), hash `8292d962b8fe40d382b97402ef58a9a48596702f863beaaa903189904d512fa9`; wartość [875, 595, 1575, 695].

Pole `/evidence/100/image/path`; bajty [115411,115439), hash `1909a421ea87dce812086a96fcaf7ec4f2e7380b02b0a77eefc6ba8f0b8cf997`; wartość "inputs/v1/pages/pdf-31.png".

Pole `/evidence/100/image/sha256`; bajty [115459,115525), hash `f80ec790ece408b391067b57927588a3c9963331e236524997b9d50e8f6e053e`; wartość "9edf269af78629a8bbfd809c75695e6353f7614d82d217d48ea2ecca0fd06712".

**context-01:** `/evidence/100`, bajty [153551,154639), SHA-256 `88842c1a3387094db4e6046084418b7f5058db0976cdccc447eea24184276916`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/100/quote/value`; bajty [153902,154003), hash `8ac9e265424240c03ec38b499be72630d70d356920a71fd3b1f8587e55bf43b0`; wartość "This Table is used to resolve Shock Combat in terms of Cohesion Hits to both attacker and defender.".

Pole `/evidence/100/image/bbox`; bajty [154330,154406), hash `afe7f8424afd19c413dc30356b4e6809716fd60969fbd6eecb942ba8006f3a0e`; wartość [875, 595, 1575, 695].

Pole `/evidence/100/image/path`; bajty [154196,154224), hash `1909a421ea87dce812086a96fcaf7ec4f2e7380b02b0a77eefc6ba8f0b8cf997`; wartość "inputs/v1/pages/pdf-31.png".

Pole `/evidence/100/image/sha256`; bajty [154245,154311), hash `f80ec790ece408b391067b57927588a3c9963331e236524997b9d50e8f6e053e`; wartość "9edf269af78629a8bbfd809c75695e6353f7614d82d217d48ea2ecca0fd06712".

Każdy naruszony glif:

{"index": 23, "text": "e", "bbox_pdf_points": [562.692, 217.39699999999993, 567.1320000000001, 227.39699999999993], "bbox_pixels": [1563.0333333333333, 603.8805555555554, 1575.3666666666668, 631.6583333333332], "overflow_pdf_points": {"left": 0, "right": 0.13200000000006185, "top": 0, "bottom": 0}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E874-boundary-0.png", "bytes": 1478, "sha256": "961a5de0d0e6499b5edc4e0ec1ff9ffcc4dedab6924cd8837cf48c2c5ef9dc92"}}
{"index": 73, "text": "d", "bbox_pdf_points": [315.0, 241.39699999999993, 320.0, 251.39699999999993], "bbox_pixels": [875.0, 670.5472222222221, 888.8888888888889, 698.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1969999999999459}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E874-boundary-1.png", "bytes": 1572, "sha256": "548bced4d0ced4a622ae21310a21d02289d6cd7f537cb9c52201ee100bab1d2d"}}
{"index": 74, "text": "e", "bbox_pdf_points": [320.0, 241.39699999999993, 324.44, 251.39699999999993], "bbox_pixels": [888.8888888888889, 670.5472222222221, 901.2222222222222, 698.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1969999999999459}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E874-boundary-2.png", "bytes": 1807, "sha256": "23d5065e0b568c4c4fbd40adb7f0c929a902225ba1d214469517a8d9ebe7fd30"}}
{"index": 75, "text": "f", "bbox_pdf_points": [324.44, 241.39699999999993, 327.77, 251.39699999999993], "bbox_pixels": [901.2222222222222, 670.5472222222221, 910.4722222222222, 698.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1969999999999459}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E874-boundary-3.png", "bytes": 1721, "sha256": "8d8ff2dd56670a4faf11316ba55818d611a5a35b002fa91304bc407ef4c11471"}}
{"index": 76, "text": "e", "bbox_pdf_points": [327.77, 241.39699999999993, 332.21, 251.39699999999993], "bbox_pixels": [910.4722222222222, 670.5472222222221, 922.8055555555555, 698.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1969999999999459}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E874-boundary-4.png", "bytes": 1735, "sha256": "4d1e2f28f47ef03e36e246e6386271fa2cf48796493e4a0cf78a57cbf28a96b6"}}
{"index": 77, "text": "n", "bbox_pdf_points": [332.21, 241.39699999999993, 337.21, 251.39699999999993], "bbox_pixels": [922.8055555555555, 670.5472222222221, 936.6944444444445, 698.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1969999999999459}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E874-boundary-5.png", "bytes": 1762, "sha256": "9375c5343da6efa94194541de030fd2fbb4787505123c72ee3e5f9a8e23967d5"}}
{"index": 78, "text": "d", "bbox_pdf_points": [337.21, 241.39699999999993, 342.21, 251.39699999999993], "bbox_pixels": [936.6944444444445, 670.5472222222221, 950.5833333333334, 698.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1969999999999459}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E874-boundary-6.png", "bytes": 1839, "sha256": "222fa173d8035ee7f739aa0cfb79c6b1144b0ef386d1ec8fe0daac4c410997a6"}}
{"index": 79, "text": "e", "bbox_pdf_points": [342.21, 241.39699999999993, 346.65, 251.39699999999993], "bbox_pixels": [950.5833333333334, 670.5472222222221, 962.9166666666666, 698.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1969999999999459}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E874-boundary-7.png", "bytes": 1720, "sha256": "77b5a25fa510ca6ad2be4aa1a17e6a014a80507eedb51edb865fd7e8f6bdd8a0"}}
{"index": 80, "text": "r", "bbox_pdf_points": [346.65, 241.39699999999993, 349.97999999999996, 251.39699999999993], "bbox_pixels": [962.9166666666666, 670.5472222222221, 972.1666666666665, 698.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1969999999999459}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E874-boundary-8.png", "bytes": 1349, "sha256": "45a08d667626c43e09fbe7a06614f37ae20a08daf97b7fcdc6cf3a0494f91e6b"}}
{"index": 81, "text": ".", "bbox_pdf_points": [349.424, 241.39699999999993, 351.924, 251.39699999999993], "bbox_pixels": [970.6222222222221, 670.5472222222221, 977.5666666666666, 698.3249999999999], "overflow_pdf_points": {"left": 0, "right": 0, "top": 0, "bottom": 1.1969999999999459}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E874-boundary-9.png", "bytes": 1012, "sha256": "3db4304fa0407ffc3d05d9a286887c0f08a78f814528212788a470f3be6cfa73"}}

Wyłączenia: pełny rekord/klauzula/pozostały crop, artwork/ratingi, wcześniejsze pending, brakujące procedury, automatyczne semantyczneFP/FN/gold.

## E875

Dokładny zakres: oryginalny krótki cytat i jego prostokąt.

> Use this as a summary of when Cohesion Hits are applied and when TQ checks take place.

Niezależny dosłowny helper:

> Use this as
> a summary of when Cohesion Hits are applied and when TQ
> checks take place.

Helper `/regions/1/text`, znaki [845, 931], SHA-256 `3fe5be6ed6b450b3ffc7b6b3a71b45c3cb8d1091d64da1afdb93f76bc6ca5a2d`.

Strona31; bbox piksele [875, 705, 1575, 815], PDFpt [315.0, 253.8, 567.0, 293.4]; wymiary [1700, 2200].

Rzeczywisty krótki cytat PDFpt [315.0, 258.7969999999999, 567.009, 292.79699999999985]; całe obwiednie NIE mieszczą się. Raster: readable_no_observed_ink_loss.

Ręczne porównanie: Cytat summarywhenHits/TQchecks takeplace widoczny. Końcowe s wTQchecks prawej obwiedni+0.009pt. Raster czytelny; nie akceptuje actualcharttiming/results ani całegoTQprocessing.

[Dokładny nieposzerzony crop](../../../measurement/M-POC5A-semantic-04c1/visual-02/E875-exact.png) · [Referencja do porównania granicy](../../../measurement/M-POC5A-semantic-04c1/visual-02/E875-quote-reference.png). Referencja nie naprawia lokatora.

**first-001:** `/evidence/101`, bajty [115847,116893), SHA-256 `f1a0a507da98abb022a70463d595f48a43cc2758a7acf7afd6e6ca2ab28eb8a4`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/101/quote/value`; bajty [116188,116276), hash `55707e3c05ed6577ef8e34441a2a8fb5126333f4e024fc98edde2f988a389339`; wartość "Use this as a summary of when Cohesion Hits are applied and when TQ checks take place.".

Pole `/evidence/101/image/bbox`; bajty [116595,116666), hash `5d772a739bebbfe7f39fa0c56c9ef17973590051078c4c7182bd8dcb896d6561`; wartość [875, 705, 1575, 815].

Pole `/evidence/101/image/path`; bajty [116463,116491), hash `1909a421ea87dce812086a96fcaf7ec4f2e7380b02b0a77eefc6ba8f0b8cf997`; wartość "inputs/v1/pages/pdf-31.png".

Pole `/evidence/101/image/sha256`; bajty [116511,116577), hash `f80ec790ece408b391067b57927588a3c9963331e236524997b9d50e8f6e053e`; wartość "9edf269af78629a8bbfd809c75695e6353f7614d82d217d48ea2ecca0fd06712".

**context-01:** `/evidence/101`, bajty [154646,155721), SHA-256 `e7ed6bd500b72c1c52a9428fc25c497a0e6396c1ee1e03a239f7d0bf0b5d2f32`. RecenzentCodex, humanwaiting_review.

Pole `/evidence/101/quote/value`; bajty [154997,155085), hash `55707e3c05ed6577ef8e34441a2a8fb5126333f4e024fc98edde2f988a389339`; wartość "Use this as a summary of when Cohesion Hits are applied and when TQ checks take place.".

Pole `/evidence/101/image/bbox`; bajty [155412,155488), hash `31f30733dbb7642be5fb3c10c37d73bb30aaadb58ca37248115f82f73d3c6271`; wartość [875, 705, 1575, 815].

Pole `/evidence/101/image/path`; bajty [155278,155306), hash `1909a421ea87dce812086a96fcaf7ec4f2e7380b02b0a77eefc6ba8f0b8cf997`; wartość "inputs/v1/pages/pdf-31.png".

Pole `/evidence/101/image/sha256`; bajty [155327,155393), hash `f80ec790ece408b391067b57927588a3c9963331e236524997b9d50e8f6e053e`; wartość "9edf269af78629a8bbfd809c75695e6353f7614d82d217d48ea2ecca0fd06712".

Każdy naruszony glif:

{"index": 8, "text": "s", "bbox_pdf_points": [563.119, 258.7969999999999, 567.009, 268.7969999999999], "bbox_pixels": [1564.2194444444444, 718.8805555555552, 1575.025, 746.6583333333331], "overflow_pdf_points": {"left": 0, "right": 0.009000000000014552, "top": 0, "bottom": 0}, "dark_pixels_outside_original_crop": 0, "dark_pixels_sample": [], "pixel_diagnostic_limitation": "Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.", "magnified_boundary_patch": {"path": "private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04c1/visual-02/E875-boundary-0.png", "bytes": 1520, "sha256": "1beba8906868df444ac818fb251f2d457d794c86ab5634c74bfdf2da17076ae1"}}

Wyłączenia: pełny rekord/klauzula/pozostały crop, artwork/ratingi, wcześniejsze pending, brakujące procedury, automatyczne semantyczneFP/FN/gold.

## Granice i wznowienie

Przypisano22ID/44wystąpienia i każde realnie porównano. Udostępniono44, porównano44, nowych decyzji właściciela0, pending44. Kolejne80wystąpień ma jawny przydział w .4c2/.4c3, tutaj nie wykonane.
Owner-decision07 przyjmuje poprzednie68+2+2 zakresów .4b3; razem257 komponentowych ocen relacji. Nie daje całych poprawnych rekordów/grafu. Osiem wcześniejszych oczekiwań/SEM-001–013 w pozostałych zakresach otwarte; SEM-005/007 mają teraz ograniczone propozycje lokatorowe, bez automatycznego zamknięcia.
Brak nowych źródeł/korekt/ekstrakcji/sytuacji; eval-v1/gold i limity bez zmiany. Pełne metryki/TP/FP/FN, aktywne czasy i budżet nieocenione. Izolacja dawnego context-01 bez zmiany: listing/path pozaallowlistą potwierdzony, odczyt treści oceny niezaobserwowany; exposure/cleancontextunknown.
Po decyzji obecnego pakietu osobna .4c2,21ID/42wystąpienia po oszacowaniu. Nadrzędne M-POC5A/.4/.4b/.4c partial; M-POC5 jedyny next.
