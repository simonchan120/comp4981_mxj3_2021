import { StyleSheet, View, SafeAreaView, Image } from 'react-native';
import React, { useState, useCallback, useEffect, useContext } from 'react'
import { GiftedChat, Bubble, messageIdGenerator } from 'react-native-gifted-chat'

import ActivitiesScreen from "./ActivitiesScreen";

import Constants from "expo-constants";
import {Auth} from "./App"
//import Agreement from './Agreement';

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
      _id: 's1',
      text: 'Welcome to Unpacking Happiness :)',
      createdAt: new Date(),
      user: {
        _id: 2,
        name: 'Unpacker',
      },
    },
    {
      _id: 's2',
      text: 'Before we talk, I hope to understand you more~',
      createdAt: new Date(),
      user: {
        _id: 2,
        name: 'Unpacker',
      },
    },
    {
      _id: 's3',
      text: 'Shall we start with a quick little test?\nWhat we are starting with is a questionaire for understanding your current status. It just composes of a few questions, and it\'s you and me who will know this!\nNow I will give a list of situations. Over the last 2 weeks, how often have you been bothered by them?',
      createdAt: new Date(),
      /*quickReplies: {
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
      },*/
      user: {
        _id: 2,
        name: 'Unpacker',
      },
    }

  ]

  var num_chat = 0;

  const reply_message_list = [
    {
      _id: 'r1',
      text: 'Great! Now I will a list of questions. From a scale of 1 to 5, how much do they sound like describing you? ',
      createdAt: new Date(),
      user: {
        _id: 2,
        name: 'Unpacker',
      },
    },
    {
      _id: 'r2',
      text: 'What we are starting with is a questionaire for understanding your current status. It just composes of a few questions, and it\'s you and me who will know this!',
      createdAt: new Date(),
      user: {
        _id: 2,
        name: 'Unpacker',
      },
    }
  ]

  const back_message_list = [
    {
      _id: 'b1',
      text: 'Hello! Welcome back to Unpacking Hapiness :)',
      image: 'https://i.giphy.com/media/yKQTrPStO2CcgNWxuK/giphy.gif', //getting GIF from links
      createdAt: new Date(),
      user: {
        _id: 2,
        name: 'Unpacker',
      },
    }
  ]

  const survey_question_list = [
    {
      _id: 'q1',
      text: 'Little interest or pleasure in doing things',
      createdAt: new Date(),
      quickReplies: {
        type: 'radio', // or 'checkbox',
        keepIt: false,
        values: [
          {
            title: 'Not at all',
            value: 0,
          },
          {
            title: 'Several days',
            value: 1,
          },
          {
            title: 'More than half the days',
            value: 2,
          },
          {
            title: 'Nearly every day',
            value: 3,
          },
        ],
      },
      user: {
        _id: 2,
        name: 'Unpacker',
      },
    },
    {
      _id: 'q2',
      text: 'Feeling down, depressed, or hopeless',
      createdAt: new Date(),
      quickReplies: {
        type: 'radio', // or 'checkbox',
        keepIt: false,
        values: [
          {
            title: 'Not at all',
            value: 0,
          },
          {
            title: 'Several days',
            value: 1,
          },
          {
            title: 'More than half the days',
            value: 2,
          },
          {
            title: 'Nearly every day',
            value: 3,
          },
        ],
      },
      user: {
        _id: 2,
        name: 'Unpacker',
      },
    },
    {
      _id: 'q3',
      text: 'Trouble falling or staying asleep, or sleeping too much',
      createdAt: new Date(),
      quickReplies: {
        type: 'radio', // or 'checkbox',
        keepIt: false,
        values: [
          {
            title: 'Not at all',
            value: 0,
          },
          {
            title: 'Several days',
            value: 1,
          },
          {
            title: 'More than half the days',
            value: 2,
          },
          {
            title: 'Nearly every day',
            value: 3,
          },
        ],
      },
      user: {
        _id: 2,
        name: 'Unpacker',
      },
    },
    {
      _id: 'q4',
      text: 'Feeling tired or having little energy',
      createdAt: new Date(),
      quickReplies: {
        type: 'radio', // or 'checkbox',
        keepIt: false,
        values: [
          {
            title: 'Not at all',
            value: 0,
          },
          {
            title: 'Several days',
            value: 1,
          },
          {
            title: 'More than half the days',
            value: 2,
          },
          {
            title: 'Nearly every day',
            value: 3,
          },
        ],
      },
      user: {
        _id: 2,
        name: 'Unpacker',
      },
    },
    {
      _id: 'q5',
      text: 'Poor appetite or overeating',
      createdAt: new Date(),
      quickReplies: {
        type: 'radio', // or 'checkbox',
        keepIt: false,
        values: [
          {
            title: 'Not at all',
            value: 0,
          },
          {
            title: 'Several days',
            value: 1,
          },
          {
            title: 'More than half the days',
            value: 2,
          },
          {
            title: 'Nearly every day',
            value: 3,
          },
        ],
      },
      user: {
        _id: 2,
        name: 'Unpacker',
      },
    },
    {
      _id: 'q6',
      text: 'Feeling bad about yourself - or that you are a failure or have let yourself or your family down',
      createdAt: new Date(),
      quickReplies: {
        type: 'radio', // or 'checkbox',
        keepIt: false,
        values: [
          {
            title: 'Not at all',
            value: 0,
          },
          {
            title: 'Several days',
            value: 1,
          },
          {
            title: 'More than half the days',
            value: 2,
          },
          {
            title: 'Nearly every day',
            value: 3,
          },
        ],
      },
      user: {
        _id: 2,
        name: 'Unpacker',
      },
    },
    {
      _id: 'q7',
      text: 'Trouble concentrating on things, such as reading the newspaper or watching television',
      createdAt: new Date(),
      quickReplies: {
        type: 'radio', // or 'checkbox',
        keepIt: false,
        values: [
          {
            title: 'Not at all',
            value: 0,
          },
          {
            title: 'Several days',
            value: 1,
          },
          {
            title: 'More than half the days',
            value: 2,
          },
          {
            title: 'Nearly every day',
            value: 3,
          },
        ],
      },
      user: {
        _id: 2,
        name: 'Unpacker',
      },
    },
    {
      _id: 'q8',
      text: 'Moving or speaking so slowly that other people could have noticed? Or the opposite - being so fidgety or restless that you have been moving around a lot more than usual',
      createdAt: new Date(),
      quickReplies: {
        type: 'radio', // or 'checkbox',
        keepIt: false,
        values: [
          {
            title: 'Not at all',
            value: 0,
          },
          {
            title: 'Several days',
            value: 1,
          },
          {
            title: 'More than half the days',
            value: 2,
          },
          {
            title: 'Nearly every day',
            value: 3,
          },
        ],
      },
      user: {
        _id: 2,
        name: 'Unpacker',
      },
    },
    {
      _id: 'q9',
      text: 'Thoughts that you would be better off dead or of hurting yourself in some way',
      createdAt: new Date(),
      quickReplies: {
        type: 'radio', // or 'checkbox',
        keepIt: false,
        values: [
          {
            title: 'Not at all',
            value: 0,
          },
          {
            title: 'Several days',
            value: 1,
          },
          {
            title: 'More than half the days',
            value: 2,
          },
          {
            title: 'Nearly every day',
            value: 3,
          },
        ],
      },
      user: {
        _id: 2,
        name: 'Unpacker',
      },
    },
    {
      _id: 'q_done',
      text: 'That\'s all for the survey. Thank you~',
      createdAt: new Date(),
      user: {
        _id: 2,
        name: 'Unpacker',
      },
    }
  ]

  const context = useContext(Auth);
  /* This part is for API */
  const [isLoading, setLoading] = useState(true);
  const [data, setData] = useState([]);
  const { manifest } = Constants;
  const uri_message = `http://${manifest.debuggerHost.split(':').shift()}:5000/`;
  var send_text, replied_content = [], replied_type = [];
  const getReplies = async () => {
    console.log("Context: ",context.token);
    let formData = new FormData();
    formData.append('message', send_text);
    try {
      const response = await fetch(uri_message, {
        method: 'POST',
        headers: {
          'Content-Type': 'multipart/form-data',
          'rasa-access-token': context.token
        },
        body: formData
      });
      const json = await response.json();
      console.log("JSON?", Array.isArray(json));
      console.log("len is", json.length);
      for (var i=0; i<json.length; i++) {
        if (json[i].type === "text") {
          replied_content[i] = json[i].text;
        }
        else if (json[i].type === "gif") {
          replied_content[i] = json[i].url;
        }
        replied_type[i] = json[i].type;
      }
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
      console.log("Loading set false");
      if (replied_content.lenth == 0) {
        return ;
      }
      for (var i=0; i<replied_content.length; i++){
        if (replied_type[i] === "text"){
          const rasa_replied_msg = [{
            _id: num_chat + 1,
            text: replied_content[i],
            createdAt: new Date(),
            user: {
              _id: 2,
              name: 'Unpacker',
            },
          }]
          setMessages(previousMessages => GiftedChat.append(previousMessages, rasa_replied_msg[0]));
          num_chat++;
        }
        if (replied_type[i] === "gif"){
          const rasa_replied_msg = [{
            _id: num_chat + 1,
            image: replied_content[i], //getting GIF from links
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
    }
  }
  /* End */

  /*For starting each chat session*/
  const uri_view_profile = `http://${manifest.debuggerHost.split(':').shift()}:5000/check-do-survey`;
  useEffect(() => {
    async function checkSurveyStatus() {
      try {
        const response = await fetch(uri_view_profile, {
          method: 'GET',
          headers: {
            'rasa-access-token': context.token
          }
        });
        const json = await response.json();
        console.log(json);
        console.log("JSON?", Array.isArray(json));
        //console.log(json.surveys.length);
        if (json.result) {
          console.log("survey now");
          setMessages([
            start_message_list[0],
          ]);
          for (let i=1; i<start_message_list.length; i++){
           sendStart(i);
          }
          //num_chat = start_message_list.length;
          setTimeout(function() {setMessages(previousMessages => GiftedChat.append(previousMessages, survey_question_list[0]))}, start_message_list.length*1000);
        }
        else {
          console.log("not survey now");
          //console.log(json.surveys.length)
          setMessages([back_message_list[0],]);
          //num_chat = back_message_list.length;
        }
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
        console.log("Survey test done");
      }
      
      function sendStart(i) {
        setTimeout(function() { setMessages(previousMessages => GiftedChat.append(previousMessages, start_message_list[i]));
        }, i*1000);
      }
    };
    checkSurveyStatus();
  }, [])
  /* End */

  const onSend = useCallback((messages = []) => {
    setMessages(previousMessages => GiftedChat.append(previousMessages, messages));
    num_chat++;
    ///
    console.log(typeof messages[0].text);
    send_text = messages[0].text;
    getReplies();
  }, [])
  
  const QUESTION_NUMBER = 9;
  var num_survey_answered = 0;
  var survey_result = [];
  const uri_submit_survey = `http://${manifest.debuggerHost.split(':').shift()}:5000/add-survey-results`;
  const onQuickReply = useCallback(async (quickReply) => { 
    let message = quickReply[0].title;
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
    survey_result.push(quickReply[0].value);
    num_survey_answered++;
    setMessages(previousMessages => GiftedChat.append(previousMessages, survey_question_list[num_survey_answered]));
    num_chat++;
    console.log(survey_result);
    if (survey_result.length == QUESTION_NUMBER) {
      let formData = new FormData();
      for (let i=0; i<QUESTION_NUMBER; i++){
        let field_name = 'field_' + (i+1);
        formData.append(field_name, survey_result[i]);
      }
      try {
        const response = await fetch(uri_submit_survey, {
          method: 'POST',
          headers: {
            'Content-Type': 'multipart/form-data',
            'rasa-access-token': context.token
          },
          body: formData
        });
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    }
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
                  resizeMode="cover"
                  style={{
                    width: 300,
                    height: 200,
                    padding: 10,
                    borderRadius: 50,
                    resizeMode: "contain",
                    //object-fit: "cover",
                    //overflow: 'hidden',
                    marginLeft: 4,
                    marginRight: 4,
                    marginTop: 5,
                  }}
                  source={{ uri: props.currentMessage.image }}
                />
                <Image source={require('./Image/Poweredby_100px-Black_VertText.png')} />
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