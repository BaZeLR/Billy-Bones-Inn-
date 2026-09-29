# Secret forest Sabbats and the Gerhardt–Franchesca rivalry

Status: **story notes only; the named Sabbats and this conspiracy arc are not implemented**. The existing `claraMoonSabbath` and Mongol guide show a generic full-moon gathering; neither selects or completes a named seasonal Sabbat. Picture sources exist outside the current mapped assets and have **not** been updated here. Preserve the working generic encounters until a distinct replacement/continuation is authored and tested.

## Place and calendar

- The parties occur **Saturday late evening** at a concealed place in the forest. The player must discover a way in through story clues and exploration; ordinary forest navigation must not expose a permanent party button from the start.
- The eight names, period associations and themes are in `devdocs/CalendarV2Blueprint.rpy`: Yule (1), Imbolc (2), Ostara (4), Beltane (5), Litha (7), Lughnasadh (9), Mabon (11), Samhain (13). They are seasonal variants of this hidden gathering, not eight simultaneously active parties.
- The draft's `day=7, week=4, 23:00` rows are **not** the schedule to copy: in the live 28-day calendar, day 7 is Sunday when period day 1 is Monday, while weekday 4 is Thursday. The live calendar owns exact time and lunar phase. Select an actual Saturday and late-evening hour for each named event before implementation; do not use descriptive time slots as schedule state. Whether each seasonal meeting also requires Full Moon is still to be resolved against the existing generic full-moon encounter.
- `ForestStoneCircle` appears in the old blueprint but is not a live room. Treat the concealed site and its approach as planned room/navigation work. The cave, spring, clearing and dark woods are possible surrounding approaches, **not** separate automatic Sabbat locations merely because the draft lists them.

## What is happening there

Affluent townspeople send adult virgin servants and protégées to the gatherings through the secret guidance of an Ellona priest. Others arrive by following forest legends or seeking an answer to the recurring virgin nightmares. Some guests are curious, some are being manipulated; these are different entry paths and must not become one generic consent or recruitment flag. The duchess's birth laws provide public cover for births, while rival powers pursue their own hidden ends.

Gerhardt is connected to the weregoat that hunts virgin energy. Franchesca, Ellona's highest priestess, is his rival for that energy. She seeks births for a force of superhumans in another, modern world, using a time-loop mechanism. The late reveal identifies her as Tempest and connects her to Steven Wolf being trapped in Coitus. This is also the explanation sought for the opening's displaced identity: **the man called Stephan is not simply the Stephan everyone assumes**. Keep the precise identity/memory mechanism a mystery until its authored reveal; do not overwrite the current player state with a second identity object.

The cave relic and the route to it are tracked in `legare_revenge_tempest_opening_plan.md`: after Becky's trade road is genuinely cleared of bandits, the Cunidail elves can reveal the hiding place of **Дилдон Ебунец**. That discovery is a later aid against Franchesca and toward escape, not a consequence of merely watching a Sabbat.

## Clue and reveal order

| Beat | What the player learns | Gate / presentation still needed |
| --- | --- | --- |
| Sunday first sign | MC overhears the strange word **“pioneers.”** It echoes the replacement opening and its identity anomaly, without explaining it yet. | Exact speaker, Sunday place, wording, and first eligible story stage are not supplied. This is an event, not ambient text repeated on every Sunday. |
| Priest connection | Gerhardt admits he knew Franchesca as Ellona's highest priestess. MC can ask **each** about the other after that discovery. | Distinct NPC talk options unlock from the same established discovery; retain each NPC's schedule and existing dialogue. |
| Competing accounts | Each tries to persuade MC that the other is the danger. The disagreement exposes their rivalry over virgin energy and makes either account suspect. | Separate Gerhardt and Franchesca conversations; no automatic truth flag from hearing only one side. |
| Gerhardt's weakness | Franchesca describes his medallion/amulet and a Latin proverb engraved on it. Solving that proverb reveals how to destroy the weregoat. | The visible chat mentions a Latin proverb on the medallion, but gives **neither its exact Latin wording nor its answer**. No project text supplies them. Do not invent either or make possession of the amulet alone win the fight. |
| Franchesca's weakness | Gerhardt calls her an exceptionally powerful witch who cannot be destroyed by ordinary force. He claims an overwhelming climax can weaken her, while insisting no one could bring that about. | His claim is a clue from a rival, not proof of the final combat mechanic or an instant-win action. The eventual solution, weapon and fight still need authored prerequisites. |
| Tempest reveal | MC connects the priestess, the birth scheme, the time loop, Steven Wolf and the identity anomaly from the opening. | Late arc after the existing cave-weapon and weregoat investigation gates; see `legare_revenge_tempest_opening_plan.md`. No mid-game restart or calendar reset. |

