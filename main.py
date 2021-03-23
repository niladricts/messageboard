# This is a main script to handle created messages and display them

from flask import Flask, request, redirect, render_template, session, flash
from collections import namedtuple
import os
import validators
import json
import xml.etree.ElementTree as e




messages = namedtuple('messages',['title','message','sender'])
messages1 = namedtuple('messages1',['title','message','sender','url'])

msg = [] #empty list
msg1 = [] #empty second list
maxlength = 10

msgapp = Flask(__name__, template_folder='templates')
import os
key = os.urandom(24)
msgapp.secret_key = key


def insert_message(title,message,sender,url):
    '''
    This function will create message based on the input field values
    returns the original message if all input fields are correct
    '''
    global msg,msg1
    if message:
        if len(msg) >= maxlength:
           print("Maximum Length Exceeded")
           msg.clear()
    data = messages(title,message,sender);
    data1 = messages1(title,message,sender,url);
    msg.append(data)
    msg1.append(data1)
    return data

@msgapp.route('/')
def index():
    """
    To return default page
    
    """
    return render_template('create.html')
@msgapp.route('/create',methods=['POST'])
def create_message():
    '''
    function to send message
    returns okay message after input validation and message sending
    '''
    if request.method == 'POST':
        title = request.form['title'].strip();
        message = request.form['message'].strip();
        sender = request.form['sender'].strip();
        url = request.form['url'].strip();
        if validators.url(url) == True:
            print("URL {0} is okay".format(url))
        else:
             print("Bad URL {0}".format(url))
             exit(0)
        created_data = insert_message(title,message,sender,url)
        return "Message has been sent!"
    else:
          return render_template('create.html')


@msgapp.route('/list',methods=['GET'])
def list_message():
    """
    This function will return the list of messages in normal text format. It will List all the fields

    """

    global msg


    return '%d messages: %s' % (len(msg),",\n".join(','.join(m) for m in msg))

@msgapp.route('/list/json',methods=['GET'])
def list_message_json():
    """
        This function will return the list of messages in json format. It will return all the fields except url

        """

    global msg1
    if msg1:
       return json.dumps(msg1)

@msgapp.route('/list/xml',methods=['GET'])
def list_message_xml():
    """
        This function will return the list of messages in xml format. It has two versions. It will return all the fields  except url

        """

    global msg1
    try:
        msg_root = e.Element("messageblock")
        for m in range(len(msg1)):
            ms = e.SubElement(msg_root, "ms")
            ms.text = str(msg1[m])

        tree = e.ElementTree(msg_root)
    except ValueError as e:
           print("List has the following errors {e}".format(e))

    # write the tree into an XML file
    try:
        tree.write("message.xml", encoding='utf-8', xml_declaration=True)
        return "XML created in local"
    except Exception:
           return "File creation error"
if __name__ == "__main__":
    msgapp.run(debug=True)