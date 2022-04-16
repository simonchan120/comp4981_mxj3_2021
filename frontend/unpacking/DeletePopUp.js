import React, { useContext } from 'react';
import { View, Text } from 'react-native';
import { Button, Paragraph, Dialog, Portal, Provider, Snackbar } from 'react-native-paper';
import { Restart } from 'fiction-expo-restart';
import Constants from "expo-constants";
import {Auth} from "./App"

const DeletePopUp = ({ route, navigation }) => {
  const [visible, setVisible] = React.useState(true);
  const [err_visible, setErrVisible] = React.useState(false);
  const onDismissErrSnackBar = () => setErrVisible(false);
  const context = useContext(Auth);
  const { manifest } = Constants;
  const uri_delete = `http://${manifest.debuggerHost.split(':').shift()}:5000/delete-profile`;
  async function deleteProfile() {
    
    try {
      const response = await fetch(uri_delete, {
        method: 'DELETE',
        headers: {
          'rasa-access-token': context.token
        }
      });
      const json = await response.json();
      var json_result = json;
      console.log(json.result);
      if (json_result['message'] === 'Profile deleted') {
        Restart();
      }
      else {
        setErrVisible(true);
      }
    } catch (error) {
      console.error(error);
    } finally {
      //
    }

  };
  return (
    
    <Provider>
      <View>
      <View>
        <Portal>
          <Dialog visible={visible}>
            <Dialog.Title>Deleting your account</Dialog.Title>
            <Dialog.Content>
              <Paragraph> {content} </Paragraph>
            </Dialog.Content>
            <Dialog.Actions>
              <Button onPress={() => navigation.navigate('Settings')}>Cancel</Button>
              <Button onPress={() => deleteProfile()}>Yes</Button>
            </Dialog.Actions>
          </Dialog>
        </Portal>
      </View>
      <Snackbar
      visible={err_visible}
      onDismiss={onDismissErrSnackBar}
      >
        An error occur.
    </Snackbar>
    </View>
    </Provider>
    
  );
};

export default DeletePopUp;
const content = "Are you sure you want to DELETE THIS ACCOUNT, AND ALL RECORDS AND DATA of this account? This is an IRREVERSIBLE ACTION!"