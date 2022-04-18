import React, {  useEffect } from 'react';
import { Headline,Subheading } from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import { StyleSheet, BackHandler } from 'react-native';


const AboutScreen = ({ navigation }) => {
    useEffect(() => {
        const backAction = () => {
          /*Alert.alert("Hold on!", "Are you sure you want to go back?", [
            {
              text: "Cancel",
              onPress: () => null,
              style: "cancel"
            },
            { text: "YES", onPress: () => BackHandler.exitApp() }
          ]);*/
          navigation.navigate('Settings');
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
            <Headline>About Us</Headline>
            <Subheading>This is Unpacking Happiness, developed by UST CSE 2021-2022 FYP Group MXJ3.</Subheading>
            <Subheading>This app is based on a chatbot that is not real-time monitored, so it is NOT intended for replacement of any therapy and NOT FOR HANDLING IMMEDIATE CRISES. Please seek help immediately from proper channels if you are encountering an immediate crisis.</Subheading>
            <Subheading>Here's is some resources that may be useful...</Subheading>
        </SafeAreaView>
    )
}

export default AboutScreen;