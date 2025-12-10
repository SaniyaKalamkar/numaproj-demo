import asyncio
import sys
from aiomqtt import Client

async def publish_message(broker, port, topic, message):
    """Publish a message to MQTT broker"""
    try:
        async with Client(broker, port) as client:
            await client.publish(topic, message)
            print(f"✅ Published to {topic}: {message}")
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Make sure MQTT broker is running on {broker}:{port}")

if __name__ == "__main__":
    # Get parameters from command line or use defaults
    broker = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 1883
    topic = sys.argv[3] if len(sys.argv) > 3 else "test"
    message = sys.argv[4] if len(sys.argv) > 4 else "Hello from MQTT!"
    
    print(f"📤 Publishing to {broker}:{port}/{topic}")
    asyncio.run(publish_message(broker, port, topic, message))
