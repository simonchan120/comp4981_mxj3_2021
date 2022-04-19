import React, { useEffect, useContext, useState } from 'react';
import { Headline, Subheading, List } from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import { BackHandler, View } from 'react-native';
import YoutubePlayer from "react-native-youtube-iframe";
//import { ActivityStatus } from './ChatScreen';
import { Info } from './App';
const ActivitiesScreen = ({ navigation }) => {
    /*const { name, detail } = useContext(ActivityStatus);
    const [stateName, setStateName] = name;
    const [stateDetail, setStateDetail] = detail;*/
    const { token, name, detail } = useContext(Info);
    const [stateToken, setStateToken] = token;
    const [stateName, setStateName] = name;
    const [stateDetail, setStateDetail] = detail;
    const [show, setShow] = useState(false);
    function name_shown() {
        console.log("Now name:")
        console.log(stateName)
        // //return stateName;
        // if (!stateDetail) {
        //   setShow(false) // to hide it
        // } else {
        //   setShow(true)  // to show it  
        // }
        return !stateName ? "No activity yet" : stateName
    }
    function detail_shown() {
        console.log("Now name:")
        console.log(String(stateDetail))
        
        return !stateDetail ? "No activity yet" : stateDetail
    }
    /*useEffect(() => {
        const backAction = () => {
          navigation.navigate('Chatting');
          return true;
        };
    
        const backHandler = BackHandler.addEventListener(
          "hardwareBackPress",
          backAction
        );
    
        return () => backHandler.remove();
    }, []);*/
    return (
        <SafeAreaView style={{ flex:1 }}>
          <View>
            <Headline 
              style={{
              fontSize: 25,
              textAlign: 'center',
              marginBottom: 16
            }}>{name_shown()}</Headline>
            { stateDetail && 
              
            <YoutubePlayer
              height={500}
              //play={playing}
              videoId={stateDetail}/>}
          </View>
        </SafeAreaView>
    )
}

export default ActivitiesScreen;