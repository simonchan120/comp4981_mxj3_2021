import React, { useEffect } from 'react';
import { Headline, Subheading, List } from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import { StyleSheet, BackHandler } from 'react-native';


const DeleteScreen = ({ navigation }) => {
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
            }}>Deleting Your Account</Headline>
            <Subheading
              style={{
              fontSize: 17,
              marginLeft:5,
              marginRight:5,
              textAlign: 'left',
              marginBottom: 16
            }}>If you hope to stop using this application or clear the previous data, you may delete your account.</Subheading>
            <Subheading
              style={{
              fontSize: 17,
              marginLeft:5,
              marginRight:5,
              textAlign: 'left',
              marginBottom: 16
            }}>Notice that all your data will be removed as you delete your account, and they will no longer be available for retrieval.</Subheading>
            <Subheading
              style={{
              fontSize: 17,
              marginLeft:5,
              marginRight:5,
              textAlign: 'left',
              marginBottom: 16
            }}>If you hope to use Unpacking Happiness again, you will need to set up a new account.</Subheading>
            <List.Item
                titleStyle={styles.delete}
                title = "CONFIRM DELETE ACCOUNT"
                left={props => <List.Icon {...props} icon="delete-forever" color='red'/>}
                onPress={
                () => navigation.navigate('DeletePop')
                }
            />
        </SafeAreaView>
    )
}
const styles = StyleSheet.create({
    delete: {
      color: 'red',
    },
  });
export default DeleteScreen;
