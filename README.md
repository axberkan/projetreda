# projetreda

## User Story

Titre : Refroidissement du réacteur par vanne TOR

En tant que opérateur de conduite d’un réacteur chimique,
Je veux que la température du réacteur soit surveillée et que la vanne de refroidissement s’ouvre ou se ferme automatiquement,
Afin de maintenir la température dans une plage de sécurité et assurer la qualité du produit.

## Critères d’acceptation
Capteur :

Une sonde de température (PT100) mesure en continu la température du réacteur.

La mesure est transmise au système de contrôle (API / DCS).

Actionneur (TOR) :

La vanne motorisée de refroidissement a seulement deux états : OUVERTE (1) ou FERMÉE (0).

Si la température dépasse 250 °C, la vanne s’ouvre pour permettre le refroidissement.

Si la température descend sous  250°C, la vanne se ferme pour éviter un sur-refroidissement.

Si la sonde est défaillante, une alarme est générée et la vanne se met en position de sécurité (ouverte).

## Comportement attendu

T° > 200 °C → la vanne s’ouvre (refroidissement actif).

T° < 200 °C → la vanne se ferme (refroidissement coupé).


On y affichera le debit calorifique qui est nécéssaire dans le milieur chimique afin de garder un oeil sur nos échange de chaleurs. 