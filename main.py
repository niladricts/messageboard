# This is a main script to handle created messages and display them

from flask import Flask, request, render_template
import validators
import json
from bson import json_util
import xml.etree.ElementTree as eL
from pymongo import MongoClient
import os

try:
    conn = MongoClient('mongodb://localhost:27017')
    print("Database Connection Successful!")
except ConnectionError as eL:
    print("Connection unsuccessful {}".format(eL))

db = conn['sample_db']
get_table = db.get_collection("message_table")
if get_table is None:
    db.create_collection("message_table")


msgapp = Flask(__name__, template_folder='templates')

key = os.urandom(24)
msgapp.secret_key = key


def insert_message(title, message, sender, url):
    """
    This function will create message based on the input field values
    returns the original message if all input fields are correct
    """

    data1 = {"title": title,
             "message": message,
             "sender": sender,
             "url": url

             }
    print(data1)
    insert_data = db.get_collection('message_table')
    insert_data.insert_one(data1)
    return data1


@msgapp.route('/')
def index():
    """
    To return default page
    
    """
    return render_template('create.html')


@msgapp.route('/create', methods=['POST'])
def create_message():
    """
    function to send message
    returns okay message after input validation and message sending
    """
    if request.method == 'POST':
        title = request.form['title'].strip();
        message = request.form['message'].strip();
        sender = request.form['sender'].strip();
        url = request.form['url'].strip();
        if validators.url(url):
            print("URL {0} is okay".format(url))
        else:
            print("Bad URL {0}".format(url))
            exit(0)
        created_data = insert_message(title, message, sender, url)
        return "Message has been sent!"
    else:
        return render_template('create.html')


@msgapp.route('/list', methods=['GET'])
def list_message():
    """
    This function will return the list of messages in normal text format. It will List all the fields

    """

    msg_total = []
    get_data = db.get_collection('message_table')
    msg_details = get_data.find({}, {"title": 1, "message": 1, "sender": 1})
    if msg_details:
        for m in msg_details:
            print(m)
            msg_total.append(m)
        return json.dumps(msg_total, default=json_util.default)
    else:
        return "No message available"


@msgapp.route('/list/json', methods=['GET'])
def list_message_json():
    """
        This function will return the list of messages in json format. It will return all the fields except url

        """
    msg_json = []
    get_data_json = db.get_collection('message_table')
    msg_details_json = get_data_json.find({}, {"title": 1, "message": 1, "sender": 1, "url": 1})
    if msg_details_json:
        for m in msg_details_json:
            print(m)
            msg_json.append(m)
        return json.dumps(msg_json, default=json_util.default)
    else:
        return "No message available"


@msgapp.route('/list/xml', methods=['GET'])
def list_message_xml():
    """
        This function will return the list of messages in xml format. It has two versions. It will return all the fields  except url

        """
    msg_list = []
    get_data_xml = db.get_collection('message_table')
    msg_details_xml = get_data_xml.find({}, {"title": 1, "message": 1, "sender": 1, "url": 1})
    if msg_details_xml:
        for m in msg_details_xml:
            print(m)
            msg_list.append(m)
    try:
        msg_root = eL.Element("messageblock")
        for m in range(len(msg_list)):
            ms = eL.SubElement(msg_root, "ms")
            ms.text = str(msg_list[m])

        tree = eL.ElementTree(msg_root)
    except ValueError as f:
        print("List has the following errors {}".format(f))

    # write the tree into an XML file
    try:
        tree.write("message.xml", encoding='utf-8', xml_declaration=True)
        return "XML created in local"
    except FileNotFoundError as y:
        return "File creation error"


if __name__ == "__main__":
    msgapp.run(debug=True)
