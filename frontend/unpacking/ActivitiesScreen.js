import React from 'react';
import { StyleSheet, Text, View, FlatList } from 'react-native';
//import VegaScrollList from 'react-native-vega-scroll-list';
import { Card, Title, Paragraph } from 'react-native-paper' ;

const ActivitiesScreen = () => {
    const languages = [
        { name: 'Pascal' , key: '1' },
        { name: 'C' , key: '2' },
        { name: 'C++' , key: '3' },
        { name: 'Java' , key: '4' },
        { name: 'JavaScript' , key: '5' },
        { name: 'Go' , key: '6' },
        { name: 'Kotlin' , key: '7' },
        { name: 'Swift' , key: '8' },
      ]

      const styles = StyleSheet.create({
        container: {
          flex: 1,
          backgroundColor: '#fff',
          paddingTop: 40,
          paddingHorizontal: 20
        },
        item: {
          marginTop: 20,
          padding: 30,
          backgroundColor: '#ffc600',
          fontSize: 24
        }
        });

    return (
        <View /*style={StyleSheet.container}*/>
            <FlatList
                //distanceBetweenItem={12}
                data = {languages}
                renderItem={({ item }) => 
                    <Card>
                        <Card.Content>
                            <Title>{item.name}</Title>
                            <Paragraph>{item.name}</Paragraph>
                        </Card.Content>
                    </Card>}
            />
        </View>
    );
}

export default ActivitiesScreen;