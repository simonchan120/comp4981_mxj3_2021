import 'react-native-gesture-handler';

//import * as React from 'react';

import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';

import {
  NavigationContainer
} from '@react-navigation/native';
import {
  createStackNavigator
} from '@react-navigation/stack';
import {
  createBottomTabNavigator
} from '@react-navigation/bottom-tabs';

import HomeScreen from './HomeScreen';
import DetailsScreen from './DetailsScreen';
import ProfileScreen from './ProfileScreen';
import SettingsScreen from './SettingsScreen';

const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();

function AccStack() {
  return (
      <Stack.Navigator
        initialRouteName="Acc"
        screenOptions={{
          headerShown: false,
          headerStyle: { backgroundColor: '#42f44b' },
          headerTintColor: '#fff',
          headerTitleStyle: { fontWeight: 'bold' }

        }}>
        <Stack.Screen
          name="Login"
          component={LoginScreen}
          options={{ title: 'Login Page' }}/>
          <Stack.Screen
          name="Details"
          component={DetailsScreen}
          options={{ title: 'Details Page' }} />

      </Stack.Navigator>
  );
}

function HomeStack() {
  return (
      <Stack.Navigator
        initialRouteName="Home"
        screenOptions={{
          headerShown: false,
          headerStyle: { backgroundColor: '#42f44b' },
          headerTintColor: '#fff',
          headerTitleStyle: { fontWeight: 'bold' }

        }}>
        <Stack.Screen
          name="Home"
          component={HomeScreen}
          options={{ title: 'Home Page' }}/>
        <Stack.Screen
          name="Details"
          component={DetailsScreen}
          options={{ title: 'Details Page' }} />
      </Stack.Navigator>
  );
}

function SettingsStack() {
  return (
    <Stack.Navigator
      initialRouteName="Settings"
      screenOptions={{
        headerStyle: { backgroundColor: '#42f44b' },
        headerTintColor: '#fff',
        headerTitleStyle: { fontWeight: 'bold' }
      }}>
      <Stack.Screen
        name="Settings"
        component={SettingsScreen}
        options={{ title: 'Setting Page' }}/>
      <Stack.Screen
        name="Details"
        component={DetailsScreen}
        options={{ title: 'Details Page' }}/>
      <Stack.Screen
        name="Profile"
        component={ProfileScreen}
        options={{ title: 'Profile Page' }}/>
    </Stack.Navigator>
  );
}

function App() {
  return (
    <NavigationContainer>
      <Tab.Navigator
        initialRouteName="Feed"
        screenOptions={{
          "tabBarActiveTintColor": '#42f44b',
          "tabBarStyle": [
            {"display": 'flex'},
          ]
        }}>
        <Tab.Screen
          name="AccStack"
          component={AccStack}
          options={{
            tabBarLabel: 'Acc',
            tabBarIcon: ({ color, size }) => (
              <MaterialCommunityIcons
                name="wrench"
                color={color}
                size={size}
              />
            ),
          }} />
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
          }} />
        <Tab.Screen
          name="HomeStack"
          component={HomeStack}
          options={{
            tabBarLabel: 'Home',
            tabBarIcon: ({ color, size }) => (
              <MaterialCommunityIcons
                name="home"
                color={color}
                size={size}
              />
            ),
          }}  />
        
      </Tab.Navigator>
    </NavigationContainer>
  );
}
export default App;



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