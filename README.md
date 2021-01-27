# SmartGrid
Groene energie is de energie van de toekomst, en zelf produceren is de mode van nu. Veel huizen hebben tegenwoordig zonnepanelen, windmolens of andere installaties om zelf energie mee te produceren. Fortuinlijk genoeg produceren die installaties vaak meer dan voor eigen consumptie nodig is. Het overschot zou kunnen worden terugverkocht aan de leverancier, maar de infrastructuur (het grid) is daar veelal niet op berekend. Om de pieken in consumptie en produktie te kunnen managen moeten er batterijen geplaatst worden.
Voor een feasibility study zijn drie dummy-woonwijken opgesteld, met daarin vijf batterijen. De huizen hebben zonnepanelen met een maximale output, de batterijen hebben een maximale capaciteit.
De opdracht is om alle huizen aan de batterijen te koppelen zodat de kosten van de kabels geminimaliseerd zijn, maar alle huizen toch voorzien zijn van stroom!

# Algoritmen

## Baseline Algoritmen
Het random en greedy algoritme zijn baseline algoritmen. Dit betekent dat er nog geen oplossing is, alleen huizen en batterijen die op een goede manier aan elkaar gekoppeld moeten worden door middel van kabels. Er zijn drie woonwijken (districts), met 150 huizen en 5 batterijen per wijk.

### Random
Bij dit random algoritme hebben wij de aanname gedaan dat er dus aan elke batterij (150 / 5 =) 30 huizen gekoppeld moeten worden. In dit algoritme worden er dus 30 random huizen aan elke batterij gekoppeld, totdat er een feasible solution uit komt.

### Greedy
Wij hebben twee verschillende greedy algoritmen toegepast:
- Eén waarbij we vanuit elke batterij kijken naar de dichtstbijzijnde huizen, dus we gaan elke batterij langs en koppelen alle dichtstbijzijnde huizen aan die batterij, totdat de batterij geen capaciteit meer heeft. En zo gaan we alle batterijen langs totdat de batterijen vol zitten. Echter geeft dit greedy algoritme niet altijd een feasible solution. Dit specifieke greedy algoritme geeft alleen een feasible solution voor district 2 en niet voor district 1 en 2.
- Eén waarbij we vanuit elk huis kijken naar de dichtstbijzijnde batterij, waarbij de huizen op output van hoog naar laag zijn gesorteerd. Dus kijkend naar de huizen, beginnend met het huis met de hoogste output en deze koppelen aan de dichtstbijzijnde batterij (die nog genoeg capaciteit over heeft) en zo door totdat (alle) huizen gekoppeld zijn. Echter geeft dit greedy algoritme ook niet altijd een feasible solution. Dit specifieke greedy algoritme geeft alleen een feasible solution voor district 1 en 3 en niet voor district 2.

## Optimalisatie Algoritmen
Het Hill Climber en Simulated Annealing algoritme zijn optimalisatie algoritmen. Dit betekent dat er al een feasible start-oplossing bestaat en dat deze oplossing door middel van een optimalisatie algoritme wordt verbeterd.

### Hill Climber
Bij het Hill Climber algoritme worden er vanuit een start-oplossing telkens twee random huizen gekozen die aan verschillende batterijen zijn gekoppeld. Deze twee huizen worden omgewisseld. Vervolgens vergelijken we de totale kosten voor de wissel en na de wissel. Als de kosten na de wissel lager zijn dan voor de wissel (verbetering), dan behouden we de wissel. Zo niet (verslechtering), dan wordt de wissel ongedaan gemaakt. Dit proces wordt n iteraties herhaald.

### Hill Climber
Hill Climber begint bij een begin staat in het systeem dat gedefinieerd wordt door de connecties tussen de batterijen en hun respectievelijke huizen. Vervolgens wordt een swap, waarbij een huis van een batterij wordt losgemaakt en aan een andere batterij wordt vastgemaakt, uitgeprobeerd. Als de swap als resultaat de totale kosten van het systeem verlaagt wordt de swap definitief gemaakt en wordt er opnieuw gezocht naar een andere swap. Dit process is vergelijkbaar met Newtons algoritme en loopt tegen soortgelijke problemen op met lokale minima. Het is nuttig om de twee algoritmes, hun toepassingen en de limieten van hun toepassingen te vergelijken. Newton's algoritme wordt typisch weergegeven als een algoritme toepasselijk op een eendimensionale continue ruimte. Het algoritme begint op een punt in de functie en neemt vervolgens (numeriek) de afgeleide waarna een stap genomen op de x-as evenredig met de afgeleide. Als een piek word wordt bereikt is de afgeleide en dus de stapgrootte nul en is er een lokaal optimum bereikt. En als de functie numeriek doorschiet voorbij de piek verandert de afgeleide van teken en wordt een stap in de omgekeerde richting gemaakt. In ons probleem is er geen continue ruimte, een swap kan namelijk niet (nuttig) worden opgedeeld in kleinere swaps. Omdat er 150*149 swaps mogelijk zijn is de ruimte die hillclimber probeert te optimaliseren 150*149 dimensionaal en discreet. Omdat de ruimte veel “groter” is zijn er een veel groter aantal lokale minima en is dus de kans dat het minimum dat hillclimber vind het globale minimum is erg klein.

### Simulated Annealing
(pseudocode):
- Kies een random start state
- Kies start temperatuur
- Herhaal n iteraties:
  - Doe een kleine random aanpassing
  - Als random() > kans(oud, nieuw, temperatuur):
    - Maak de aanpassing ongedaan
  - Verlaag temperatuur

### Simulated Annealing
Simulated Annealing (SA) onttrekt zijn naam uit het temperen van ijzer, de kristalstructuur van het metaal nadat het afgekoeld is hangt namelijk af van hoe snel die koeling heeft geduurd. SA heeft namelijk een analoge temperatuur die beïnvloedt hoe het algoritme zich door de oplossing ruimte heen beweegt. SA is gepast voor een algoritme waar er in de oplossing ruimte veel lokale minima zijn waardoor Hill Climber vast zou te komen te zitten. Net zoals Hillclimber past SA swaps toe en vergelijkt de prijs van de nieuwe en oude staat, echter waar Hillclimber altijd staten met een hogere prijs verwerpt accepteert SA soms staten die een hogere prijs hebben (SA accepteert altijd een staat met een lagere prijs). De kans P, om een staat met een hogere prijs te accepteren is evenredig met Exp(K/T) waarbij K het prijs verschil is tussen de 2 staten en T de temperatuur. Aangezien deze kans alleen wordt berekend als de nieuwe prijs hoger is is K<0. De temperatuur is homogeen afnemend als functie van de hoeveelheid interacties (swaps) die het algoritme heeft doorgelopen. Iedere homogeen afnemende functie voldoet de literatuur gebruikt typisch 0.99^n waar n de hoeveelheid iteratie zijn. Als K toeneemt wordt P (snel) kleiner en als T toeneemt wordt P (snel) groter. Aan het begin van ons algoritme worden swaps die de kosten tijdelijk omhoog brengen vaak gedaan. Dit is de crux van SA, doordat er soms wel swaps worden gedaan die de kosten verhogen kan het algoritme locale optimus ontsnappen. Naarmate het algoritme meer iteraties doet convergeert het naar hillclimber. SA reduceert namelijk tot Hillclimber voor T=0. Dit is ook belangrijk omdat voor een T groter dan nul het algoritme niet hoeft te convergeren naar een staat. 
