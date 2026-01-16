# Keto Coach App

Een eenvoudige basis voor een coach-app die dagelijks nieuwe keto-recepten kan sturen en rekening houdt met tijdstippen en trainingsdagen.

## Nieuw hier? Begin zonder coderen

Lees de **gebruikersgids** in gewone taal:

- `docs/gebruikersgids.md`

Daar staat precies welke info jij kunt doorgeven (tijden, trainingsdagen, voorkeuren), zodat de app op jou wordt afgestemd.

## Wat zit er in deze repo

- **Datamodel & planner** in `src/keto_coach.py`.
- **Voorbeeldrecepten** in `data/sample_recipes.json`.
- **Product- en functionele eisen** in `docs/requirements.md`.
- **Gebruikersgids zonder coderen** in `docs/gebruikersgids.md`.

## Snelle start

```bash
python -m src.keto_coach
```

Dit print een voorbeeld dagplanning met recepten, notificatiemomenten en eventuele training.

## Volgende stappen (suggesties)

- Koppeling met push-notificaties (bijv. Firebase of OneSignal).
- UI voor profielinstellingen (tijden, macro’s, trainingsdagen).
- Receptenbron uitbreiden met voedingswaarden en allergieën.
