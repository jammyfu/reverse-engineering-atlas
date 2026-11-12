# Catalog ordering and discovery contract

- The five READMEs are generated from `data.json`, `descriptions.json`, `images.json`, `stars.json`, and the shared renderer. Edit sources, then run `python render.py` and `python validate.py`.
- Source platform determines the game category. A PC recompilation of a Switch game belongs to Switch, not PC. Switch 2 is explicitly prioritized editorially; no measured trending claim is implied.
- `stars.json` is an inherited cumulative snapshot without a recorded capture timestamp. Do not present it as live heat or invent a collection date. Missing values are unknown, not zero. Record source and timestamp before adding future trend claims.
- Each category/subcategory shows up to 15 entries, with the rest in a native GitHub disclosure. Nothing is removed. All languages share the same records and order.
- The hero is original editorial artwork. Existing catalog media remain source-labeled; neither a repository listing nor CC0 on this catalog grants rights to upstream code, game assets, cover art, ROMs or trademarks. Verify upstream terms before redistribution.
- The repository license applies to this catalog, not the software and media it links to. Project viability and legal usability must be checked at each original source.
- Clear titles, localized descriptions and stable anchors help readers and machine retrieval. They do not guarantee search rankings, AI citations or stars.

## Game identity and hardware labels (2026-11-12)

- `game-titles.json` promotes 28 already-described game identities into the project cell; it does not add new games, imply new releases, or create a popularity ranking. Original proper names are retained consistently across translations rather than inventing localized release names.
- All game rows have a local original hardware pictogram plus the source-platform text. They do not mean the project runs on that hardware; host OS requirements remain in the description. Generic icons are not official manufacturer logos.
- Switch 2 remains `explicit_user_priority` (user direction, observed this request on 2026-11-12 UTC; window/metric/value not applicable; heat_status unknown). Other categories retain the documented cumulative snapshot ordering. Group order is source-platform relevance then existing snapshot, with stable input order for ties; no new measured heat claim is made.
- The source of each game label is its existing catalog description and upstream project URL in `data.json`. Commercial game cover rights are independent of source code licenses. Do not fetch random box art or use an upstream placeholder as gameplay.
- Before using an image check README, asset directory, project license and media-specific restrictions. If redistribution/embedding permission is not established, keep the source link rather than copying or hotlinking. Do not add any upstream site to this atlas's About, hero destination or promotional slots.
