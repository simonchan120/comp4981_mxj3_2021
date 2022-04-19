import React, { useContext, useState } from 'react';
import { StyleSheet, Text, View, FlatList, Dimensions } from 'react-native';
//import VegaScrollList from 'react-native-vega-scroll-list';
import { Card, Title, Paragraph, TouchableRipple, Button } from 'react-native-paper' ;
import { SafeAreaView, withNavigation } from 'react-navigation';
//import { ActivityStatus } from './ChatScreen';
import { Info } from './App';
const CurrentActivitiesScreen = ({ navigation }) => {
    const languages = [
        { name: 'Activities A' , cover: 'https://picsum.photos/seed/picsum1/1200/600', key: '1' },
        /*{ name: 'Activities B' , cover: 'https://picsum.photos/seed/picsum2/1200/600', key: '2' },
        { name: 'Activities C' , cover: 'https://picsum.photos/seed/picsum3/1200/600', key: '3' },
        { name: 'Activities ABC' , cover: 'https://picsum.photos/seed/picsum4/1200/600', key: '4' },
        { name: 'Activities DEF' , cover: 'https://picsum.photos/seed/picsum5/1200/600', key: '5' },*/
      ]
    /*const { name, detail } = useContext(ActivityStatus);
    const [stateName, setStateName] = name;
    const [stateDetail, setStateDetail] = detail;*/
    const { token, name, detail } = useContext(Info);
    const [stateToken, setStateToken] = token;
    const [stateName, setStateName] = name;
    const [stateDetail, setStateDetail] = detail;
    function name_shown() {
        console.log("Now name:")
        console.log(stateName)
        //return stateName;
        return !stateName ? "No activity yet" : stateName
    }
    /*function nav() {
      navigation.navigate('ActivitiesStack');
    }*/
    return (
        <SafeAreaView style={{ flex: 1 }}>
            <View>
                <Text
                style={{
                    fontSize: 17,
                    marginLeft:5,
                    marginRight:5,
                    textAlign: 'left',
                    marginBottom: 7,
                    fontWeight: 'bold'
                  }}>Current recommended activity</Text>
                  <Text
                    style={{
                    fontSize: 15,
                    marginLeft:5,
                    marginRight:5,
                    textAlign: 'left',
                    marginBottom: 16,
                  }}>{name_shown()}</Text>
                
                <Button 
                style={{
                    align: 'right',
                  }}
                //icon="arrow-right"
                mode="contained"
                onPress={() => this.props.navigation.navigate('ActivitiesStack')}>
                    Click here for detail
                </Button>
                
            </View>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
  card_template:{
    width: '100%',
    //height: '30%',
    //boxShadow: "10px 10px 17px -12px rgba(0,0,0,0.75)"
  },
  text_template:{
    //width: '30%',
    //height: '15%',
    //boxShadow: "10px 10px 17px -12px rgba(0,0,0,0.75)"
  },
  title:{
    fontSize: 10,
  },
  content:{
    fontSize: 8,
  },
});

export default withNavigation(CurrentActivitiesScreen);