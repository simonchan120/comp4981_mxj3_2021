// React Native Bottom Navigation
// https://aboutreact.com/react-native-bottom-navigation/

import * as React from 'react';
import { View, Text } from 'react-native';
import { Avatar } from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';

const ProfileScreen = () => {
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