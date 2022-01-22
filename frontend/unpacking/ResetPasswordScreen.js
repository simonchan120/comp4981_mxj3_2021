import { Button as Button_Paper, TextInput as TextInput_Paper, Snackbar} from 'react-native-paper' ;
import React from "react";
import {
    StyleSheet,
    Text,
    View,
    SafeAreaView
  } from "react-native";
import Constants from "expo-constants";
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import {Restart} from 'fiction-expo-restart';

const Stack = createStackNavigator();


const ForgetPassword = () => {
  return (
    <NavigationContainer independent={true}>
      <Stack.Navigator initialRouteName="EnterEmail" screenOptions={{headerShown: false}}>
        <Stack.Screen
          name="EnterEmail"
          component={EnterEmail}
        />
        <Stack.Screen
          name="ResetPassword"
          component={ResetPassword}
        />
        <Stack.Screen
          name="DoneReset"
          component={DoneReset}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
};
export default ForgetPassword;

const EnterEmail = ({navigation}) => {
    const [err_visible, setErrVisible] = React.useState(false);
    const onDismissErrSnackBar = () => setErrVisible(false);

    const [noUsr_visible, setNoUsrVisible] = React.useState(false);
    const onDismissNoUsrSnackBar = () => setNoUsrVisible(false);

    const [email, setEmail] = React.useState('');
    const { manifest } = Constants;
  
  
    const uri = `http://${manifest.debuggerHost.split(':').shift()}:5000/signup/forget-password`;
    const resetRequest = async () => {
      let formData = new FormData();
      formData.append('email', email);
      var json_result;
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
       else if (json_result.message === 'user not found') {
        setNoUsrVisible(true);
       }
       else if (json_result.message != 'Email sent') {
        setErrVisible(true);
       }
       else {
         navigation.navigate('ResetPassword', {
          enteredEmail: email,
        })
       }
     }
    }
  
    return (
      <View style={styles.container}>
        <View style={styles_login.container}>
          <Text>Please enter the email you used to set up your account.</Text>
          <TextInput_Paper
            label="Email"
            value={email}
            style={styles_login.input}
            onChangeText={(t) => {
              setEmail(t);
            }}
          />
          <Button_Paper mode="contained" onPress={() => {
            resetRequest();
            }}>Submit</Button_Paper>
        </View>

        <Snackbar
            visible={err_visible}
            onDismiss={onDismissErrSnackBar}
            >
            An error occur.
        </Snackbar>

        <Snackbar
            visible={noUsr_visible}
            onDismiss={onDismissNoUsrSnackBar}
            >
            The email you entered is wrong.
        </Snackbar>

      </View>
    );
}

const ResetPassword = ({route, navigation}) => {
    const [err_visible, setErrVisible] = React.useState(false);
    const onDismissErrSnackBar = () => setErrVisible(false);

    const [OTP, setOTP] = React.useState('');
    const [newPassword, setNewPassword] = React.useState('');
    //const { setToken } = React.useContext(Auth)
    const { manifest } = Constants;
  


    const uri = `http://${manifest.debuggerHost.split(':').shift()}:5000/signup/reset-password`;
    const resetRequest = async () => {
      var json_result;
      let formData = new FormData();
      formData.append('email', route.params.enteredEmail);
      formData.append('otp', OTP);
      formData.append('password', newPassword);
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
       else if (json_result.message != 'Resetted password') {
        setErrVisible(true);
       }
       else {
        navigation.navigate('DoneReset');
       }
     }
    }
  
    return (
      <View style={styles.container}>
        <View style={styles_login.container}>
          <Text>Please enter the OTP you received and a new password.</Text>
          <TextInput_Paper
            label="OTP"
            value={OTP}
            style={styles_login.input}
            onChangeText={(t) => {
              setOTP(t);
            }}
          />
    
          <TextInput_Paper
            label="New Password"
            value={newPassword}
            style={styles_login.input}
            onChangeText={(t) => {
              setNewPassword(t);
            }}
          />
    
          <Button_Paper mode="contained" onPress={() => {
            resetRequest();
            }}>Submit</Button_Paper>
        </View>
        <Snackbar
            visible={err_visible}
            onDismiss={onDismissErrSnackBar}
            >
            An error occur, or your OTP is wrong.
        </Snackbar>
  
      </View>
    );
}

const DoneReset = (navigation) => {
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
            Password reset done!
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