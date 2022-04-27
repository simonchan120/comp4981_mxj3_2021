import logo from './logo.svg';
import './App.css';
import React, { useEffect, useContext, useRef } from 'react';
import * as RN from 'react-native';
import { VictoryBar, VictoryChart, VictoryAxis, VictoryTheme, VictoryStack, VictoryGroup, VictoryArea } from 'victory';
import { createStackNavigator } from '@react-navigation/stack';
import { NavigationContainer } from '@react-navigation/native';
import {
  BrowserRouter,
  Routes, //replaces "Switch" used till v5
  Route,
} from "react-router-dom";
const Stack = createStackNavigator();


//class App extends React.Component {
const Auth = React.createContext(null);

/*export default function App() {
  const [token, setToken] = React.useState(null);

  return (
    <Auth.Provider value={{token, setToken}}>
      <NavigationContainer>
      <Stack.Navigator
    initialRouteName="Login" // Add this to set initial screen
    screenOptions={{
      headerShown: false,
    }}>
        <Stack.Screen
          name="Login"
          component={Login}
          options={{ title: 'Login Page' }}/>
          <Stack.Screen
          name="Start"
          component={Start}
          options={{ title: 'Start Page' }} />
            </Stack.Navigator>
              </NavigationContainer>

    </Auth.Provider>
  );
}



const Login = ({navigation}) => {
  const [usr, setUsr] = React.useState('');
  const [pass, setPass] = React.useState('');
  //const [err_visible, setErrVisible] = React.useState(false);
  //const onDismissErrSnackBar = () => setErrVisible(false);
  
  
  //const [token, setToken] = React.useState(null);
  const context = useContext(Auth);
  
  //const { token, setToken } = React.useContext(Auth)
  //const [stateToken, setStateToken] = token;
  //const [stateName, setStateName] = name;
  //const [stateDetail, setStateDetail] = detail;
  //const { manifest } = Constants;

  //const uri = `http://${manifest.debuggerHost.split(':').shift()}:5000/login`;
  //const uri = `https://f467-210-6-181-56.ap.ngrok.io/login`;
  var uri = `https://7143-210-6-181-56.ap.ngrok.io/login`
  var json_result;
  const loginAuth = async () => {
    setTimeout(function() {console.log(uri)}, 1000);
    let formData = new FormData();
    formData.append('username', 'test1');
    formData.append('password', 'admin123');
    //setToken("Testing")

    navigation.navigate('Start')
    /*try {
      
      const response = await fetch(uri, {
        method: 'POST',
        //mode: 'no-cors',stateName
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        body: formData
      });

      const json = await response.json();
      console.log(typeof json);
      json_result = json;
      //console.log(json['rasa-access-token'] == null);
    } catch (error) {
      console.error(error);
    } finally {
      //setLoading(false);
      //console.log("Loading set false")
      if (json_result['rasa-access-token'] == null) {
      //setErrVisible(true);
      }
      else {
        context.setToken(json_result['rasa-access-token']);
        console.log(context.token);
      }
      console.log(json_result)
    }*/ /*
  }

  return (
      <div>
        <BrowserRouter>
         <form>
            <label>Username</label>
            <input 
              type="text"
              placeholder="Enter Username"
              onChange={(e) => {setUsr(e.target.value); console.log(usr);}}
              /*onChange={(t) => {
                setUsr(t);
                console.log(usr)
              }}*/ /*
              required/><br/>
            <label>Password</label>
            <input
              type="password"
              placeholder="Enter Password" 
              onChange={(e) => {setPass(e.target.value); console.log(pass);}}
              /*onChange={(t) => {
                setPass(t);
                console.log(pass)
              }}*/ /*
              required/><br/>
            <button type="submit" onClick={() => {loginAuth()}}>Login</button>
         </form>
         </BrowserRouter>
      </div>
  );
}
//var full = []
//var chat = []
//var token;*/
const App = () => {
  //render() {
    //const { token, setToken } = useContext(Auth);
    const [full, setFull] = React.useState(0)
    const [chat, setChat] = React.useState(0)

    const [full1, setFull1] = React.useState(0)
    const [chat1, setChat1] = React.useState(0)

    const [full2, setFull2] = React.useState(0)
    const [chat2, setChat2] = React.useState(0)

    const [full3, setFull3] = React.useState(0)
    const [chat3, setChat3] = React.useState(0)

    const [full4, setFull4] = React.useState(0)
    const [chat4, setChat4] = React.useState(0)

    const useComponentWillMount = (cb) => {
      const willMount = useRef(true)
  
      if (willMount.current) cb()
  
      willMount.current = false
  }
    
  const context = useContext(Auth);

      //initialRouteName="HomeScreen"

    //const token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRlc3QxIiwiZXhwIjoxNjUzNjM4MjYzfQ._Wt71osLk3O5ClrKdh2sCrduHRlTanfcsIuTWiPbGpo";
    useComponentWillMount(() => {
      //console.log(token)
      
      const uri = `https://7143-210-6-181-56.ap.ngrok.io/get-global-statistics`;
      async function getScore() {
        var target_uri;
        const dateTime = Date.now();
        var timestamp = Math.floor(dateTime / 1000);
        for (let i=0; i<5; i++) {
          let formData = new FormData();
          if (i != 0 ){
            target_uri = 'https://7143-210-6-181-56.ap.ngrok.io/get-global-statistics?start_time=' + (timestamp-86400) + '&end_time=' + timestamp
            timestamp-=86400;
          } else {
            target_uri = uri
          }
          try {
            const response = await fetch(target_uri, {
              method: 'GET',
              headers: {
                'Content-Type': 'multipart/form-data',
                //'rasa-access-token': context.token
              },
              //mode: "no-cors",
              //body: formData
            });
            
            console.log(response)
            const json = await response.json();
            //console.log(json);
            //console.log("JSON?", Array.isArray(json));
            //console.log(json.surveys.length);
            console.log("Full score is:")
            console.log(json.users_average_full_score)
            if (i == 0) {
              setFull(json.users_average_full_score)
            } else if (i == 1) {
              setFull1(json.users_average_full_score)
            } else if (i == 2) {
              setFull2(json.users_average_full_score)
            } else if (i == 3) {
              setFull3(json.users_average_full_score)
            } else if (i == 4) {
              setFull4(json.users_average_full_score)
            }
            //full.push(parseFloat(json.users_average_full_score))
            //setCurrentFull(parseFloat(json.users_average_full_score))
            //console.log(full[0])
            console.log("Chat score is:")
            console.log(json.users_average_chat_score)
            if (i == 0) {
              setChat(json.users_average_chat_score)
            } else if (i == 1) {
              setChat1(json.users_average_chat_score)
            } else if (i == 2) {
              setChat2(json.users_average_chat_score)
            } else if (i == 3) {
              setChat3(json.users_average_chat_score)
            } else if (i == 4) {
              setChat4(json.users_average_chat_score)
            }
            //chat.push(json.users_average_chat_score)
            //setCurrentChat(parseFloat(json.users_average_chat_score))
            /*setFull(json.latest_emotion_profile.full_score);
            if (json.surveys.length === 0) {
              console.log("No survey before");
              //setSurvey("No survey done before");
            }
            else {
              console.log("Done survey before");
              //console.log(json.surveys[0].result)
              //setSurvey(json.surveys[0].result);
            }*/
          } catch (error) {
            console.error(error);
          } finally {
            console.log("Survey test done");
          }
        }
      }
      //console.log("Context: ",token);
      getScore();
    }, []); 
    return (
      
<div className="App-header">
    <h1>Unpacking Happiness Backstage</h1>
    <t>General Report of current emotion score in the user community</t>

      <VictoryChart width={400} height={400}>
        <VictoryGroup
          style={{
            data: { strokeWidth: 3, fillOpacity: 0.4 }
          }}
        >
          <VictoryArea
          //labels={() => ["Thsi"]}
            style={{
              data: { fill: "cyan", stroke: "cyan" }
            }}
            data={[
              { x: "4 Day ago", y: full4},
              { x: "3 Day ago", y: full3 },
              { x: "2 Day ago", y: full2 },
              { x: "1 Day ago", y: full1 },
              { x: "Current", y: full}
            ]}
          />
          <VictoryArea
            style={{
              data: { fill: "red", stroke: "red" }
            }}
            data={[
              { x: "4 Day ago", y: chat4 },
              { x: "3 Day ago", y: chat3 },
              { x: "2 Day ago", y: chat2 },
              { x: "1 Day ago", y: chat1 },
              { x: "Current", y: chat}
            ]}
          />
        </VictoryGroup>
      </VictoryChart>

      <span style={{ color: 'cyan' }}>
            {"Overall Score"}
        </span>
        <span style={{ color: 'red' }}>
            {"Chat Score"}
        </span>
      </div>
    );
  //}
}
export default App;