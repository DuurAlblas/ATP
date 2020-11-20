# ATP

## Gekozen taal
De taal die ik heb gekozen is This=That(3.0++). Ik ga de diverse versies (1.0, 2.0 en 3.0) hiervan implementeren en ik zal ook lichtelijk aanpasseningen aanbrengen. Een paar voorbeelden van die aanpassingen zijn bijvoorbeeld dat functies een `return` statement krijgen en dat variablen niet formules krijgen toegewezen maar daadwerkelijke waarden.

### Afspraken
Elke lijn code is in principe een case-sensitive variable naam gevolgd door een `=` en dan een case-sensitive waarde.
Het is belangrijk dat er spaties tussen de diverse keywords en operators in staan. Strings moeten worden encased in `"` en mogen geen spaties bevatten. Executie van de code begint bij de eerste lijn code en zal van boven naar beneden door de lijnen code heengaan. Als een variable een nieuwe waarde krijgt toegewezen zal de variable ook daadwerkelijk die waarde krijgen en niet een formule. Met andere woorden als een variable `x minus 2` krijgt toegewezen wordt de daadwerkelijke waarde op dat moment toegewezen en niet de formule.

### Keywords
|Keyword|Uitleg|
|---|---|
|`print`|Print de waarde van de variable naar de STDOUT. Ex: `x = print`|
|`input`|Ken een waarde van de STDIN toe aan een variable. Ex: `x = input`|
|`plus`,`minus`,`divide`,`times`| Voor wiskunde. Ex: </br> `x = 4` </br> `y = x minus 2` </br> Dit geeft `x` de waarde `4` en daarna `y` `2` (4-2). Bij strings werkt het als volgt: </br> `fruit = "fly"` </br> `printer = "paper"` </br> `sticky = fruit plus printer` </br> Geef `fruit` de waarde `"fly"`, `printer` de waarde `"paper"` en dan krijgt `sticky` de waarde `"flypaper"` (wordmath werkt alleen met plus).|
|`if x =`*`condition`*|Start een `if` statement genaamd `x` met een gegeven conditie|
|`while x =`*`condition`*|Start een `while` loop genaamd `x` met een gegeven conditie|
|`end if x` `end while x`|Eindigt een `if`/`while` loop genaamd `x`|
|`function MyFunction = param param2`|Maak een functie genaamd `MyFunction` en geef de functie de parameters `param` en `param2` mee.(Spatie gescheiden)|
|`return`|In een functie wordt `return` gebruikt om een waarde terug te geven door `=` achter `return` te zetten of direct de functie uit te springen als er geen `=` achter `return` staat.|
|`end function MyFunction`|Eindig de functie genaamd `MyFunction`|
|`start function MyFuntion`|Start de functie. Indien er een waarde wordt gereturned wordt er voor het keyword `start` een variable gezet met een `=` teken. Ex: `result = start function AddTwo 6`.|

### Condities
Condities bestaan uit 3 delen, 2 waarden om te vergelijken en een vergelijkings symbool. De taal kent de volgende vergelijkings symbolen:

|Symbool|Actie|
|---|---|
|`>`|Groter dan|
|`<`|Kleiner dan|
|`~`|Niet gelijk aan|
|`~>`|Niet groter dan|
|`~<`|Niet kleiner dan|
|`~~`|Gelijk aan|

### Turing compleet
Brainfuck is een turing complete taal. Door aan te tonen dat de This=That(3.0++) taal dezelfde functionaliteiten heeft bewijs ik dat This=That(3.0++) ook turing compleet is.

|Brainfuck|Actie|This=That(3.0++)|Toelichting|
|---|---|---|---|
|`<` `>`|Verander de pointer.|`x = `*`val`*|Vind de `x` variable en wijs `x` de waarde *`val`* toe.|
|`+`|Verhoog de waarde van de pointer met 1.|`x = x plus 1`|Wijs `x` de waarde van `x` plus `1` toe.|
|`-`|Verlaag de waarde van de pointer met 1.|`x = x minus 1`|Wijs `x` de waarde van `x` min `1` toe.|
|`.`|Output de waarde van de pointer.|`x = print`|Output de waarde van `x`.|
|`,`|Ontvang input en geef de pointer die waarde.|`x = input`|Geef `x` de waarde van input.|
|`[` `]`| Conditionele loop.|`while l = x ~~ 0` `end while l`|Loop zolang `x` gelijk is aan `0`.|

### Optional To-Do's
- Add arrays
- Remove need for second `x` in self assignment Ex: `x = minus 2`
- Add For loops

## Taal ondersteunt

## Bevat

## Interpreter-functionaliteit Must-have

## Interpreter-functionaliteit Should-/Could-have