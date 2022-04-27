import logo from './logo.svg';
import './App.css';
import React, { useEffect, useContext } from 'react';
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


/*const data2012 = [
  {quarter: 1, earnings: 13000},
  {quarter: 2, earnings: 16500},
  {quarter: 3, earnings: 14250},
  {quarter: 4, earnings: 19000}
];

const data2013 = [
  {quarter: 1, earnings: 15000},
  {quarter: 2, earnings: 12500},
  {quarter: 3, earnings: 19500},
  {quarter: 4, earnings: 13000}
];

const data2014 = [
  {quarter: 1, earnings: 11500},
  {quarter: 2, earnings: 13250},
  {quarter: 3, earnings: 20000},
  {quarter: 4, earnings: 15500}
];

const data2015 = [
  {quarter: 1, earnings: 18000},
  {quarter: 2, earnings: 13250},
  {quarter: 3, earnings: 15000},
  {quarter: 4, earnings: 12000}
];
function App() {
  return (
    <div className="App-header">
    <h1>Unpacking Happiness Backstage</h1>
    <t>General Report of currentemotion score in the user community</t>
    <VictoryChart
      domainPadding={10}
      theme={VictoryTheme.material}
    >
      <VictoryAxis
        tickValues={["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"]}
      />
      <VictoryAxis
        dependentAxis
        tickFormat={(x) => ({x})}
      />
      <VictoryStack
        colorScale={"warm"}
      >
        <VictoryBar
          data={data2012}
          x={"week1"}
          y={"value"}
        />
        <VictoryBar
          data={data2013}
          x={"week2"}
          y={"value"}
        />
        <VictoryBar
          data={data2014}
          x={"week3"}
          y={"value"}
        />
        <VictoryBar
          data={data2015}
          x={"week4"}
          y={"value"}
        />
      </VictoryStack>
    </VictoryChart>
  </div>
  );
}
/*const PieChart = (props: Props) => {

  const [data, setData] = useState<Data[]>([]);
  const [endAngle, setEndAngle] = useState(0);

  useEffect(() => {
    setTimeout(() => {
      setData(props.pieData);
      setEndAngle(360);
    }, 100);
  }, []);

  return (
    <VictoryPie
      animate={{
        duration: 2000,
        easing: "bounce"
      }}
      endAngle={endAngle}
      colorScale={props.pieColors}
      data={data}
      height={height}
      innerRadius={100}
      labels={() => ""}
      name={"pie"}
      padding={0}
      radius={({ datum, index }) => index === selectedIndex ? 130 : 120}
      width={width}
   />
)*/
//class App extends React.Component {
const Auth = React.createContext(null);

export default function App() {
  const [token, setToken] = React.useState(null);

  return (
    <Auth.Provider value={{token, setToken}}>
      <NavigationContainer>

        <Stack.Screen
          name="Login"
          component={Login}
          options={{ title: 'Login Page' }}/>
          <Stack.Screen
          name="Start"
          component={Start}
          options={{ title: 'Start Page' }} />
              </NavigationContainer>

    </Auth.Provider>
  );
}



/*const Login = ({navigation}) => {
  const [usr, setUsr] = React.useState('');
  const [pass, setPass] = React.useState('');
  //const [err_visible, setErrVisible] = React.useState(false);
  //const onDismissErrSnackBar = () => setErrVisible(false);
  const [token, setToken] = React.useState(null);
  //const { token, setToken } = React.useContext(Auth)
  //const [stateToken, setStateToken] = token;
  //const [stateName, setStateName] = name;
  //const [stateDetail, setStateDetail] = detail;
  //const { manifest } = Constants;

  //const uri = `http://${manifest.debuggerHost.split(':').shift()}:5000/login`;
  //const uri = `https://f467-210-6-181-56.ap.ngrok.io/login`;
  var uri = `https://7143-210-6-181-56.ap.ngrok.io/login`
  var json_result;
  const _App = async () => {
    setTimeout(function() {console.log(uri)}, 1000);
    let formData = new FormData();
    formData.append('username', 'test1');
    formData.append('password', 'admin123');
    setToken("Testing")

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
        setToken(json_result['rasa-access-token']);
        console.log(token);
      }
      console.log(json_result)
    }*//*
  }

  return (
    <Auth.Provider value={{token, setToken}}>
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
              }}*//*
              required/><br/>
            <label>Password</label>
            <input
              type="password"
              placeholder="Enter Password" 
              onChange={(e) => {console.log(token); setPass(e.target.value); console.log(pass);}}
              /*onChange={(t) => {
                setPass(t);
                console.log(pass)
              }}*//*
              required/><br/>
            <button type="submit" onClick={() => {loginAuth()}}>Login</button>
         </form>
         </BrowserRouter>
      </div>
      </Auth.Provider>
  );
}*/

