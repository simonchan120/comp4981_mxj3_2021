import React, { useEffect, useState } from 'react';
import { ActivityIndicator, FlatList, Text, View } from 'react-native';

import Constants from "expo-constants";

export default API_test = () => {
  const [isLoading, setLoading] = useState(true);
  const [data, setData] = useState([]);
  const { manifest } = Constants;
  const uri = `http://${manifest.debuggerHost.split(':').shift()}:5005/webhooks/rest/webhook/`;
  const getMovies = async () => {
     try {
      const response = await fetch(uri, {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          sender: 'test_user',
          message: 'What should I do?'
        })
      });

      const json = await response.json();
      console.log(typeof json[0].text);
      setData(json[0].text);
      //console.log(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
      console.log("Loading set false")
    }
  }

  useEffect(() => {
    getMovies();
  }, []);

  return (
    <View style={{ flex: 1, padding: 24 }}>
      {isLoading ? <ActivityIndicator/> : (
        <FlatList
          data={data}
          keyExtractor={({ id }, index) => id}
          renderItem={({ item }) => (
            <Text>{item}</Text>
          )}
        />
      )}
    </View>
  );
};