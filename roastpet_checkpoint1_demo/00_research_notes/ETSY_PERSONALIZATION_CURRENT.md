# Etsy personalization model used by this fixture

Current Etsy custom options allow up to five personalization fields. Supported field types are:
text input, dropdown, and a single file-upload question. File upload can accept up to ten files.

For roast.pet, use **one labeled upload field with four required labels**. This is better than an unlabeled
'upload whatever you have' field because our downstream avatar pipeline benefits from predictable coverage:

1. Front face
2. Full body
3. Side view
4. Favourite extra

The listing itself should define the visual product template. Do not burn a personalization field asking
customers to choose among many card themes. On Etsy, variations are the right primitive when a choice changes
price, inventory, processing profile, or SKU. Personalization is for buyer-specific content.

Recommended V1: one listing = one clear visual concept ("Comedy Club Roast"). Later create separate listings
for "Breaking News", "Awards Roast", etc., all backed by the same Pog/FreakTown pipeline.

Photo guidance should be operational, not aesthetic:
- same pet in every photo
- natural or even light
- face and eyes visible
- full ears/head visible in front-face image
- at least one full-body image
- one side view
- no beauty filters / stickers
- avoid costumes covering body shape
- original image preferred over screenshot

Etsy cannot guarantee our desired quality merely because the upload field is required. The post-order intake
validator must score each file and request replacement only when the minimum identity/geometry evidence is absent.
