import React, { useState, useEffect, useContext, useRef} from "react";
import {
  StyleSheet,
  Text,
  View,
} from "react-native";

import 'react-native-gesture-handler';
import Constants from "expo-constants";



//import * as React from 'react';

import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';

import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

import { Button as Button_Paper, TextInput as TextInput_Paper, Snackbar} from 'react-native-paper' ;

import ChatScreen from './ChatScreen';
import ProfileScreen from './ProfileScreen';
import ActivitiesScreen from "./ActivitiesScreen";
import SettingsScreen from './SettingsScreen';
//import API_test from './_API_test';
import ForgetPassword from "./ResetPasswordScreen";
import NewUser from "./NewUserScreen";
import { schedulePushNotification, registerForPushNotificationsAsync } from "./Notification";
import Agreement from "./Agreement";
import PrivacyScreen from "./PrivacyScreen";
import DeleteScreen from "./DeleteBriefScreen";
import DeletePopUp from "./DeletePopUp";
import AboutScreen from "./AboutScreen";
import ShowJSONScreen from "./ShowJSONScreen";
//import ShowActivities from "./_ShowActivities";
//import CurrentActivitiesScreen from "./_CurrentActivities";

import * as Notifications from "expo-notifications";


const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();


/*Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
  }),
});*/


/*Stack.Navigator.defaultProps = {
  headerMode: 'none',
};*/

function ChatStack() {
  return (
      <Stack.Navigator
        initialRouteName="Chat"
        screenOptions={{
          headerShown: false/*,
          headerStyle: { backgroundColor: '#42f44b' },
          headerTintColor: '#fff',
          headerTitleStyle: { fontWeight: 'bold' }*/
        }}>
          <Stack.Screen
          name="Agreement"
          component={Agreement}
          options={{ title: 'Agreement Page' }}/>
          <Stack.Screen
          name="Chatting"
          component={ChatScreen}
          options={{ title: 'Details Page' }} />
      </Stack.Navigator>
  );
}

function ActivitiesStack() {
  return (
      <Stack.Navigator
        initialRouteName="Activities"
        screenOptions={{
          headerShown: false/*,
          headerStyle: { backgroundColor: '#42f44b' },
          headerTintColor: '#fff',
          headerTitleStyle: { fontWeight: 'bold' }*/

        }}>
        <Stack.Screen
          name="Details"
          component={ActivitiesScreen}
          options={{ title: 'Activities Page' }} />
      </Stack.Navigator>
  );
}

function SettingsStack() {
  return (
    <Stack.Navigator
      initialRouteName="Settings"
      screenOptions={{
        headerShown: false/*,
        headerStyle: { backgroundColor: '#42f44b' },
        headerTintColor: '#fff',
        headerTitleStyle: { fontWeight: 'bold' }*/
      }}>
      <Stack.Screen
        name="Settings"
        component={SettingsScreen}
        options={{ title: 'Setting Page' }}/>
      <Stack.Screen
        name="Profile"
        component={ProfileScreen}
        options={{ title: 'Profile Page' }}/>
      <Stack.Screen
        name="ShowJSON"
        component={ShowJSONScreen}
        options={{ title: 'JSON Page' }}/>
      <Stack.Screen
        name="About"
        component={AboutScreen}
        options={{ title: 'About Page' }}/>
      <Stack.Screen
        name="Privacy"
        component={PrivacyScreen}
        options={{ title: 'Privacy Page' }}/>
      <Stack.Screen
        name="Delete"
        component={DeleteScreen}
        options={{ title: 'Delete Page' }}/>
      <Stack.Screen
        name="DeletePop"
        component={DeletePopUp}
        options={{ title: 'Delete Pop Up' }}/>
      </Stack.Navigator>
  );
}

export function Start() {
  // for notification
  const [expoPushToken, setExpoPushToken] = useState("");
  const [notification, setNotification] = useState(false);
  const notificationListener = useRef();
  const responseListener = useRef();
  //console.log("func Notification started!")
  // for check from API
  //const context = useContext(Auth);
  const { token, name, detail } = useContext(Info);
  const [stateToken, setStateToken] = token;
  const [stateName, setStateName] = name;
  const [stateDetail, setStateDetail] = detail;
  
  const { manifest } = Constants;
  //const uri_view_push = `http://${manifest.debuggerHost.split(':').shift()}:5000/check-send-push-notification`;
  //const uri_view_push = `https://f467-210-6-181-56.ap.ngrok.io/check-send-push-notification`;
  const uri_view_push = `https://acba-210-6-181-56.ap.ngrok.io/check-send-push-notification`;
  useEffect(() => {
    // notification
    registerForPushNotificationsAsync().then((token) =>
      setExpoPushToken(token)
    );

    notificationListener.current =
      Notifications.addNotificationReceivedListener((notification) => {
          setNotification(notification);
      });

    responseListener.current =
      Notifications.addNotificationResponseReceivedListener((response) => {
        console.log(response);
      });
    // Notification part end

    async function checkPushStatus() {
      try {
        const response = await fetch(uri_view_push, {
          method: 'GET',
          headers: {
            'rasa-access-token': stateToken
          }
        });
        const json = await response.json();
        //console.log(json);
        //console.log("JSON?", Array.isArray(json));
        console.log(json.result);
        if (json.result === true) {
          console.log("push true");
          await schedulePushNotification();
        }
        else {
          console.log("push false");
          //console.log(json.surveys.length)
          //setMessages([back_message_list[0],]);
          //num_chat = back_message_list.length;
        }
      } catch (error) {
        console.error(error);
      } finally {
        //
      }

    };
    checkPushStatus();
    // Notification
    return () => {
      Notifications.removeNotificationSubscription(
        notificationListener.current
      );
      Notifications.removeNotificationSubscription(responseListener.current);
    };
    // Notification part end
  }, []);
  return (
    <NavigationContainer independent={true} /*onPress={async () => {
      console.log("Loading!"); await schedulePushNotification();
    }}*/>
      <Tab.Navigator
        initialRouteName="ChatStack"
        screenOptions={{
          "tabBarActiveTintColor": '#42f44b',
          "tabBarStyle": [
            {"display": 'flex'},
          ]
        }}>
        <Tab.Screen
          name="ChatStack"
          component={ChatStack}
          options={{
            tabBarLabel: 'Chat',
            tabBarIcon: ({ color, size }) => (
              <MaterialCommunityIcons
                name="chat-processing-outline"
                color={color}
                size={size}
              />
            ),
            headerShown: false,
          }
          } />
        
        <Tab.Screen
          name="ActivitiesStack"
          component={ActivitiesStack}
          options={{
            tabBarLabel: 'Activities',
            tabBarIcon: ({ color, size }) => (
              <MaterialCommunityIcons
                name="human-greeting"
                color={color}
                size={size}
              />
            ),
            headerShown: false,
          }}  />
        <Tab.Screen
          name="SettingsStack"
          component={SettingsStack}
          options={{
            tabBarLabel: 'Settings',
            tabBarIcon: ({ color, size }) => (
              <MaterialCommunityIcons
                name="wrench"
                color={color}
                size={size}
              />
            ),
            headerShown: false,
          }} />
        
      </Tab.Navigator>
    </NavigationContainer>
  );
}

