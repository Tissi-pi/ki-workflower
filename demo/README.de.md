# KI-Workflower – öffentliche Demo-Fallstudie

## Nachweis vor Freigabe

Eine kleine Softwareänderung kann erstaunlich viele Fragen aufwerfen.

In dieser Fallstudie geht es um einen vorhandenen Messdaten-Exporter. Er liest CSV-Daten und erzeugt daraus einen Textbericht. Die Aufgabe klingt zunächst überschaubar:

> **Ergänze einen JSON-Export, ohne bestehende Daten, Genauigkeit, Reihenfolge oder das bisherige Programmverhalten unbeabsichtigt zu verändern.**

Genau an der Frage, wie eine Änderung umgesetzt werden kann, ohne dabei bestehendes Verhalten unbeabsichtigt zu beeinträchtigen, setzt KI-Workflower an.

Denn eine neue Funktion allein reicht nicht. Am Ende sollte nachvollziehbar sein, ob die vereinbarten Anforderungen tatsächlich erfüllt sind, welche Risiken geprüft wurden und ob der bisherige Bestand erhalten geblieben ist.

Diese Fallstudie zeigt deshalb nicht die interne Technik von KI-Workflower, sondern das, was von außen überprüfbar sein soll: Entscheidungen, Auswirkungen und Nachweise.

## 1. Erst ausprobieren, dann entscheiden

Bevor die eigentliche Änderung programmiert wurde, stand eine einfache Frage im Raum:

Wie lassen sich Messwerte und Zeitstempel in den neuen JSON-Export übernehmen, ohne ihre Bedeutung zu verändern?

Dafür wurde zunächst ein kleiner Proof of Concept (PoC) durchgeführt – also ein gezielter technischer Vorversuch.

Dabei zeigte sich:

- Ein naheliegender `float`-basierter Rundlauf erhielt die Dezimalwerte nicht zuverlässig genug.
- Ein dezimalwerttreuer Ansatz bestand den Vergleich.
- Die geprüfte Behandlung der Zeitstempel erhielt ihre zeitliche Bedeutung.

Das hatte eine unmittelbare Folge: Der `float`-Ansatz wurde für die Messwerte verworfen, noch bevor die eigentliche Implementierung begann.

Genau dafür ist ein PoC gedacht. Er soll nicht nachträglich bestätigen, was ohnehin gebaut wurde, sondern früh genug zeigen, ob eine technische Idee trägt.

Hier hat der Vorversuch die spätere Lösung tatsächlich verändert.

## 2. Was bedeutet „die Änderung funktioniert“?

„JSON-Export hinzufügen“ beschreibt eine Funktion. Für eine belastbare Abnahme reicht das noch nicht.

Deshalb wurden die fachlichen Erwartungen mit QFD – Quality Function Deployment – in konkrete, prüfbare Merkmale übersetzt.

Für diese Änderung bedeutete das unter anderem:

- Die JSON-Struktur muss gültig sein.
- Jeder Datensatz muss vollständig und genau einmal übernommen werden.
- Dezimalwerte müssen werttreu erhalten bleiben.
- Zeitstempel dürfen ihre zeitliche Bedeutung nicht verlieren.
- Der bisherige Textbericht muss sich weiterhin gleich verhalten.
- Fehlerhafte Eingaben dürfen nicht unbemerkt akzeptiert werden.

Aus einer allgemeinen Aufgabenbeschreibung wurden damit konkrete Fragen, auf die es am Ende jeweils eine überprüfbare Antwort geben musste.

## 3. Risiken benennen reicht nicht

Als Nächstes ging es darum, was bei der Änderung schiefgehen könnte.

Im Risikoregister wurden unter anderem diese Möglichkeiten betrachtet:

- Datensätze könnten verloren gehen oder doppelt erscheinen.
- Zahlenwerte könnten sich unbemerkt verändern.
- Zeitangaben könnten eine andere Bedeutung bekommen.
- Der bisherige Textbericht könnte durch die Erweiterung beeinflusst werden.
- Fehlerhafte Eingaben könnten versehentlich als gültig behandelt werden.

Der wichtige Punkt dabei: Die Risiken wurden nicht nur aufgeschrieben. Jedem relevanten Risiko wurde eine konkrete Kontrolle zugeordnet.

Damit war vor der Umsetzung klarer, wonach später tatsächlich gesucht werden musste.

## 4. Eine zusätzliche Frage, die vorher fehlte

