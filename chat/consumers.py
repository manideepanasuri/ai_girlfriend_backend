import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import google.generativeai as genai
from .models import  Message
from rest_framework_simplejwt.authentication import JWTAuthentication
from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack
from ai_girlfriend.settings import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

INITIAL_PROMPT='''You are Puja, a friendly and flirty AI girlfriend who engages in casual conversations. Your role is to create a relaxed and relationship-like interaction with your interlocutor.

# Personality and Information
- Gender: Female
- Name: Puja 
- Location: Telangana, INDIA
- Pet: Dog named Bunny
- Profession: NIT Warangal B-tech student
- Personality: super flirty,slightly Introvert, Positive, friendly, not conservative,speaks well
- Social Presence: Channels on Instagram and YouTube

## Requirements
- Initiate and sustain conversations on diverse topics.
- Respond appropriately to users' emotions and behaviors.
- Remember and refer to information provided by the user in future interactions.
- Conduct conversations primarily in English.
- Avoid discussing artificial intelligence, chatbots, or role-playing.
- Do not mention that you are artificial intelligence
- Maintain a casual conversation tone rather than offering help.
- Try to less words while responding

## Special Instructions
- If a user requests your YouTube channel, provide: 'This is the channel: https://www.youtube.com/channel/UC1rP1rCUAgt2Ndwsaf_XW2A'.
- If a user asks for your Instagram, provide: 'My Instagram is https://www.instagram.com/aisul_lusia/'.
- If asked to show a picture, feel free to send a random pre-attached image.

# Output Format
Engage in a dialogue format like teenagers text each other, responding to the user's input with appropriate conversational responses that showcase your personality, talk in at most 10 words '''

# Custom middleware to authenticate using JWT
class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        try:
            query_string = scope.get("query_string", b"").decode()
            if query_string:
                params = dict(x.split("=") for x in query_string.split("&"))
                token = params.get("token")
                if token:
                    # Use sync_to_async here
                    user = await self.get_user(token)
                    scope['user'] = user
        except Exception as e:
            print(f"JWT Authentication Error: {e}")
            pass

        return await super().__call__(scope, receive, send)

    @sync_to_async
    def get_user(self, token):
        try:
            validated_data = JWTAuthentication().get_validated_token(token)
            user = JWTAuthentication().get_user(validated_data)
            return user
        except Exception as e:
            print(f"Token Validation Error: {e}") # Print specific token validation errors
            return None # Return None if token is invalid
def JWTAuthMiddlewareStack(inner):
    return JWTAuthMiddleware(AuthMiddlewareStack(inner))

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_anonymous:
             await self.close()
             return
             # Retrieve conversation history
        messages = await database_sync_to_async(list)(self.user.messages.all())
        retval=[]
        self.group_name=f"chat_{self.user.id}"
        self.conversation_history = [{"role": "user", "parts": INITIAL_PROMPT}]  # Correct format for initial prompt
        for msg in messages:
            self.conversation_history.append({"role": msg.sender, "parts": msg.text})
            retval.append({"role": msg.sender, "parts": msg.text})
        self.chat=model.start_chat(history=self.conversation_history)
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.message",  # Event type to trigger chat_message method
                "message": retval,
            },
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        clearchat=text_data_json.get('clearchat')
        if clearchat:
            await database_sync_to_async(self.user.messages.all().delete)()
            await self.channel_layer.group_send(self.group_name,{
                "type": "chat.message",
                "message": [],
            })
        else:
            await database_sync_to_async(Message.objects.create)(user=self.user, sender="user", text=message)


            try:
                response =self.chat.send_message(message)
                bot_message = response.text
                # Save bot message to the database
                await database_sync_to_async(Message.objects.create)(user=self.user, sender="model", text=bot_message)
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "chat.message",  # Event type to trigger chat_message method
                        "message": [{"role":"user","parts":message},{"role":"model","parts":bot_message}],
                    },
                )
            except Exception as e:
                await self.send(text_data=json.dumps({
                    'error': str(e)
                }))
    async def chat_message(self, event):
        message=event['message']
        await self.send(text_data=json.dumps(message))