## Gerhardt's confession leverage (requested, not implemented)

Gerhardt becomes more forthcoming when MC first witnesses an eligible episode **and later tells him about it in confession**. Repeating the same report must not farm points. One-time subject weights: Georgette +1, Lizette +1, Becky +2, Pauline +1, Legare +1. The **completed entire** Draupnir repair list contributes **one** Gerhardt point, not one per pledge. Confession score belongs to Gerhardt's NPC/story state, while the observation belongs to the source event's completed/seen state. It must not be inferred from merely seeing a person at church.

Each of the ten *distinct* Draupnir pledges adds **five** to the tavern's usual daily attendance (ten pledges: **+50 directly**) and **one** to temporary tavern fame (`player.economy.tavern_fame`). Each five pledge-earned fame points should yield **one point for each current tavern worker's personal karma**, not a shared tavern-karma score. The live `Girl` object has `mana`, friendship, and corruption but no `karma` or `carma` field; identify the intended personal value before coding that bonus. The existing fame-to-visitors conversion at fame 10 is a separate effect and may increase the eventual visitor total beyond the direct +50.

At **five** Gerhardt points, new conversation subjects unlock **beyond Becky/Rebecca**: his past with Franchesca and his account of the town ladies. His disclosures should foreshadow the rival Ellona priest's influence: the ladies may unknowingly further her plan through the servants under their care. The talks are narrative revelations, not proof that every individual woman understands or endorses that plan. Pauline and Legare reports need their own witnessed-event prerequisites before becoming confession options.

## Discovery and event ownership

The hidden path should emerge from converging evidence: forest traces, Clarissa's sketches/visits, Mongol's knowledge, and the priests' contradictory stories are **candidate clues**, not automatically completed steps. A playable design still needs exact evidence, discovery threshold, alternate route, failure/return, and whether any specific named Sabbat can be missed. Observing a gathering should not by itself identify Gerhardt or Franchesca, resolve virgin nightmares, or reveal the time loop.

When implemented, the calendar supplies date/hour/moon facts; the concealed forest room owns navigation and visibility; Gerhardt/Franchesca own their NPC talk state; event/thread objects own activation, advancement, completion and one-time versus recurring rules; event labels own scene text, image order and native choices. Do not add a parallel Sabbat calendar, duplicate global mystery flags, or overwrite the generic Clarissa/Mongol encounters as a shortcut.

## Still needed before code or illustrations

1. Exact eligible Saturday per seasonal period and whether Full Moon is compulsory; the old blueprint's Thursday/Sunday mixture is invalid.
2. Hidden site's visual identity and discoverable route, including an alternative to following Clarissa or Mongol.
3. Source-image inventory and mapping for approach, concealed site, each named gathering, and exits. None is claimed ready by this note.
4. The Sunday “pioneers” speaker and dialogue, both reciprocal priest conversations, the Latin proverb and answer, and evidence required for the Tempest/Steven identity reveal.
5. Consequences for guests and tavern characters, the weregoat fight, Franchesca's actual weakness, and how the late arc joins the existing cave-weapon plan without skipping its gates.