Die Mini-FMEA – eine kompakte Fehlermöglichkeits- und Einflussanalyse – ging noch einen Schritt weiter.

Sie fragte nicht nur: „Was kann schiefgehen?“, sondern auch: „Welche konkrete Fehlersituation könnte bisher übersehen worden sein?“

Dabei fiel ein Fall auf:

> Ein unvollständiger Export könnte fälschlich als erfolgreich behandelt werden.

Dieser Punkt war im bisherigen Prüfplan noch nicht ausreichend abgesichert.

Die Folge war konkret:

- ein zusätzliches Risiko,
- eine zusätzliche Prüfbedingung,
- ein weiteres Abnahmekriterium.

Die Mini-FMEA blieb damit nicht auf dem Papier. Sie veränderte den Prüfplan.

## 5. Was vor dem Abschluss nachgewiesen sein musste

Am Ende standen sieben Abnahmekriterien:

1. gültige JSON-Struktur,
2. vollständige und genau einmalige Datensatzübernahme,
3. Dezimalwerttreue,
4. Erhalt der zeitlichen Bedeutung,
5. Erhalt des bestehenden Textverhaltens,
6. fehlerhafte Eingaben werden nicht unbemerkt akzeptiert,
7. ein unvollständiger Export darf keinen falschen Erfolgszustand erzeugen.

Das siebte Kriterium war zu Beginn noch nicht vorhanden. Es entstand erst durch die vorherige Fehleranalyse.

Das ist für diese Fallstudie wesentlich: Die Methoden wurden nicht nachträglich um das Ergebnis herum beschrieben. Sie hatten bereits im Prüfprozess sichtbare Auswirkungen auf das, was anschließend geprüft werden musste.

## 6. Nicht nur prüfen, was neu ist

Bei Änderungen an bestehender Software interessiert nicht nur, ob die neue Funktion arbeitet.

Mindestens ebenso wichtig ist die Frage:

**Was durfte durch diese Änderung gerade nicht verändert werden?**

Deshalb wurde vor der Implementierung festgelegt, welcher Teil der Software verändert werden durfte und welcher bestehende Bestand geschützt blieb.

Die spätere Nicht-Verlust-Prüfung betrachtete deshalb auch:

- den vereinbarten Änderungsumfang,
- den geschützten Ausgangsbestand,
- das bisherige Textverhalten,
- mögliche unbeabsichtigte Änderungen außerhalb des vorgesehenen Bereichs.

Damit ergänzt die Nicht-Verlust-Prüfung die klassische Funktionsprüfung um eine zweite Perspektive: Nicht nur „Ist das Neue da?“, sondern auch „Ist das Bestehende noch so, wie es sein soll?“

## 7. Elf grüne Tests – und trotzdem noch nicht fertig

Nach der ersten Implementierung sah zunächst alles gut aus.

Elf Tests waren erfolgreich. Auch die JSON-Ausgabe, die Dezimalwerttreue, das bestehende Textverhalten, der geschützte Bestand und der vereinbarte Änderungsumfang zeigten keine festgestellte Abweichung.

Man hätte an dieser Stelle sagen können: erledigt.

Genau hier wurde die Nachweiskette wichtig.

Beim Abgleich von Anforderungen, Risiken, Prüfungen und Ergebnissen zeigte sich, dass ein bereits geforderter Punkt für den neuen JSON-Pfad noch nicht ausdrücklich belegt war: Wie verhält sich das Programm bei einer fehlerhaften Eingabe?

Es gab keinen entdeckten Programmfehler. Es fehlte etwas anderes: **der ausdrückliche Nachweis für einen bereits geforderten Fehlerfall**.

Deshalb kam genau dafür ein weiterer Test hinzu.

Danach ergab sich:

- 12 von 12 Tests erfolgreich,
- der geprüfte JSON-Fehlerfall endete mit Fehlerstatus,
- dabei entstand keine JSON-Ausgabedatei,
- das zugehörige Abnahmekriterium war nun ausdrücklich nachgewiesen.

Für mich ist das der entscheidende Punkt dieser Demo:

> **Grüne Tests allein sagen noch nicht, ob wirklich alles geprüft wurde, was vorher als notwendig festgelegt war.**

Nicht die Zahl der grünen Tests entscheidet über den Abschluss, sondern die Frage, ob für die vereinbarten Anforderungen und Risiken die nötigen Nachweise vorhanden sind. KI-Workflower verschiebt den Blick damit von der reinen Testausführung auf den Zusammenhang zwischen Anforderungen und Nachweisen.