export const Info = React.createContext(null);

export function Login() {
  const [usr, setUsr] = React.useState('');
  const [pass, setPass] = React.useState('');
  const [err_visible, setErrVisible] = React.useState(false);
  const onDismissErrSnackBar = () => setErrVisible(false);
  
  const { token, name, detail } = useContext(Info);
  const [stateToken, setStateToken] = token;
  const [stateName, setStateName] = name;
  const [stateDetail, setStateDetail] = detail;
  const { manifest } = Constants;

  //const uri = `http://${manifest.debuggerHost.split(':').shift()}:5000/login`;
  //const uri = `https://f467-210-6-181-56.ap.ngrok.io/login`;
  const uri = `https://acba-210-6-181-56.ap.ngrok.io/login`
  const loginAuth = async () => {
    let json_result;
    let formData = new FormData();
    formData.append('username', usr);
    formData.append('password', pass);
    try {
     const response = await fetch(uri, {
       method: 'POST',
       headers: {
         'Content-Type': 'multipart/form-data'
       },
       body: formData
     });

     const json = await response.json();
     console.log(typeof json);
     json_result = json;
     console.log(json['rasa-access-token'] == null);
   } catch (error) {
     console.error(error);
   } finally {
     //setLoading(false);
     console.log("Loading set false")
     if (json_result['rasa-access-token'] == null) {
      setErrVisible(true);
     }
     else {
      setStateToken(json_result['rasa-access-token']);
     }
   }
  }

  return (
    <View style={styles.container}>
    <View style={styles_login.container}>
      <TextInput_Paper
        label="Username"
        value={usr}
        style={styles_login.input}
        onChangeText={(t) => {
          setUsr(t);
        }}
      />

      <TextInput_Paper
        label="Password"
        value={pass}
        style={styles_login.input}
        secureTextEntry={true}
        onChangeText={(t) => {
          setPass(t);
        }}
      />

      <Button_Paper mode="contained" onPress={() => {
        loginAuth();
        }}>Submit</Button_Paper>
      <Button_Paper mode="text" onPress={() => {
        setStateToken('FORGET PASSWORD');
        }}>Forget password?</Button_Paper>
      <Button_Paper mode="text" onPress={() => {
        setStateToken('NEW USER');
        }}>New to Unpacking Happiness?</Button_Paper>

    </View>
    <Snackbar
      visible={err_visible}
      onDismiss={onDismissErrSnackBar}
      >
        An error occur, or your username/password is incorrect.
    </Snackbar>
    </View>
  );
}

export function Home() {
  const { token, name, detail } = useContext(Info);
  const [stateToken, setStateToken] = token;
  const [stateName, setStateName] = name;
  const [stateDetail, setStateDetail] = detail;

  return (
    <View>
      <Text>Home</Text>
      <Button_Paper mode="contained" onPress={() => setStateToken(null)}>Signout</Button_Paper>
    </View>
  );
}

export default function App() {
  const [token, setToken] = React.useState(null);
  const [name, setName] = React.useState(null);
  const [detail, setDetail] = React.useState(null);
  return (
    <Info.Provider value={{token:[token, setToken], name: [name, setName], detail:[detail, setDetail]}}>
      <NavigationContainer>
        <Stack.Navigator
        screenOptions={{
          headerShown: false
        }}
        >
          {!token ? (
            <Stack.Screen name="Login" component={Login} />
          ) : ( token === 'FORGET PASSWORD' ? (<Stack.Screen name="Forget" component={ForgetPassword} />
          ) : ( token === 'NEW USER' ? (<Stack.Screen name="New" component={NewUser} />
          ) : (<Stack.Screen name="Start" component={Start} />))
          )}
        </Stack.Navigator>
      </NavigationContainer>
    </Info.Provider>
  );
}

const styles_login = StyleSheet.create({
  container: {
    paddingTop: Constants.statusBarHeight + 20,
    padding: 20,
  },
  input: {
    marginBottom: 20,
  },
});

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'space-between',
  },
});