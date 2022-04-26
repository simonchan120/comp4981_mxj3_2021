import React, { useEffect, useContext, useState } from 'react';
import { ActivityIndicator, FlatList, Text, View, BackHandler, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Info } from './App';
import Constants from "expo-constants";

export default ShowJSONScreen = ({ navigation }) => {
    const [json_result, setJSON_result] = useState(null);
    const { token, name, detail } = useContext(Info);
    const [stateToken, setStateToken] = token;
    const [stateName, setStateName] = name;
    const [stateDetail, setStateDetail] = detail;
    const { manifest } = Constants;
    const uri_view_profile = `https://7143-210-6-181-56.ap.ngrok.io/show-profile`;
    useEffect(() => {
      const backAction = () => {
        navigation.navigate('Profile');
        return true;
      };
  
      const backHandler = BackHandler.addEventListener(
        "hardwareBackPress",
        backAction
      );
      async function getProfile() {
        try {
          const response = await fetch(uri_view_profile, {
            method: 'GET',
            headers: {
              'rasa-access-token': stateToken
            }
          });
          const json = await response.json();
          setJSON_result(JSON.stringify(json));
          console.log(JSON.stringify(json))
        } catch (error) {
          console.error(error);
        } finally {
          console.log("Survey test done");
        }
      }
      getProfile();
      
      return () => backHandler.remove();
    }, []);

  return (
    <SafeAreaView style={{ flex: 1 }}>
      <ScrollView>
        <Text>{json_result}</Text>
      </ScrollView>
    </SafeAreaView>
  );
};