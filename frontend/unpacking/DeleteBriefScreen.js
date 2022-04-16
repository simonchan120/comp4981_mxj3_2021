import React, { Component } from 'react';
import { Headline, Paragraph, Subheading, List } from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import { StyleSheet } from 'react-native';


const DeleteScreen = ({ route, navigation }) => {
    return (
        <SafeAreaView style={{ flex:1 }}>
            <Headline>Deleting Your Account</Headline>
            <Subheading>If you hope to stop using this application or clear the previous data, you may delete your account.</Subheading>
            <Subheading>Notice that all your data will be removed as you delete your account, and they will no longer be available for retrieval.</Subheading>
            <Subheading>If you hope to use Unpacking Happiness again, you will need to set up a new account.</Subheading>
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
