import math
import json
import pika
from datetime import datetime

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))



def publish_geo_event(device_id, fence, event, lat, lon):
    message = {
        "device_id": device_id,
        "fence": fence,
        "event": event,
        "lat": lat,
        "lon": lon,
        "timestamp": datetime.utcnow().isoformat()
    }

    # RabbitMQ serverga ulanish (localhost da ishlayotgan bo‘lsa)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()

    # Queue mavjud bo‘lmasa, yaratadi
    channel.queue_declare(queue="geo-events", durable=True)

    # JSON xabar publish qilamiz
    channel.basic_publish(
        exchange="",
        routing_key="geo-events",
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # persistent
        )
    )
    connection.close()
    return message