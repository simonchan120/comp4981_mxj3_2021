import React from 'react';
import { StyleSheet, Text, View, FlatList, Dimensions } from 'react-native';
//import VegaScrollList from 'react-native-vega-scroll-list';
import { Card, Title, Paragraph, TouchableRipple, Button } from 'react-native-paper' ;
import { SafeAreaView } from 'react-navigation';

const ActivitiesScreen = () => {
    const languages = [
        { name: 'Activities A' , cover: 'https://picsum.photos/seed/picsum1/1200/600', key: '1' },
        { name: 'Activities B' , cover: 'https://picsum.photos/seed/picsum2/1200/600', key: '2' },
        { name: 'Activities C' , cover: 'https://picsum.photos/seed/picsum3/1200/600', key: '3' },
        { name: 'Activities ABC' , cover: 'https://picsum.photos/seed/picsum4/1200/600', key: '4' },
        { name: 'Activities DEF' , cover: 'https://picsum.photos/seed/picsum5/1200/600', key: '5' },
      ]

    return (
        <SafeAreaView style={{ flex: 1 }}>
            <View>
                <FlatList
                    //distanceBetweenItem={12}
                    horizontal = { true }
                    data = {languages}
                    renderItem={({ item }) => 
                        <TouchableRipple>
                            <Card>
                                <Card.Cover style={styles.card_template} source={{ uri: item.cover }} />
                                <Card.Content style={styles.text_template}>
                                    <Title style={styles.title}>{item.name}</Title>
                                    <Paragraph style={styles.content}>{item.name}</Paragraph>
                                </Card.Content>
                                <Card.Actions>
                                    <Button style={styles.title}>Cancel</Button>
                                    <Button style={styles.title}>Ok</Button>
                                </Card.Actions>
                            </Card>
                        </TouchableRipple>}
                />
            </View>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
  card_template:{
    //width: '30%',
    height: '30%',
    //boxShadow: "10px 10px 17px -12px rgba(0,0,0,0.75)"
  },
  text_template:{
    //width: '30%',
    height: '15%',
    //boxShadow: "10px 10px 17px -12px rgba(0,0,0,0.75)"
  },
  title:{
    fontSize: 10,
  },
  content:{
    fontSize: 8,
  },
});

export default ActivitiesScreen;