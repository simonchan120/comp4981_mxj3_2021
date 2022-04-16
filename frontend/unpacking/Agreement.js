import * as React from 'react';
import { View, Text } from 'react-native';
import { Button, Paragraph, Dialog, Portal, Provider } from 'react-native-paper';
const Agreement = ({ route, navigation }) => {
  const [visible, setVisible] = React.useState(true);
  //const hideDialog = () => setmodalVisible(false);

  return (
    <Provider>
      <View>
        <Portal>
          <Dialog visible={visible} /*onDismiss={hideDialog}*/>
            <Dialog.Title>About Unpacking Happiness </Dialog.Title>
            <Dialog.Content>
              <Paragraph> {content} </Paragraph>
            </Dialog.Content>
            <Dialog.Actions>
              <Button onPress={() => navigation.navigate('Chatting')}>Done</Button>
            </Dialog.Actions>
          </Dialog>
        </Portal>
      </View>
    </Provider>
  );
};

export default Agreement;
const content = "This is Unpacking Happiness, developed by UST CSE 2021-2022 FYP Group MXJ3. By using this app, you agree with our Privacy Policies. This app is based on a chatbot that is not real-time monitored, so it is NOT intended for replacement of any therapy and NOT FOR HANDLING IMMEDIATE CRISES. Please seek help immediately from proper channels if you are encountering an immediate crisis."