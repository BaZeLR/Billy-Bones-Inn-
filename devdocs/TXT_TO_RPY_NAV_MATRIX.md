# TXT -> RPY Navigation Matrix

Scope: world/navigation labels. Source-of-truth: `game/Inn/*.txt` (`Location: "..."` + `act ... gt ...`).

| Location | TXT Source | RPY Entry Label | Exits (TXT) | Active/Inactive Rule (TXT) | Media/BG Policy |
|---|---|---|---|---|---|
| TavernMain | `TavernMain.txt` | `TavernMain` | `StreetTavern`, `TavernGloryHole`*, `TavernHelp`, `TavernMyRoom`, `TavernAmandaRoom`*, `TavernStable` | Closed text on Sunday morning, Friday dance slot, late night | `bg TavernMain` + `TavernShowImage` |
| TavernMyRoom | `TavernMyRoom.txt` | `TavernMyRoom` | `TavernMain` | Always | `bg myroom` |
| TavernAmandaRoom | `TavernAmandaRoom.txt` | `TavernAmandaRoom` | `TavernMain` | Content varies by `time` | `bg amanda_room` + Amanda room images |
| TavernStable | `TavernStable.txt` | `TavernStable` | `TavernMain`, `SherwoodTravel`* | Travel actions gated by quest/horse/time | `bg stable` + stable media |
| TavernGloryHole | `TavernGloryHole.txt` | `TavernGloryHole` | `TavernMain` | Exists only when built (`TavernGloryHole >= 2`) | Gloryhole event media |
| TavernHelp | `TavernHelp.txt` | `TavernHelp` | `TavernMain` | Always | `bg book` |
| StreetTavern | `StreetTavern.txt` | `StreetTavern` | `TavernMain`, `MarketPlace`, `PortStreets`, `Church`, `ArtisansQuarter` | Always | `bg StreetTavern` + `LocStreetTavern*` |
| MarketPlace | `MarketPlace.txt` | `MarketPlace` | `GroceryStore`, `WineStore`, `CityGuard`, `BeckyHomeFront`*, `StreetTavern` | Closed Sunday or late; Friday dance redirect | `LocMarketPlace*` |
| GroceryStore | `GroceryStore.txt` | `GroceryStore` | `MarketPlace` | Closed Sunday or late (`time >= 3`) | Eddie/Becky portraits |
| WineStore | `WineStore.txt` | `WineStore` | `MarketPlace` | Closed Sunday or late (`time >= 3`) | Clara/Alber portraits |
| Church | `Church.txt` | `Church` | `ChurchIspoved(1)`, `ChurchAfterCermon(1)`, `StreetTavern` | Open only Sunday service slots | Church open/closed images |
| ChurchAfterCermon | `ChurchAfterCermon.txt` | `ChurchAfterCermon(entry_arg=0)` | `Church` | Valid only when `entry_arg == 1` | Event-driven |
| ChurchIspoved | `ChurchIspoved.txt` | `ChurchIspoved(entry_arg=0)` | `Church` (via `AdvanceTime`) | Valid only when `entry_arg == 1` | Gerhard image |
| EllonaTemple | `EllonaTemple.txt` | `EllonaTemple` | `PortStreets` | Always, inner options by `FranBusy[time]` | `ellona` sequence |
| PortStreets | `PortStreets.txt` | `PortStreets` | `EllonaTemple`, `StreetTavern`, `StreetClients`* | Always, branch-heavy by NPC state/time | Port event images |
| ArtisansQuarter | `ArtisansQuarter.txt` | `ArtisansQuarter` | `StolyarWorkshop`, `DressShop`, `StreetTavern` | Always | `bg ArtisansQuarter` + `LocArtisansQuarter*` |
| StolyarWorkshop | `StolyarWorkshop.txt` | `StolyarWorkshop` | `ArtisansQuarter` | Closed Sunday/late and while active order in progress | `bg StolyarWorkshop` |
| DressShop | `DressShop.txt` | `DressShop` | `ArtisansQuarter` | Closed Sunday/late | Irma portraits/media |
| SherwoodTravel | `SherwoodTravel.txt` | `SherwoodTravel` | `TavernMain` path returns | Entry only via stable travel branch | Robin/media sequence |
| BeckyHomeFront | `BeckyHomeFront.txt` | `becky_home_front` | `BeckyHome`, `StreetTavern` | Branches by `ArriveMode` + random checks | Becky front media |
| BeckyHome | `BeckyHome.txt` | `becky_home` | `StreetTavern` | Access by relationship/arrival conditions | Becky home media |
| CityGuard | `CityGuard.txt` | `city_guard` | `MarketPlace` | Open only Tue day or Fri morning | Guard/Zimmer visuals |
| FridayDance | `FridayDance.txt` | `friday_dance` | `StreetTavern` | Valid only Friday evening conditions | Dance event visuals |

\* conditional route/action.

## Alias Resolution

Canonical gameplay location names remain original (TXT names): `TavernMain`, `StreetTavern`, `MarketPlace`, etc.

Compatibility aliases supported:
- `street_tavern -> StreetTavern`
- `market_place -> MarketPlace`
- `marketplace -> MarketPlace`
- `port_streets -> PortStreets`
- `artisans_quarter -> ArtisansQuarter`
- `city_guard -> CityGuard`
- `friday_dance -> FridayDance`
- `becky_home_front -> BeckyHomeFront`
- `becky_home -> BeckyHome`