const Start = () => {
  //render() {
    //const { token, setToken } = useContext(Auth);
    const token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRlc3QxIiwiZXhwIjoxNjUzNjE1Njc2fQ.t8hO84XZ5cer6S7E7CXeo8939QKrYfDU_bLuC7RbohI";
    useEffect(() => {
      console.log(token)
      const uri_view_profile = `https://7143-210-6-181-56.ap.ngrok.io/get-global-statistics`;
      async function getScore() {
        try {
          const response = await fetch(uri_view_profile, {
            method: 'GET',
            headers: {
              'rasa-access-token': token
            },
            mode: "no-cors",
          });
          const json = await response.json();
          console.log(json);
          //console.log("JSON?", Array.isArray(json));
          //console.log(json.surveys.length);
          console.log("Full score is:")
          console.log(json.users_average_full_score)
          console.log("Chat score is:")
          console.log(json.users_average_chat_score)
          /*setFull(json.latest_emotion_profile.full_score);
          if (json.surveys.length === 0) {
            console.log("No survey before");
            setSurvey("No survey done before");
          }
          else {
            console.log("Done survey before");
            console.log(json.surveys[0].result)
            setSurvey(json.surveys[0].result);
          }*/
        } catch (error) {
          console.error(error);
        } finally {
          console.log("Survey test done");
        }
      }
      console.log("Context: ",token);
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
              { x: "Jan", y: 0.75},
              { x: "Feb", y: 0.8 },
              { x: "Mar", y: 0.72 },
              { x: "Apr", y: 0.52 },
              { x: "May", y: 0.42}
            ]}
          />
          <VictoryArea
            style={{
              data: { fill: "red", stroke: "red" }
            }}
            data={[
              { x: "Jan", y: 0.66 },
              { x: "Feb", y: 0.9, },
              { x: "Mar", y: 0.8 },
              { x: "Apr", y: 0.33 },
              { x: "May", y: 0.40  }
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


/*class App extends React.Component {
  render() {
    const styles = this.getStyles();
    const dataSetOne = this.getDataSetOne();
    const dataSetTwo = this.getDataSetTwo();
    const tickValues = this.getTickValues();

    return (
      <svg style={styles.parent} viewBox="0 0 450 350">

        {/* Create stylistic elements }
        <rect x="0" y="0" width="10" height="30" fill="#f01616"/>
        <rect x="420" y="10" width="20" height="20" fill="#458ca8"/>

        {/* Define labels }
        <VictoryLabel x={25} y={24} style={styles.title}
          text="An outlook"
        />
        <VictoryLabel x={430} y={20} style={styles.labelNumber}
          text="1"
        />
        <VictoryLabel x={25} y={55} style={styles.labelOne}
          text={"Economy \n % change on a year earlier"}
        />
        <VictoryLabel x={425} y={55} style={styles.labelTwo}
          text={"Dinosaur exports\n $bn"}
        />

        <g transform={"translate(0, 40)"}>
          {/* Add shared independent axis }
          <VictoryAxis
            scale="time"
            standalone={false}
            style={styles.axisYears}
            tickValues={tickValues}
            tickFormat={
              (x) => {
                if (x.getFullYear() === 2000) {
                  return x.getFullYear();
                }
                if (x.getFullYear() % 5 === 0) {
                  return x.getFullYear().toString().slice(2);
                }
              }
            }
          />

          {/*
            Add the dependent axis for the first data set.
            Note that all components plotted against this axis will have the same y domain
          }
          <VictoryAxis dependentAxis
            domain={[-10, 15]}
            offsetX={50}
            orientation="left"
            standalone={false}
            style={styles.axisOne}
          />

          {/* Red annotation line }
          <VictoryLine
            data={[
              {x: new Date(1999, 1, 1), y: 0},
              {x: new Date(2014, 6, 1), y: 0}
            ]}
            domain={{
              x: [new Date(1999, 1, 1), new Date(2016, 1, 1)],
              y: [-10, 15]
            }}
            scale={{x: "time", y: "linear"}}
            standalone={false}
            style={styles.lineThree}
          />

          {/* dataset one }
          <VictoryLine
            data={dataSetOne}
            domain={{
              x: [new Date(1999, 1, 1), new Date(2016, 1, 1)],
              y: [-10, 15]
            }}
            interpolation="monotoneX"
            scale={{x: "time", y: "linear"}}
            standalone={false}
            style={styles.lineOne}
          />

          {/*
            Add the dependent axis for the second data set.
            Note that all components plotted against this axis will have the same y domain
          }
          <VictoryAxis dependentAxis
            domain={[0, 50]}
            orientation="right"
            standalone={false}
            style={styles.axisTwo}
          />

          {/* dataset two }
          <VictoryLine
            data={dataSetTwo}
            domain={{
              x: [new Date(1999, 1, 1), new Date(2016, 1, 1)],
              y: [0, 50]
            }}
            interpolation="monotoneX"
            scale={{x: "time", y: "linear"}}
            standalone={false}
            style={styles.lineTwo}
          />
        </g>
      </svg>
    );
  }

  getDataSetOne() {
    return [
      {x: new Date(2000, 1, 1), y: 12},
      {x: new Date(2000, 6, 1), y: 10},
      {x: new Date(2000, 12, 1), y: 11},
      {x: new Date(2001, 1, 1), y: 5},
      {x: new Date(2002, 1, 1), y: 4},
      {x: new Date(2003, 1, 1), y: 6},
      {x: new Date(2004, 1, 1), y: 5},
      {x: new Date(2005, 1, 1), y: 7},
      {x: new Date(2006, 1, 1), y: 8},
      {x: new Date(2007, 1, 1), y: 9},
      {x: new Date(2008, 1, 1), y: -8.5},
      {x: new Date(2009, 1, 1), y: -9},
      {x: new Date(2010, 1, 1), y: 5},
      {x: new Date(2013, 1, 1), y: 1},
      {x: new Date(2014, 1, 1), y: 2},
      {x: new Date(2015, 1, 1), y: -5}
    ];
  }

  getDataSetTwo() {
    return [
      {x: new Date(2000, 1, 1), y: 5},
      {x: new Date(2003, 1, 1), y: 6},
      {x: new Date(2004, 1, 1), y: 4},
      {x: new Date(2005, 1, 1), y: 10},
      {x: new Date(2006, 1, 1), y: 12},
      {x: new Date(2007, 2, 1), y: 48},
      {x: new Date(2008, 1, 1), y: 19},
      {x: new Date(2009, 1, 1), y: 31},
      {x: new Date(2011, 1, 1), y: 49},
      {x: new Date(2014, 1, 1), y: 40},
      {x: new Date(2015, 1, 1), y: 21}
    ];
  }

  getTickValues() {
    return [
      new Date(1999, 1, 1),
      new Date(2000, 1, 1),
      new Date(2001, 1, 1),
      new Date(2002, 1, 1),
      new Date(2003, 1, 1),
      new Date(2004, 1, 1),
      new Date(2005, 1, 1),
      new Date(2006, 1, 1),
      new Date(2007, 1, 1),
      new Date(2008, 1, 1),
      new Date(2009, 1, 1),
      new Date(2010, 1, 1),
      new Date(2011, 1, 1),
      new Date(2012, 1, 1),
      new Date(2013, 1, 1),
      new Date(2014, 1, 1),
      new Date(2015, 1, 1),
      new Date(2016, 1, 1)
    ];
  }

  getStyles() {
    const BLUE_COLOR = "#00a3de";
    const RED_COLOR = "#7c270b";

    return {
      parent: {
        background: "#ccdee8",
        boxSizing: "border-box",
        display: "inline",
        padding: 0,
        fontFamily: "'Fira Sans', sans-serif"
      },
      title: {
        textAnchor: "start",
        verticalAnchor: "end",
        fill: "#000000",
        fontFamily: "inherit",
        fontSize: "18px",
        fontWeight: "bold"
      },
      labelNumber: {
        textAnchor: "middle",
        fill: "#ffffff",
        fontFamily: "inherit",
        fontSize: "14px"
      },

      // INDEPENDENT AXIS
      axisYears: {
        axis: { stroke: "black", strokeWidth: 1},
        ticks: {
          size: ({ tick }) => {
            const tickSize =
              tick.getFullYear() % 5 === 0 ? 10 : 5;
            return tickSize;
          },
          stroke: "black",
          strokeWidth: 1
        },
        tickLabels: {
          fill: "black",
          fontFamily: "inherit",
          fontSize: 16
        }
      },

      // DATA SET ONE
      axisOne: {
        grid: {
          stroke: ({ tick }) =>
            tick === -10 ? "transparent" : "#ffffff",
          strokeWidth: 2
        },
        axis: { stroke: BLUE_COLOR, strokeWidth: 0 },
        ticks: { strokeWidth: 0 },
        tickLabels: {
          fill: BLUE_COLOR,
          fontFamily: "inherit",
          fontSize: 16
        }
      },
      labelOne: {
        fill: BLUE_COLOR,
        fontFamily: "inherit",
        fontSize: 12,
        fontStyle: "italic"
      },
      lineOne: {
        data: { stroke: BLUE_COLOR, strokeWidth: 4.5 }
      },
      axisOneCustomLabel: {
        fill: BLUE_COLOR,
        fontFamily: "inherit",
        fontWeight: 300,
        fontSize: 21
      },

      // DATA SET TWO
      axisTwo: {
        axis: { stroke: RED_COLOR, strokeWidth: 0 },
        tickLabels: {
          fill: RED_COLOR,
          fontFamily: "inherit",
          fontSize: 16
        }
      },
      labelTwo: {
        textAnchor: "end",
        fill: RED_COLOR,
        fontFamily: "inherit",
        fontSize: 12,
        fontStyle: "italic"
      },
      lineTwo: {
        data: { stroke: RED_COLOR, strokeWidth: 4.5 }
      },

      // HORIZONTAL LINE
      lineThree: {
        data: { stroke: "#e95f46", strokeWidth: 2 }
      }
    };
  }
}

//ReactDOM.render(<CustomTheme/>, mountNode)*/