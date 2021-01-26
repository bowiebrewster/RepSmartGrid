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
Het Simulated Annealing en Hill Climber algoritme zijn optimalisatie algoritmen. Dit betekent dat er al een feasible start-oplossing bestaat en dat deze oplossing door middel van de optimalisatie algoritmen wordt verbeterd.

### Simulated Annealing
(pseudocode):
- Kies een random start state
- Kies start temperatuur
- Herhaal N iteraties:
  - Doe een kleine random aanpassing
  - Als random() > kans(oud, nieuw, temperatuur):
    - Maak de aanpassing ongedaan
  - Verlaag temperatuur

Bij het Simulated Annealing algoritme wordt er ten eerste een start-oplossing en start temperatuur gekozen. 

### Hill Climber
Bij het Hill Climber algoritme worden er telkens twee random huizen gekozen die aan verschillende batterijen zijn gekoppeld en deze worden omgewisseld. Vervolgens vergelijken we de totale kosten voor de wissel en na de wissel. Als de kosten na de wissel lager zijn dan voor de wissel (verbetering), dan behouden we de wissel. Zo niet (verslechtering), dan wordt de wissel ongedaan gemaakt. Dit proces wordt N iteraties herhaald.
