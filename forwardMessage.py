import paho.mqtt.client as mqtt

# broker ip address
broker_ip = "172.20.0.2"
# cloud ip address
cloud_ip = "169.59.1.50"

# define the topic and QoS -- QoS 0 is fine, most minimal implementation
# and no risk if data is lost
topic_sub = "faces"
qos_level = 0

# action to perform when connection occurs
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe(topic_sub)
    print("connected: ", not bool(rc))

# action to perform when data is published
def on_publish(client, userdata, result):
    print("data published \n")

# action to perform when a subscribed message comes through
def on_message(client, userdata, message):
    print("message received ")
    print("topic: ",message.topic)
    print("qos: ",message.qos)

    # extract the message content and topic and immediately publish to
    # the cloud
    msg = message.payload
    topic_pub = message.topic
    cloud_pub.publish(topic_pub, msg, qos=qos_level, retain=False)

# Initialize the cloud publisher
cloud_pub = mqtt.Client("cloudPub")
cloud_pub.on_message = on_message
cloud_pub.on_publish = on_publish

# Connect to cloud broker and keep connection alive
cloud_pub.connect(cloud_ip, keepalive=1200)

# Initialize the client for subscribing to internal broker
broker_sub = mqtt.Client("brokerSub")
broker_sub.on_connect = on_connect
broker_sub.on_publish = on_publish
broker_sub.on_message = on_message

# Connect to local broker
broker_sub.connect(broker_ip)

# run forever
broker_sub.loop_forever()
