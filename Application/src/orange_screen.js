import React from "react";
import { Button, Text, Image, View, StyleSheet } from "react-native";
import { LinearGradient } from "expo-linear-gradient";

// let obj_in_the_way = route.params;
const orange_screen = ({ route, navigation }) => {
  // const obj_in_the_way = route.params.obj;
  // console.log(obj_in_the_way);
  return (
    <View style={styles.container}>
      <View style={styles.red_circle} pointerEvents={"none"}>
        <LinearGradient
          colors={["#F57C00", "black"]}
          style={{
            width: 300,
            height: 300,
            // padding: 125,
            borderRadius: 150,
          }}
        >
          <View style={styles.dark_red_circle}>
            <Image
              style={styles.img}
              source={require("../assets/orange_warning.png")}
            />
          </View>
        </LinearGradient>
      </View>

      <View>
        <Text style={styles.text}> {obj_in_the_way} ahead </Text>
      </View>
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
    width: 90,
    height: 90,
    borderRadius: 50,

    marginBottom: 100,
    // marginTop: 40,
    alignSelf: "center",
    position: "absolute",
    justifyContent: "center",
  },
  dark_red_circle: {
    borderColor: "#F57C00",
    justifyContent: "center",
    alignItems: "center",
    alignSelf: "center",
    width: 100,
    height: 100,
    borderRadius: 50,
    borderWidth: 50,
    marginTop: 95,
  },
  red_circle: {
    marginTop: -100,
    borderWidth: 10,
    justifyContent: "center",
    alignItems: "center",
    borderColor: "#F18D26",
    width: 310,
    height: 310,
    borderRadius: 160,
  },
  text: {
    color: "#F57C00",
    fontSize: 50,
    textAlign: "center",
    marginTop: 30,
    fontWeight: "bold",
    justifyContent: "center",
    alignSelf: "center",
    writingDirection: "rtl",
    // fontFamily: "AmaticSC-Bold",
  },
});

export default orange_screen;
