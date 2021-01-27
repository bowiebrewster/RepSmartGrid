# SmartGrid
Groene energie is de energie van de toekomst, en zelf produceren is de mode van nu. Veel huizen hebben tegenwoordig zonnepanelen, windmolens of andere installaties om zelf energie mee te produceren. Fortuinlijk genoeg produceren die installaties vaak meer dan voor eigen consumptie nodig is. Het overschot zou kunnen worden terugverkocht aan de leverancier, maar de infrastructuur (het grid) is daar veelal niet op berekend. Om de pieken in consumptie en produktie te kunnen managen moeten er batterijen geplaatst worden. Voor een feasibility study zijn drie dummy-woonwijken opgesteld, met daarin 5 batterijen en 150 huizen. De huizen hebben zonnepanelen met een maximale output en de batterijen hebben een maximale capaciteit. Alle huizen moeten aan de batterijen gekoppeld door middel van kabels. Op een manier dat de maximale capaciteit van de baterijen niet wordt overschreden en dat alle huizen wel aan een batterij gekoppeld zijn. Elke batterij kost €5000,- en elk grid-segment waar de kabel over loopt kost €9,-.

De opdracht is om alle huizen aan de batterijen te koppelen zodat de totale kosten geminimaliseerd zijn, maar alle huizen toch voorzien zijn van stroom!

# Algoritmen

## Baseline Algoritmen
Het random en greedy algoritme zijn de baseline algoritmen. Dit betekent dat er oplossing is, dus dat huizen en batterijen op een goede manier aan elkaar gekoppeld zijn door middel van kabels. Deze oplossing is echter ver van optimaal. Daarom is een baseline algoritme een goed startpunt bij het ontwikkelen van betere oplossingen in de optimalisatie algoritmen.

### Random
Bij dit random algoritme hebben wij de aanname gedaan dat elke batterij aan evenveel huizen verbonden is. In dit algoritme worden er dus 30 willekeurige huizen aan elke batterij gekoppeld, totdat er een geldige oplossing uit komt.

### Greedy
Wij hebben twee verschillende greedy algoritmen toegepast:
- Eén waarbij we vanuit elke batterij kijken naar de dichtstbijzijnde huizen. Hierbij gaan we elke batterij langs en koppelen alle dichtstbijzijnde huizen aan die batterij, totdat de batterij geen capaciteit meer over heeft. Zo gaan we alle batterijen langs totdat ze allemaal vol zitten. Echter geeft dit greedy algoritme niet altijd een geldige oplossing. Dit specifieke greedy algoritme geeft alleen een geldige oplossing voor woonwijk 2.
- Eén waarbij we vanuit elk huis kijken naar de dichtstbijzijnde batterij, waarbij de huizen op output van hoog naar laag zijn gesorteerd. We pakken steeds het huis met de hoogste output en kijken of deze gekoppeld kan worden aan de dichtsbijzijnde batterij, mits deze nog capaciteit over heeft. We gaan zo door tot alle huizen gekoppeld zijn. Echter geeft dit greedy algoritme ook niet altijd een geldige oplossing. Dit specifieke greedy algoritme geeft alleen een geldige oplossing voor district 1.

## Optimalisatie Algoritmen
Het hill climber en simulated annealing algoritme zijn optimalisatie algoritmen. Dit betekent dat er al een geldige start-oplossing bestaat en dat deze oplossing door middel van een optimalisatie algoritme wordt verbeterd.

### Hill Climber
Hill climber begint bij een begin staat in het systeem dat gedefinieerd wordt door de connecties tussen de batterijen en hun respectievelijke huizen. Vervolgens wordt een swap, waarbij een huis van een batterij wordt losgemaakt en aan een andere batterij wordt vastgemaakt, uitgeprobeerd. Als de swap de totale kosten van het systeem verlaagt, en er dus een verbetering plaatsvindt, wordt de swap definitief gemaakt en wordt er opnieuw gezocht naar een andere swap. Dit proces wordt n keer herhaald. Hill climbing vindt een optimale oplossing (globaal minimum) voor convexe problemen. In elk ander geval zal het een lokaal minimum opleveren, omdat het algoritme slechts verbeteringen accepteert en hierdoor ontstaat de situatie dan het niet uit een lokaal minimum kan springen.

### Simulated Annealing
Simulated annealing onttrekt zijn naam uit het temperen van ijzer, de kristalstructuur van het metaal nadat het afgekoeld is hangt namelijk af van hoe snel die koeling heeft geduurd. Simulated annealing heeft namelijk een analoge temperatuur die beïnvloedt hoe het algoritme zich door de oplossing ruimte heen beweegt. Waar hill climber vast zou komen te zitten in een lokaal minimum, biedt simulated annealing een betere oplossing door soms ook verslechteringen te accepteren. Hierdoor is het mogelijk om uit een lokaal minimum te springen. Net zoals hill climber past simulated annealing swaps toe en vergelijkt de prijs van de nieuwe en oude staat. De kans om de nieuwe staat te accepteren, is geheel aan kans overgelaten. De kans om een staat met een hogere prijs te accepteren is evenredig met exp(K/T), waarbij K het prijsverschil is en T de temperatuur. Deze kans wordt vergeleken met een willekeurig getal tussen 0 en 1. Hierdoor is het mogelijk om een verlechtering te accepteren, om vervolgens in een ander minimum toe te kunnen treden. In dit proces neemt de temperatuur exponentieel af en stopt het algoritme wanneer deze zeer klein is. Hoe lager de temperatuur, hoe meer de oplossing naar het (globale) minimum zal convergeren.

# Interface
De resultaten van dit probleem zijn heel makkelijk te reproduceren. In het main script wordt de gebruiker een aantal vragen gesteld waarna het optimalisatie proces wordt gestart. Na het toepassen van een van de baseline algoritme wordt gevraagd of de gebruiker deze oplossing wil verbeteren. Als dat het geval is, worden een van de twee optimalisatie algoritmen toegepast.