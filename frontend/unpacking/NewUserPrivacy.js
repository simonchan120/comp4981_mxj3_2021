import React, { useEffect } from 'react';
import { Headline, Checkbox, Button, Snackbar } from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import { StyleSheet, BackHandler, View, TouchableOpacity, Text, ScrollView } from 'react-native';
import { Restart } from 'fiction-expo-restart';

const NewUserPrivacy = ({ navigation }) => {
    const [checked, setChecked] = React.useState(false);
    const [error_visible, setErrorVisible] = React.useState(false);
    const onDismissErrorSnackBar = () => setErrorVisible(false);
    function CheckBox({ label, status, onPress }) {
        return (
          <TouchableOpacity onPress={onPress}>
            <View style={{ flexDirection: 'row', alignItems: 'center' }}>
              <Checkbox status={status} />
              <Text style={styles.content_bold}>{label}</Text>
            </View>
          </TouchableOpacity>
        );
    }
    
    function checkAgree() {
        if(checked) {
            navigation.navigate('EnterData');
        } else {
            setErrorVisible(true)
        }
    }

    useEffect(() => {
        const backAction = () => {
            Restart();
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
            <View style={styles.container}>
              <ScrollView>
                <Headline
                  style={{
                  fontSize: 25,
                  textAlign: 'center',
                  marginBottom: 16
                }}>Privacy Policy</Headline>
                <Text
                  style={styles.content_bold}>{intro}</Text>
                <Text
                  style={styles.title}>{title_1}</Text>
                <Text
                  style={styles.content}>{content_1}</Text>
                <Text
                  style={styles.content_bold}>{content_1_1}</Text>
                <Text
                  style={styles.title}>{title_2}</Text>
                <Text
                  style={styles.content}>{content_2}</Text>
                <Text
                  style={styles.title}>{title_3}</Text>
                <Text
                  style={styles.content}>{content_3}</Text>
                <Text
                  style={styles.title}>{title_4}</Text>
                <Text
                  style={styles.content}>{content_4}</Text>
                <Text
                  style={styles.title}>{title_5}</Text>
                <Text
                  style={styles.content}>{content_5}</Text>
                <Text
                  style={styles.title}>{title_6}</Text>
                <Text
                  style={styles.content}>{content_6}</Text>
                <CheckBox
                  status={checked ? 'checked' : 'unchecked'}
                  onPress={() => {
                      setChecked(!checked);
                  }}
                  label='I understand and agree the above Privacy Policy.'
                />
                <Button mode="contained" onPress={() => {
                  checkAgree();
                }}>Submit</Button>
              </ScrollView>
              <Snackbar
                  visible={error_visible}
                  onDismiss={onDismissErrorSnackBar}
                  duration={2000}
              >
                You need to agree with this Privacy Policy to use Unpacking Happines.
              </Snackbar>
            </View>
        </SafeAreaView>
    )
}

export default NewUserPrivacy;

const styles = StyleSheet.create({
    title: {
        fontWeight: 'bold',
        fontSize: 20,
        marginLeft:5,
        marginRight:5,
        textAlign: 'left',
        marginBottom: 5
    },
    content: {
        fontSize: 15,
        marginLeft:5,
        marginRight:5,
        textAlign: 'left',
        marginBottom: 5
    },
    content_bold: {
        fontWeight: 'bold',
        fontSize: 15,
        marginLeft:5,
        marginRight:5,
        textAlign: 'left',
        marginBottom: 5
    },
    container: {
        flex: 1,
        justifyContent: 'space-between',
    },
});

const intro = 
`HKUST CSE 2021-2022 FYP Group MXJ3 built the Unpacking Happiness app as a free app. This SERVICE is provided by HKUST CSE 2021-2022 FYP Group MXJ3 at no cost and is intended for use as is.

This page is used to inform users regarding our policies with the collection, use, and disclosure of Personal Information if anyone decided to use our Service.

If you choose to use our Service, then you agree to the collection and use of information in relation with this policy. 

The Personal Information that we collect are used for providing and improving the Service. 

We will not use or share your information with anyone except as described in this Privacy Policy.`

const title_1 = 'Information Collection and Use'

const content_1 = 
`For a better experience while using our Service, we may require you to provide us with certain personally identifiable information, including but not limited to message contents, account id and email address in this application. 

The information that we request is will be retained by us and used as described in this privacy policy.`

const content_1_1 = 
`We value the confidentiality of these information. 

Your data would not be shared to any third-party, except that they may be stored in database services offered by third-parties with strict security and confidentiality rules.

These data in plaintext can only be accessed by authorized individuals, with guarantee that these accesses are strictly necessary for the techical maintenance of the Service and they shall in no way disclose the content to any other individual.

All data stored within your account will be stored for as most 1 year unless with explicit agreement from you to extend for a designated period.

All data stored within your account will be completely deleted upon your deletion of the account.

Notice that your data, including but not limited to emotional scores generated by analysis of your data, may be used for providing an overall statistical analysis given to the backstage system of this Service for the access of dedicated individuals to monitor the general situation of your community.

These data will not include any personally identifiable information; they are strictly anonymous when being used for such purpose.`

const title_2 = 'Service Providers'

const content_2 = 
`We may employ third-party companies and individuals due to the following reasons:

    - To facilitate our Service;
    - To provide the Service on our behalf;
    - To perform Service-related services; or
    - To assist us in analyzing how our Service is used.

We want to inform users of this Service that these third parties have access to your Personal Information. The reason is to perform the tasks assigned to them on our behalf. However, they are obligated not to disclose or use the information for any other purpose.`

const title_3 = 'Security'

const content_3 =
`We value your trust in providing us your Personal Information and the confidentiality of these Personal Information, thus we are striving to use commercially acceptable means of protecting it. But remember that no method of transmission over the internet, or method of electronic storage is 100% secure and reliable, and we cannot guarantee its absolute security.`

const title_4 = 'Links to Other Sites'

const content_4 =
`This Service may contain links to other sites. If you click on a third-party link, you will be directed to that site. Note that these external sites are not operated by us. Therefore, we strongly advise you to review the Privacy Policy of these websites. We have no control over, and assume no responsibility for the content, privacy policies, or practices of any third-party sites or services.`

const title_5 = 'Changes to This Privacy Policy'

const content_5 =
`We may update our Privacy Policy from time to time. Thus, you are advised to review this page periodically for any changes. We will notify you of any changes by posting the new Privacy Policy on this page. These changes are effective immediately, after they are posted on this page.`

const title_6 = 'Contact Us'

const content_6 =
`If you have any questions or suggestions about our Privacy Policy, do not hesitate to contact us.`