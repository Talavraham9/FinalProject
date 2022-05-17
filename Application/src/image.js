import React from "react";
import { Image, ImageBackground, View, StyleSheet } from "react-native";

const show_image = ({ route, navigation }) => {
  const img_to_show = route.params.obj;
  console.log("image page", img_to_show);
  return (
    <View style={styles.container}>
      <Image style={styles.img} source={{ uri: img_to_show.uri }} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    backgroundColor: "#423C3B",
    alignItems: "center",
  },
  img: {
    flex: 1,
    width: "100%",
    height: "100%",
    borderRadius: 50,
  },
});

export default show_image;
