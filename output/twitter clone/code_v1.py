from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from uuid import uuid4

app = FastAPI()

class Tweet(BaseModel):
    author: str
    content: str

tweets: Dict[str, Tweet] = {}

@app.get("/tweets", response_model=List[Tweet])
async def get_all_tweets():
    return list(tweets.values())

@app.get("/tweets/{tweet_id}", response_model=Tweet)
async def get_tweet(tweet_id: str):
    if tweet_id not in tweets:
        raise HTTPException(status_code=404, detail="Tweet not found")
    return tweets[tweet_id]

@app.post("/tweets", response_model=str)
async def create_tweet(tweet: Tweet):
    tweet_id = str(uuid4())
    tweets[tweet_id] = tweet
    return tweet_id

@app.put("/tweets/{tweet_id}", response_model=Tweet)
async def update_tweet(tweet_id: str, updated_tweet: Tweet):
    if tweet_id not in tweets:
        raise HTTPException(status_code=404, detail="Tweet not found")
    tweets[tweet_id] = updated_tweet
    return updated_tweet

@app.delete("/tweets/{tweet_id}", response_model=str)
async def delete_tweet(tweet_id: str):
    if tweet_id not in tweets:
        raise HTTPException(status_code=404, detail="Tweet not found")
    del tweets[tweet_id]
    return f"Deleted tweet with ID {tweet_id}"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)