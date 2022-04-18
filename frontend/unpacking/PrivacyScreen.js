import React, { useEffect } from 'react';
import { StyleSheet, Text, View, BackHandler } from 'react-native';
import { WebView } from 'react-native-webview';
import { SafeAreaView } from 'react-native-safe-area-context';


const PrivacyScreen = ({ route, navigation }) => {
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
            <WebView
            originWhitelist={['*']}
            source={{ html: content }}
            />
        </SafeAreaView>
    )
}

export default PrivacyScreen;

const content = `<html>
<body>
<h2>Privacy Policy</h2>
<p>HKUST CSE 2021-2022 FYP Group MXJ3 built the Unpacking Happiness app as a free app. This SERVICE is provided by HKUST CSE 2021-2022 FYP Group MXJ3 at no cost and is intended
    for use as is.</p>
<p>This page is used to inform users regarding our policies with the collection, use, and
    disclosure of Personal Information if anyone decided to use our Service.</p>
<p>If you choose to use our Service, then you agree to the collection and use of information in
    relation with this policy. The Personal Information that we collect are used for providing and
    improving the Service. We will not use or share your information with anyone except as described
    in this Privacy Policy.</p>

<p><strong>Information Collection and Use</strong></p>
<p>For a better experience while using our Service, we may require you to provide us with certain
    personally identifiable information, including but not limited to account id and email address in this application. 
	The information that we request is will be retained by us and used as described in this privacy policy.</p>
<p>We value the confidentiality of these information, so senstive data, such as message 

<p><strong>Cookies</strong></p>
<p>Cookies are files with small amount of data that is commonly used an anonymous unique identifier.
    These are sent to your browser from the website that you visit and are stored on your devices’s
    internal memory.</p>
<p>This Services does not uses these “cookies” explicitly. However, the app may use third party code
    and libraries that use “cookies” to collection information and to improve their services. You
    have the option to either accept or refuse these cookies, and know when a cookie is being sent
    to your device. If you choose to refuse our cookies, you may not be able to use some portions of
    this Service.</p>

<p><strong>Service Providers</strong></p> <!-- This part need seem like it's not needed, but if you use any Google services, or any other third party libraries, chances are, you need this. -->
<p>[I|We] may employ third-party companies and individuals due to the following reasons:</p>
<ul>
    <li>To facilitate our Service;</li>
    <li>To provide the Service on our behalf;</li>
    <li>To perform Service-related services; or</li>
    <li>To assist us in analyzing how our Service is used.</li>
</ul>
<p>We want to inform users of this Service that these third parties have access to your Personal
    Information. The reason is to perform the tasks assigned to them on our behalf. However, they
    are obligated not to disclose or use the information for any other purpose.</p>

<p><strong>Security</strong></p>
<p>We value your trust in providing us your Personal Information and the confidentiality of these Personal Information, thus we are striving to use
    commercially acceptable means of protecting it. But remember that no method of transmission over
    the internet, or method of electronic storage is 100% secure and reliable, and we cannot
    guarantee its absolute security.</p>

<p><strong>Links to Other Sites</strong></p>
<p>This Service may contain links to other sites. If you click on a third-party link, you will be
    directed to that site. Note that these external sites are not operated by us. Therefore, we
    strongly advise you to review the Privacy Policy of these websites. We have no control over, and
    assume no responsibility for the content, privacy policies, or practices of any third-party
    sites or services.</p>

<p><strong>Children’s Privacy</strong></p>
<p>This Services do not address anyone under the age of 13. [I|We] do not knowingly collect personal
    identifiable information from children under 13. In the case [I|we] discover that a child under 13
    has provided [me|us] with personal information, [I|we] immediately delete this from our servers. If you
    are a parent or guardian and you are aware that your child has provided us with personal
    information, please contact [me|us] so that [I|we] will be able to do necessary actions.</p>

<p><strong>Changes to This Privacy Policy</strong></p>
<p>[I|We] may update our Privacy Policy from time to time. Thus, you are advised to review this page
    periodically for any changes. [I|We] will notify you of any changes by posting the new Privacy Policy
    on this page. These changes are effective immediately, after they are posted on this page.</p>

<p><strong>Contact Us</strong></p>
<p>If you have any questions or suggestions about [my|our] Privacy Policy, do not hesitate to contact
    [me|us].</p>
<p>This Privacy Policy page was created at <a href="https://privacypolicytemplate.net"
                                              target="_blank">privacypolicytemplate.net</a>.</p>
</body>
</html>`;