// React Native Bottom Navigation
// https://aboutreact.com/react-native-bottom-navigation/
//import * as React from 'react';
import { View, Text, SafeAreaView, Dimensions } from 'react-native';

/*const DetailsScreen = () => {
  return (
    <SafeAreaView style={{ flex: 1 }}>
      <View style={{ flex: 1 , padding: 16}}>
        <View
          style={{
            flex: 1,
            alignItems: 'center',
            justifyContent: 'center',
          }}>
          <Text
            style={{
              fontSize: 25,
              textAlign: 'center',
              marginBottom: 16
            }}>
            You are on Details Screen
          </Text>
        </View>
        <Text
          style={{
            fontSize: 18,
            textAlign: 'center',
            color: 'grey'
          }}>
          React Native Bottom Navigation
        </Text>
        <Text
          style={{
            fontSize: 16,
            textAlign: 'center',
            color: 'grey'
          }}>
          www.aboutreact.com
        </Text>
      </View>
    </SafeAreaView>
  );
}*/
import React, { useState, useCallback, useEffect } from 'react'
import { GiftedChat, Bubble } from 'react-native-gifted-chat'

import ActivitiesScreen from "./ActivitiesScreen";

/*** For API ***/
//import React, { useEffect, useState } from 'react';
//import { ActivityIndicator, FlatList, Text, View } from 'react-native';
import Constants from "expo-constants";

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


  /* This part is for API */
  const [isLoading, setLoading] = useState(true);
  const [data, setData] = useState([]);
  const { manifest } = Constants;
  const uri = `http://${manifest.debuggerHost.split(':').shift()}:5005/webhooks/rest/webhook/`;
  var send_text, replied_text;
  const getReplies = async () => {
    try {
      const response = await fetch(uri, {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          sender: 'test_user',
          message: send_text
        })
      });
      const json = await response.json();
      console.log(typeof json[0].text);
      replied_text = json[0].text;
      //console.log(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
      console.log("Loading set false");
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



  return (
    <SafeAreaView style={{ flex: 1 }}>
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
      />
      
      <ActivitiesScreen/>
        
    </SafeAreaView>
  )
}


export default ChatScreen;