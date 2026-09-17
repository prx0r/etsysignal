# Etsy API Quick Reference

## Rate Limits
- QPS: 150/sec
- QPD: 100,000/day (sliding window)
- Exceeded: 429 with retry-after

## Auth
```
Header: x-api-key: {API_KEY}:{SHARED_SECRET}
```

## Key Endpoints
```
GET  /v3/application/listings/active?keywords=...    # Search
GET  /v3/application/listings/{listing_id}           # Get listing
POST /v3/application/listings/{shop_id}              # Create listing
GET  /v3/application/shops/{shop_id}                 # Get shop
```

## Optimization
- Cache responses
- Handle 429 with exponential backoff
- Use retry-after header
