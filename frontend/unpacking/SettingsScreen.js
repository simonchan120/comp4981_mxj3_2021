// React Native Bottom Navigation
// https://aboutreact.com/react-native-bottom-navigation/
import * as React from 'react';
import {
  TouchableOpacity,
  StyleSheet,
  View,
  Text,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

import { List } from 'react-native-paper';

const SettingsScreen = ({ route, navigation }) => {
  return (
    <SafeAreaView /*style={styles.container}*/>
      <List.Item
        title = "My Profile"
        left={props => <List.Icon {...props} icon="account" />}
        onPress={
          () => navigation.navigate('Profile')
        }
      />
      <List.Item
        title = "About"
        left={props => <List.Icon {...props} icon="information" />}
        onPress={
          () => navigation.navigate('Profile')
        }
      />
      <List.Item
        title = "Privacy Policies"
        left={props => <List.Icon {...props} icon="shield-star" />}
        onPress={
          () => navigation.navigate('Privacy')
        }
      />
      <List.Item
        titleStyle={styles.delete}
        title = "Delete Account"
        left={props => <List.Icon {...props} icon="delete-forever" color='red'/>}
        onPress={
          () => navigation.navigate('Delete')
        }
      />
    </SafeAreaView>
  )
  /*return (
    <SafeAreaView style={{ flex: 1 }}>
      <View style={{ flex: 1, padding: 16 }}>
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
            You are on Setting Screen
          </Text>
          <TouchableOpacity
            style={styles.button}
            onPress={
              () => navigation.navigate('Profile')
            }>
            <Text>Open Profile Screen</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.button}
            onPress={
              () => navigation.navigate('API')
            }>
            <Text>Open API test Screen</Text>
          </TouchableOpacity>
        </View>
      </View>
    </SafeAreaView>
  );*/

}
const styles = StyleSheet.create({
  button: {
    alignItems: 'center',
    backgroundColor: '#DDDDDD',
    padding: 10,
    width: 300,
    marginTop: 16,
  },
  container: {
    flex: 1,
  },
  delete: {
    color: 'red',
  },
});
export default SettingsScreen;