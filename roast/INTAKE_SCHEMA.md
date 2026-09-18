# Roast Intake Schema

## Pet Info
- pet_name: string
- pet_species: string (dog/cat/other)
- pet_breed: string
- pet_photos: array[3-8] (uploaded)
- pet_personality: string (1-3 lines)

## Recipient Info
- recipient_name: string
- recipient_relationship: string (dad/boyfriend/friend/sister)
- recipient_age: string (turning 30, 50th birthday, etc)

## Roast Material
- funny_facts: array[3-10] (stories about recipient)
- tone: enum (light_cheeky, funny_cheeky, savage_safe)
- custom_message: string (optional closing)

## Example RoastBrief
```json
{
  "pet": {"name": "Buster", "species": "dog", "breed": "dachshund", "personality": "chaotic, cheese-obsessed"},
  "recipient": {"name": "James", "relationship": "dad", "occasion": "50th birthday"},
  "roast_material": ["supports Arsenal", "thinks he's good at golf", "snores loudly"],
  "tone": "funny and cheeky",
  "custom_message": "Happy birthday from Sophie and Buster"
}
```
