import * as React from 'react';

import { Text, View, StyleSheet } from 'react-native';

import { Button, TextInput } from 'react-native-paper';

import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

import Constants from 'expo-constants';

const Stack = createStackNavigator();

const Auth = React.createContext(null);

export function Login() {
  const [email, setEmail] = React.useState('');
  const [pass, setPass] = React.useState('');
  
  const { setToken } = React.useContext(Auth)

  return (
    <View style={styles.container}>
      <TextInput
        label="Email"
        value={email}
        style={styles.input}
        onChangeText={(t) => setEmail(t)}
      />

      <TextInput
        label="Password"
        value={pass}
        style={styles.input}
        onChangeText={(t) => setPass(t)}
      />

      <Button mode="contained" onPress={() => setToken('Get the token and save!')}>Submit</Button>
    </View>
  );
}

export function Home() {
const { setToken } = React.useContext(Auth)

  return (
    <View>
      <Text>Home</Text>
      <Button mode="contained" onPress={() => setToken(null)}>Signout</Button>
    </View>
  );
}

export default function App() {
  const [token, setToken] = React.useState(null);

  return (
    <Auth.Provider value={{token, setToken}}>
      <NavigationContainer>
        <Stack.Navigator>
          {!token ? (
            <Stack.Screen name="Login" component={Login} />
          ) : (
            <Stack.Screen name="Home" component={Home} />
          )}
        </Stack.Navigator>
      </NavigationContainer>
    </Auth.Provider>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingTop: Constants.statusBarHeight + 20,
    padding: 20,
  },
  input: {
    marginBottom: 20,
  },
});