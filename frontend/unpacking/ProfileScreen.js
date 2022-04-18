// React Native Bottom Navigation
// https://aboutreact.com/react-native-bottom-navigation/

import React, { useEffect, useContext } from 'react';
import { View, Text, BackHandler } from 'react-native';
import { Avatar } from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import Constants from "expo-constants";
import {Auth} from "./App"

const ProfileScreen = ({ navigation }) => {
  const context = useContext(Auth);
  const { manifest } = Constants;
  const uri_view_profile = `http://${manifest.debuggerHost.split(':').shift()}:5000/show-profile`;
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
            'rasa-access-token': context.token
          }
        });
        const json = await response.json();
        /*console.log(json);
        console.log("JSON?", Array.isArray(json));
        console.log(json.surveys.length);*/
        console.log("Full score is:")
        console.log(json.emotion_score.full_score)
        if (json.surveys.length === 0) {
          console.log("No survey before");
        }
        else {
          console.log("Done survey before");
          console.log(json.surveys[0].result)
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
        </View>
      </View>
    </SafeAreaView>
  );
}
export default ProfileScreen;