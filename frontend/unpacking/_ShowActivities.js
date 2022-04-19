import React, { useEffect, useContext } from 'react';
import { Headline, Subheading, List } from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import { BackHandler } from 'react-native';
import YoutubePlayer from "react-native-youtube-iframe";
import { ActivityStatus } from './ChatScreen';
const ShowActivities = ({ navigation }) => {
    const context = useContext(ActivityStatus);
    function name_shown() {
        console.log("Now name:")
        console.log(context)
        return !context.name ? "No activity yet" : context.name
    }
    function detail_shown() {
        console.log("Now name:")
        console.log(context)
        return !context.detail ? "No activity yet" : context.detail
    }
    useEffect(() => {
        const backAction = () => {
          navigation.navigate('Chatting');
          return true;
        };
    
        const backHandler = BackHandler.addEventListener(
          "hardwareBackPress",
          backAction
        );
    
        return () => backHandler.remove();
    }, []);
    return (
        <SafeAreaView style={{ flex:1 }}>
            <Headline 
              style={{
              fontSize: 25,
              textAlign: 'center',
              marginBottom: 16
            }}>{name_shown()}</Headline>
            <YoutubePlayer
                    visible={false}
                    height={500}
                    //play={playing}
                    videoId={detail_shown()}/>
 
        </SafeAreaView>
    )
}

export default ShowActivities;