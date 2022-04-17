// React Native Bottom Navigation
// https://aboutreact.com/react-native-bottom-navigation/

import React, { useEffect } from 'react';
import { View, Text, BackHandler } from 'react-native';
import { Avatar } from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';

const ProfileScreen = ({ navigation }) => {
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
            You are on Profile Screen
          </Text>
        </View>
      </View>
    </SafeAreaView>
  );
}
export default ProfileScreen;