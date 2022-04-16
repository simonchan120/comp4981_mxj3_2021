import { Button as Button_Paper, TextInput as TextInput_Paper, Snackbar} from 'react-native-paper' ;
import React from "react";
import {
    StyleSheet,
    Text,
    View,
  } from "react-native";
import { SafeAreaView } from 'react-native-safe-area-context';
import Constants from "expo-constants";
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import {Restart} from 'fiction-expo-restart';

const Stack = createStackNavigator();

const NewUser = () => {
    return (
      <NavigationContainer independent={true}>
        <Stack.Navigator initialRouteName="EnterEmail" screenOptions={{headerShown: false}}>
          <Stack.Screen
            name="EnterData"
            component={EnterData}
          />
          <Stack.Screen
            name="VerifyPage"
            component={VerifyPage}
          />
          <Stack.Screen
            name="DoneReg"
            component={DoneReg}
          />
        </Stack.Navigator>
      </NavigationContainer>
    );
  };
export default NewUser;

const EnterData = ({navigation}) => {
    const [err_visible, setErrVisible] = React.useState(false);
    const onDismissErrSnackBar = () => setErrVisible(false);

    const [exist_visible, setExistVisible] = React.useState(false);
    const onDismissExistSnackBar = () => setExistVisible(false);

    const [empty_visible, setEmptyVisible] = React.useState(false);
    const onDismissEmptySnackBar = () => setEmptyVisible(false);
    
    const [email, setEmail] = React.useState('');
    const [usr, setUsr] = React.useState('');
    const [password, setPassword] = React.useState('');
    const { manifest } = Constants;
  
  
    const uri = `http://${manifest.debuggerHost.split(':').shift()}:5000/signup`;
    const regRequest = async () => {
      let formData = new FormData();
      formData.append('username', usr);
      formData.append('email', email);
      formData.append('password', password)
      var json_result;
      if (usr == '' || email == '' || password == '') {
        setEmptyVisible(true);
        console.log("empty!")
      }
      else {
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
        //setData(json);
        console.log(json.message);
        json_result = json;
        } catch (error) {
        console.error(error);
        //setErrVisible(true);
        } finally {
        //setLoading(false);
        console.log("Loading set false")
            if (json_result == null) {
                setErrVisible(true);
            }
            else if (json_result.message === 'Username or email already exists. Please Log in.') {
                setExistVisible(true);
            }
            else if (json_result.message != 'Successfully registered. Please verify your email.') {
                setErrVisible(true);
            }
            else {
                navigation.navigate('VerifyPage', {
                    enteredEmail: email,
                });
            }
        }
      }
    }
  
    return (
      <View style={styles.container}>
        <View style={styles_login.container}>
          <Text>Welcome! Please set up your account here :)</Text>
          <TextInput_Paper
            label="Email"
            value={email}
            style={styles_login.input}
            onChangeText={(t) => {
              setEmail(t);
            }}
          />
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
            value={password}
            style={styles_login.input}
            onChangeText={(t) => {
              setPassword(t);
            }}
          />
          <Button_Paper mode="contained" onPress={() => {
            regRequest();
            }}>Submit</Button_Paper>
        </View>

        <Snackbar
            visible={err_visible}
            onDismiss={onDismissErrSnackBar}
            >
            An error occur.
        </Snackbar>

        <Snackbar
            visible={exist_visible}
            onDismiss={onDismissExistSnackBar}
            >
            The email or username you entered is already being used.
        </Snackbar>

        <Snackbar
            visible={empty_visible}
            onDismiss={onDismissEmptySnackBar}
            >
            Email, username and password cannot be empty.
        </Snackbar>

      </View>
    );
}


const VerifyPage = ({route, navigation}) => {
    const [err_visible, setErrVisible] = React.useState(false);
    const onDismissErrSnackBar = () => setErrVisible(false);

    const [errOTP_visible, setErrOTPVisible] = React.useState(false);
    const onDismissErrOTPSnackBar = () => setErrOTPVisible(false);

    const [OTP, setOTP] = React.useState('');
    const { manifest } = Constants;
  


    const uri = `http://${manifest.debuggerHost.split(':').shift()}:5000/signup/verification`;
    const regRequest = async () => {
      var json_result;
      let formData = new FormData();
      formData.append('email', route.params.enteredEmail);
      formData.append('otp', OTP);
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
       //setData(json);
       console.log(json.message);
       json_result = json;
     } catch (error) {
       console.error(error);
     } finally {
       console.log("Loading set false")
       if (json_result == null) {
        setErrVisible(true);
       }
       else if (json_result.message === 'Wrong otp') {
        setErrOTPVisible(true);
       }
       else if (json_result.message != 'Successfully verifed') {
        setErrVisible(true);
       }
       else {
        navigation.navigate('DoneReg');
       }
     }
    }
  
    return (
      <View style={styles.container}>
        <View style={styles_login.container}>
          <Text>Please enter the OTP you received.</Text>
          <TextInput_Paper
            label="OTP"
            value={OTP}
            style={styles_login.input}
            onChangeText={(t) => {
              setOTP(t);
            }}
          />

          <Button_Paper mode="contained" onPress={() => {
            regRequest();
            }}>Submit</Button_Paper>
        </View>
        <Snackbar
            visible={err_visible}
            onDismiss={onDismissErrSnackBar}
            >
            An error occur.
        </Snackbar>
        <Snackbar
            visible={errOTP_visible}
            onDismiss={onDismissErrOTPSnackBar}
            >
            Your OTP is wrong.
        </Snackbar>
      </View>
    );
}

const DoneReg = (navigation) => {
  return (
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
            Registration done!
          </Text>
          <Button_Paper mode="contained" onPress={() => Restart()}>
            Go back to Login
          </Button_Paper>
        </View>
      </View>
    </SafeAreaView>
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