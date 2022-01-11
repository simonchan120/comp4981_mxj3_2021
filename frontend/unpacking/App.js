import { StatusBar } from "expo-status-bar";
import React, { useState } from "react";
import {
  StyleSheet,
  Text,
  View,
  Image,
  TextInput,
  Button,
  TouchableOpacity,
} from "react-native";

import 'react-native-gesture-handler';

//import * as React from 'react';

import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';

import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

import { Button as Button_Paper, TextInput as TextInput_Paper} from 'react-native-paper' ;

import Constants from 'expo-constants';

import HomeScreen from './HomeScreen';
import ChatScreen from './ChatScreen';
import ProfileScreen from './ProfileScreen';
import ActivitiesScreen from "./ActivitiesScreen";
import SettingsScreen from './SettingsScreen';
import API_test from './API_test';

const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();

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
        name="Chat"
        component={ChatScreen}
        options={{ title: 'Details Page' }}/>
      <Stack.Screen
        name="Profile"
        component={ProfileScreen}
        options={{ title: 'Profile Page' }}/>
      <Stack.Screen
        name="API"
        component={API_test}
        options={{ title: 'API test Page' }}/>
    </Stack.Navigator>
  );
}

export function Start() {
  return (
    <NavigationContainer independent={true}>
      <Tab.Navigator
        initialRouteName="Feed"
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
//export default App;




const Auth = React.createContext(null);

export function Login() {
  const [email, setEmail] = React.useState('');
  const [pass, setPass] = React.useState('');
  
  const { setToken } = React.useContext(Auth)

  return (
    <View style={styles_login.container}>
      <TextInput_Paper
        label="Email"
        value={email}
        style={styles_login.input}
        onChangeText={(t) => setEmail(t)}
      />

      <TextInput_Paper
        label="Password"
        value={pass}
        style={styles_login.input}
        onChangeText={(t) => setPass(t)}
      />

      <Button_Paper mode="contained" onPress={() => setToken('Get the token and save!')}>Submit</Button_Paper>
    </View>
  );
}

export function Home() {
const { setToken } = React.useContext(Auth)

  return (
    <View>
      <Text>Home</Text>
      <Button_Paper mode="contained" onPress={() => setToken(null)}>Signout</Button_Paper>
    </View>
  );
}

export default function App() {
  const [token, setToken] = React.useState(null);

  return (
    <Auth.Provider value={{token, setToken}}>
      <NavigationContainer>
        <Stack.Navigator
        screenOptions={{
          headerShown: false
        }}
        >
          {!token ? (
            <Stack.Screen name="Login" component={Login} />
          ) : (
            <Stack.Screen name="Start" component={Start} />
          )}
        </Stack.Navigator>
      </NavigationContainer>
    </Auth.Provider>
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



 
const LoginScreen = ({ navigation }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
 
  return (
    <View style={styles.container}>

 
      <StatusBar style="auto" />
      <View style={styles.inputView}>
        <TextInput
          style={styles.TextInput}
          placeholder="Email"
          placeholderTextColor="#003f5c"
          onChangeText={(email) => setEmail(email)}
        />
      </View>
 
      <View style={styles.inputView}>
        <TextInput
          style={styles.TextInput}
          placeholder="Password"
          placeholderTextColor="#003f5c"
          secureTextEntry={true}
          onChangeText={(password) => setPassword(password)}
        />
      </View>
 
      <TouchableOpacity>
        <Text style={styles.forgot_button}>Forgot Password?</Text>
      </TouchableOpacity>
 
      <TouchableOpacity 
        style={styles.loginBtn}
        onPress={
          () => navigation.navigate('Details')
        }
      >
        <Text style={styles.loginText}>LOGIN</Text>
      </TouchableOpacity>
    </View>
  );
}
 
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
  },
 
  image: {
    marginBottom: 40,
  },
 
  inputView: {
    backgroundColor: "#FFA500",
    borderRadius: 30,
    width: "70%",
    height: 45,
    marginBottom: 20,
 
    alignItems: "center",
  },
 
  TextInput: {
    height: 50,
    flex: 1,
    padding: 10,
    marginLeft: 20,
  },
 
  forgot_button: {
    height: 30,
    marginBottom: 30,
  },
 
  loginBtn: {
    width: "80%",
    borderRadius: 25,
    height: 50,
    alignItems: "center",
    justifyContent: "center",
    marginTop: 40,
    backgroundColor: "#FFA500",
  },
});