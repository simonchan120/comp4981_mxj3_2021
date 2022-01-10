import React from 'react';
import { StyleSheet, Text, View, FlatList, Dimensions } from 'react-native';
//import VegaScrollList from 'react-native-vega-scroll-list';
import { Card, Title, Paragraph, TouchableRipple, Button } from 'react-native-paper' ;
import { SafeAreaView } from 'react-navigation';


const window = Dimensions.get("window");


const width_proportion = '80%';
const height_proportion = '60%';

const styles = StyleSheet.create({
  screen: {
    /*flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#5A9BD4',*/
    height: height_proportion,
  },
  box: {
    width: width_proportion,
    height: height_proportion,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#B8D2EC',
  },
  text: {
    fontSize: 18,
  },
});




const ActivitiesScreen = () => {
    const languages = [
        { name: 'Activities A' , cover: 'https://picsum.photos/seed/picsum1/1200/600', key: '1' },
        { name: 'Activities B' , cover: 'https://picsum.photos/seed/picsum2/1200/600', key: '2' },
        { name: 'Activities C' , cover: 'https://picsum.photos/seed/picsum3/1200/600', key: '3' },
        { name: 'Activities ABC' , cover: 'https://picsum.photos/seed/picsum4/1200/600', key: '4' },
        { name: 'Activities DEF' , cover: 'https://picsum.photos/seed/picsum5/1200/600', key: '5' },
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

    /*const [dimensions, setDimensions] = useState({ window, screen });
    useEffect(() => {
        const subscription = Dimensions.addEventListener(
          "change",
          ({ window, screen }) => {
            setDimensions({ window, screen });
          }
        );
        return () => subscription?.remove();
      });*/

    return (
        <SafeAreaView style={{ flex: 1 }}>
            <View style={StyleSheet.screen}>
                <FlatList
                    //distanceBetweenItem={12}
                    horizontal = { true }
                    data = {languages}
                    renderItem={({ item }) => 
                        <TouchableRipple>
                            <Card>
                                <Card.Cover source={{ uri: item.cover }} />
                                <Card.Content>
                                    <Title>{item.name}</Title>
                                    <Paragraph>{item.name}</Paragraph>
                                </Card.Content>
                                <Card.Actions>
                                    <Button>Cancel</Button>
                                    <Button>Ok</Button>
                                </Card.Actions>
                            </Card>
                        </TouchableRipple>}
                />
            </View>
        </SafeAreaView>
    );
}

export default ActivitiesScreen;