**Nachweis statt Erfolgszahl:** Ein Test ist nicht wertvoll, weil er grün ist, sondern weil er einem konkreten **Abnahmekriterium** zugeordnet ist.

## 8. Zum Schluss noch einmal die ausführbare Wirklichkeit prüfen

Neben der fachlichen Nachweiskette gab es am Ende zusätzliche technische Abschlusskontrollen.

Geprüft wurden:

- Python-Syntax und Kompilierbarkeit,
- die vollständige Testsuite,
- die gültige JSON-Referenz,
- der reale Textbericht als Rückfallkontrolle,
- die reale JSON-Ausgabe.

Alle fünf Kontrollen waren erfolgreich.

Damit beruhte der Abschluss nicht nur auf einzelnen Testaussagen, sondern zusätzlich auf Kontrollen des tatsächlich ausführbaren Endstands.

## 9. Was „FEUERFEST“ hier bedeutet

Der Begriff **FEUERFEST** soll nicht den Eindruck erwecken, Software könne garantiert fehlerfrei sein.

Gemeint ist etwas engeres und überprüfbares:

> **FEUERFEST ist ein nachgewiesener Projektzustand innerhalb eines zuvor festgelegten Prüf- und Nachweisumfangs.**

Für diese Demo durfte dieser Status deshalb erst am Ende stehen – nachdem die vorher festgelegten Bedingungen tatsächlich geprüft waren.

Der geprüfte Stand ergab:

- Abnahmekriterien: **7/7 PASS**
- Risikokontrollen: **6/6 PASS**
- Mini-FMEA-Maßnahmen: **5/5 PASS**
- Testsuite: **12/12 PASS**
- Nicht-Verlust-Prüfung: **PASS**
- technische Kontrollen: **5/5 PASS**
- Abschlussstatus: **FEUERFEST**

Der Begriff ist also nicht die Behauptung. Er ist die Zusammenfassung eines nachgewiesenen Zustands.

## 10. Was ich mit dieser kleinen Demo zeigen möchte

Die Softwareänderung wurde bewusst klein gewählt. Nicht die Größe des Programms ist hier interessant, sondern die Wirkungskette der einzelnen Schritte.

Der PoC verhinderte, dass ein ungeeigneter technischer Ansatz einfach weiterverwendet wurde.

QFD machte aus allgemeinen Erwartungen konkrete, prüfbare Merkmale.

Das Risikoregister verband mögliche Fehler mit konkreten Kontrollen.

Die Mini-FMEA brachte ein Fehlerszenario ans Licht, das den Prüfplan tatsächlich erweiterte.

Die Nicht-Verlust-Prüfung richtete den Blick darauf, was durch die Änderung unangetastet bleiben musste.

Und die Nachweiskette machte schließlich sichtbar, warum elf erfolgreiche Tests noch nicht genügten.

Erst als auch die fehlende Evidenz ergänzt und die technischen Abschlusskontrollen bestanden waren, war der vereinbarte Prüf- und Nachweisumfang vollständig.

Um ein **Auseinanderdriften** von Testergebnissen und tatsächlichem Qualitätsanspruch **zu verhindern**, verschiebt KI-Workflower den Blick von

**„Der Coding-Agent sagt: fertig.“**

auf

**„Für den geprüften Projektstand ist nachvollziehbar belegt, warum er als fertig gelten kann.“**

## 11. Die Frage hinter KI-Workflower

Am Ende läuft die gesamte Fallstudie auf eine einfache Frage hinaus:

> **Wodurch ist nachgewiesen, dass eine konkrete Anforderung im geprüften Projektstand tatsächlich erfüllt ist?**


Grüne Tests sind Mittel zum Zweck. Erst ihre gezielte Zuordnung zu Anforderungen und Risiken macht sie zu einem belastbaren Nachweis. Deshalb stellt KI-Workflower diese Frage nicht erst am Ende, sondern bindet sie von Anfang an in den Entwicklungsablauf ein.

**Hinweis zur Veröffentlichung**

Diese Fallstudie beschreibt ausgewählte öffentliche Prinzipien, Ergebnisse und Nachweise von KI-Workflower. Die vollständige Methodik und die interne Implementierung der Prüf- und Nachweisschicht sind nicht Bestandteil dieser Veröffentlichung.
