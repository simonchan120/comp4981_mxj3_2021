import { StyleSheet, View, SafeAreaView, Image } from 'react-native';
import React, { useState, useCallback, useEffect, useContext } from 'react'
import { GiftedChat, Bubble } from 'react-native-gifted-chat'

import ActivitiesScreen from "./ActivitiesScreen";

import Constants from "expo-constants";
import {Auth} from "./App"

const ChatScreen = () => {
  const [messages, setMessages] = useState([]);
  /*interface Reply {
    title: string
    value: string
    messageId?: any
  }

  interface QuickReplies {
    type: 'radio' | 'checkbox'
    values: Reply[]
    keepIt?: boolean
  }*/

  const start_message_list = [
    {
      _id: 1,
      text: 'Welcome to Unpacking Happiness :)',
      createdAt: new Date(),
      user: {
        _id: 2,
        name: 'Unpacker',
      },
    },
    {
      _id: 2,
      text: 'Shall we start with a quick little test?',
      createdAt: new Date(),
      quickReplies: {
        type: 'radio', // or 'checkbox',
        keepIt: false,
        values: [
          {
            title: '😛 Sure~',
            value: 'Sure~',
          },
          {
            title: '🤔 What is it about?',
            value: 'What is it about?',
          },
        ],
      },
      user: {
        _id: 2,
        name: 'Unpacker',
      },
    }

  ]

  var num_chat = start_message_list.length;

  const reply_message_list = [
    {
      _id: 4,
      text: 'Great! Now let\'s prepare a piece of paper and a pen, and start drawing a house!',
      image: 'https://facebook.github.io/react/img/logo_og.png',
      createdAt: new Date(),
      user: {
        _id: 2,
        name: 'Unpacker',
      },
    },
    {
      _id: 4,
      text: 'What we are starting with is a super simiplifed version of the House-Person-Tree test, a test widely used by clinical psychologist to find out your personality 🧐 Why not start with preparing a piece of paper and a pen, and try to draw a house?',
      createdAt: new Date(),
      user: {
        _id: 2,
        name: 'Unpacker',
      },
    }
  ]

  useEffect(() => {
    setMessages([
      start_message_list[0],
    ]);
    setMessages(previousMessages => GiftedChat.append(previousMessages, start_message_list[1]));
  }, [])

  const context = useContext(Auth);
  /* This part is for API */
  const [isLoading, setLoading] = useState(true);
  const [data, setData] = useState([]);
  const { manifest } = Constants;
  const uri = `http://${manifest.debuggerHost.split(':').shift()}:5000/`;
  var send_text, replied_text;
  const getReplies = async () => {
    console.log("Context: ",context.token);
    let formData = new FormData();
    formData.append('message', send_text);
    try {
      const response = await fetch(uri, {
        method: 'POST',
        headers: {
          'Content-Type': 'multipart/form-data',
          'rasa-access-token': context.token
        },
        body: formData
      });
      const json = await response.json();
      console.log("JSON?", Array.isArray(json));
      if (!Array.isArray(json)){
        console.log(replied_text == null);
        return ;
      }
      replied_text = json[0].text;
      //console.log(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
      console.log("Loading set false");
      if (replied_text == null) {
        return ;
      }
      const rasa_replied_msg = [{
        _id: num_chat + 1,
        text: replied_text,
        createdAt: new Date(),
        user: {
          _id: 2,
          name: 'Unpacker',
        },
      }]
      setMessages(previousMessages => GiftedChat.append(previousMessages, rasa_replied_msg[0]));
      num_chat++;
    }
  }
  /* End */


  const onSend = useCallback((messages = []) => {
    setMessages(previousMessages => GiftedChat.append(previousMessages, messages));
    num_chat++;
    ///
    console.log(typeof messages[0].text);
    send_text = messages[0].text;
    getReplies();
  }, [])


  const onQuickReply = useCallback((quickReply) => {
    /*if(quickReply[0].value == "yes") {
    } else if (quickReply[0].value == "yes_picture") {
    } else if (quickReply[0].value == "NO") {
    }*/
    
    let message = quickReply[0].value;
    let msg = {
      _id: num_chat + 1,
      text: message,
      createdAt: new Date(),
      user: {
        _id:1
      }
    }
    setMessages(previousMessages => GiftedChat.append(previousMessages, msg));
    num_chat++;
    if (quickReply[0].value == 'Sure~') {
      setMessages(previousMessages => GiftedChat.append(previousMessages, reply_message_list[0]));
    } else {
      setMessages(previousMessages => GiftedChat.append(previousMessages, reply_message_list[1]));
    }
    num_chat++;



    /*var sendBotResponsetxt = "Thanks";
    this.sendBotResponse(sendBotResponsetxt);*/
  }, [])

  /*const chatHeight = ph(70);
  const chatWeight = pw(90);
  const actHeight = ph(20);
  const actWeight = pw(90);*/

  return (
    <SafeAreaView style={{ flex: 1 }}>
      <View style={style.chat}>
        <GiftedChat
          messages={messages}
          renderBubble={props => {
            return (
              <Bubble
                {...props}
                textStyle={{
                  left: {
                    color: 'white',
                  },
                  right: {
                    color: 'white',
                  },
                }}
                wrapperStyle={{
                  left: {
                    backgroundColor: 'green',
                  },
                  right: {
                    backgroundColor: 'orange',
                  },
                }}
              />
            );
          }}
          onSend={messages => onSend(messages)}
          onQuickReply={quickReply => onQuickReply(quickReply)}
          user={{
            _id: 1,
          }}
          renderMessageImage= {(props) => {
            return (
              <View
                style={{
                  borderRadius: 15,
                  padding: 2,
                }}
              >
                <Image
                  resizeMode="contain"
                  style={{
                    width: 200,
                    height: 200,
                    padding: 6,
                    borderRadius: 15,
                    resizeMode: "cover",
                  }}
                  source={require('./Image/giphy.gif')}
                />
              </View>
            );
          }}
        />
      </View>
      <View style={style.act}>
        <ActivitiesScreen/>
      </View>
    </SafeAreaView>
  )
}

const width_proportion = '100%';
const height_proportion_chat = '85%';
const height_proportion_act = '65%';
const style = StyleSheet.create({

  chat: {
    width: width_proportion,
    height: height_proportion_chat,
    /*alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#B8D2EC',*/
  },
  act: {
    width: width_proportion,
    height: height_proportion_act,
    /*alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#B8D2EC',*/
  },
});

export default ChatScreen;