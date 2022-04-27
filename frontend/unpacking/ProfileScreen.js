import React, { useEffect, useContext, useState } from 'react';
import { View, Text, BackHandler } from 'react-native';
import { Avatar, Caption } from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import Constants from "expo-constants";
import {Info} from "./App"
import { host_name } from './App';
var full_score_content;
  var survey_score_content;
const ProfileScreen = ({ navigation }) => {
  const [full, setFull] = useState(null);
  const [survey, setSurvey] = useState(null);
  const { token, name, detail } = useContext(Info);
  const [stateToken, setStateToken] = token;
  const [stateName, setStateName] = name;
  const [stateDetail, setStateDetail] = detail;
  const { manifest } = Constants;
  const uri_view_profile = host_name + '/show-profile';
  
  useEffect(() => {
    const backAction = () => {
      /*Alert.alert("Hold on!", "Are you sure you want to go back?", [
        {
          text: "Cancel",
          onPress: () => null,
          style: "cancel"
        },
        { text: "YES", onPress: () => BackHandler.exitApp() }
      ]);*/
      navigation.navigate('Settings');
      return true;
    };

    const backHandler = BackHandler.addEventListener(
      "hardwareBackPress",
      backAction
    );
    async function getScore() {
      try {
        const response = await fetch(uri_view_profile, {
          method: 'GET',
          headers: {
            'rasa-access-token': stateToken
          }
        });
        const json = await response.json();
        /*console.log(json);
        console.log("JSON?", Array.isArray(json));
        console.log(json.surveys.length);*/
        var status_str = [
          "It seems like you are facing some rough challenges...",
          "It looks like you are facing some troubles...",
          "Seemly you are doing okay :)",
          "Seemly you are doing well!"
        ]
        console.log("Full score is:")
        console.log(json.latest_emotion_profile.full_score)
        setFull(json.latest_emotion_profile.full_score);
        var full_score_str = parseFloat(json.latest_emotion_profile.full_score).toFixed(4) + " out of 1. "
        var score_level = Math.ceil(parseFloat(json.latest_emotion_profile.full_score)*4);
        if (score_level == 0) {
          score_level = 1;
        }
        setFull(full_score_str + status_str[score_level-1]);
        if (json.surveys.length === 0) {
          console.log("No survey before");
          setSurvey("No survey done before");
          survey_score_content = "No survey done before"
        }
        else {
          console.log("Done survey before");
          console.log(json.surveys[0].result)
          setSurvey(json.surveys[0].result);
          var survey_score_str = parseFloat(json.surveys[0].result).toFixed(4) + " out of 1. "
          var score_level = Math.ceil(parseFloat(json.surveys[0].result)*4);
          if (score_level == 0) {
            score_level = 1;
        }
        setSurvey(survey_score_str + status_str[score_level-1]);
        }
      } catch (error) {
        console.error(error);
      } finally {
        console.log("Survey test done");
      }
    }
    getScore();
    return () => backHandler.remove();
  }, []);

  return (
    <SafeAreaView style={{ flex: 1 }}>
      <View style={{ flex: 1, padding: 16 }}>
        <View
          style={{
            flex: 1,
            alignItems: 'center',
            justifyContent: 'center',
          }}>
          <Avatar.Image size={240} source={ {uri:'https://picsum.photos/seed/picsum5/1200/600' }} />
          <Text
            style={{
              fontSize: 25,
              textAlign: 'center',
              marginBottom: 16
            }}>
            Your Profile
          </Text>
          <Caption>Your full emotion score:</Caption>
          <Caption>{full}</Caption>
          <Caption>Your most recent survey score:</Caption>
          <Caption>{survey}</Caption>
          <Caption>We value your right to know what we are storing.</Caption>
          <Caption>View all the stored data of your profile</Caption>
          <Caption 
            style={{color: 'blue'}}
            onPress={() => navigation.navigate('ShowJSON')}>
              in JSON format here
          </Caption>
        </View>
      </View>
    </SafeAreaView>
  );
}
export default ProfileScreen;