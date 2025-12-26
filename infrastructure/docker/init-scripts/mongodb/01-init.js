// Switch to ai_marketplace database
db = db.getSiblingDB('ai_marketplace');

// Create collections with validation
db.createCollection('models', {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["model_id", "owner_id", "name", "status"],
            properties: {
                model_id: { bsonType: "string" },
                owner_id: { bsonType: "string" },
                name: { bsonType: "string" },
                status: { enum: ["draft", "published", "deprecated"] }
            }
        }
    }
});

db.createCollection('model_reviews');
db.createCollection('inference_cache');

// Create indexes
db.models.createIndex({ "model_id": 1 }, { unique: true });
db.models.createIndex({ "owner_id": 1 });
db.models.createIndex({ "status": 1 });
db.models.createIndex({ "tags": 1 });
db.models.createIndex({ "created_at": -1 });

db.model_reviews.createIndex({ "model_id": 1 });
db.model_reviews.createIndex({ "user_id": 1 });

db.inference_cache.createIndex({ "request_hash": 1 }, { unique: true });
db.inference_cache.createIndex({ "ttl": 1 }, { expireAfterSeconds: 0 });

print('MongoDB initialized successfully');