import React, {  useEffect } from 'react';
import { Headline,Subheading } from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import { StyleSheet, BackHandler } from 'react-native';


const AboutScreen = ({ navigation }) => {
    useEffect(() => {
        const backAction = () => {
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
            <Headline
              style={{
              fontSize: 25,
              textAlign: 'center',
              marginBottom: 16
            }}>About Us</Headline>
            <Subheading
              style={{
              fontSize: 17,
              marginLeft:5,
              marginRight:5,
              textAlign: 'left',
              marginBottom: 16
            }}>This is Unpacking Happiness, developed by UST CSE 2021-2022 FYP Group MXJ3.</Subheading>
            <Subheading
              style={{
              fontSize: 17,
              marginLeft:5,
              marginRight:5,
              textAlign: 'left',
              marginBottom: 16
            }}>This app is based on a chatbot that is not real-time monitored, so it is NOT intended for replacement of any therapy and NOT FOR HANDLING IMMEDIATE CRISES. Please seek help immediately from proper channels if you are encountering an immediate crisis.</Subheading>
            <Subheading
              style={{
              fontSize: 17,
              marginLeft:5,
              marginRight:5,
              textAlign: 'left',
              marginBottom: 16
            }}>{helplines}</Subheading>
        </SafeAreaView>
    )
}

export default AboutScreen;

const helplines = `Some 24-hour helping hotlines available in Hong Kong:

The Samaritans 撒瑪利亞會 (Multi-Lingual)
(852) 2896 0000

Justone Mental Health Linking Project《即時通》精神健康守護同行計劃 
(852) 3512 2626

List of helplines globally is available at:
https://en.wikipedia.org/wiki/List_of_suicide_crisis_lines`