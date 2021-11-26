import { StatusBar } from 'expo-status-bar';
//import React from 'react';
import { StyleSheet, Text, View } from 'react-native';

/*export default function App() {
  return (
    <View style={styles.container}>
      <Text>Open up App.js to start working on your app!</Text>
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});*/

import React, { useState, useCallback, useEffect } from 'react'
import { GiftedChat, Bubble } from 'react-native-gifted-chat'

export default function App() {
  
  
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

  

  const onSend = useCallback((messages = []) => {
    setMessages(previousMessages => GiftedChat.append(previousMessages, messages));
    num_chat++;

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
  )
}
