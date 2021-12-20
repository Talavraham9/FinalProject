import React from "react";
import { Button, Text, Image, View, StyleSheet } from "react-native";
import { LinearGradient } from "expo-linear-gradient";

const Home = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <LinearGradient
        colors={["#EBB150", "#E3503E"]}
        useAngle={true}
        angle={145}
        start={{ x: 0, y: 0 }}
        end={{ x: 0.5, y: 1 }}
        style={{
          height: "100%",
          width: "100%",
          padding: 15,
          alignItems: "center",
          borderRadius: 5,
        }}
      >
        <View>
          <Text style={styles.text}> Wheel-Way</Text>
          <Image style={styles.img} source={require("../assets/wheel.png")} />
        </View>
        <View style={styles.button}>
          <Button
            style={styles.button}
            mode="contained"
            color="#F8F6F4"
            compact="true"
            title="Start navigate"
            onPress={() => navigation.navigate("Camera")}
          ></Button>
        </View>
      </LinearGradient>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    backgroundColor: "whitesmoke",
    alignItems: "center",
  },
  button: {
    color: "#8fbc8f",
    marginTop: -120,
    width: "50%",
    height: 60,
    justifyContent: "center",
    borderRadius: 20,
    borderColor: "#F8F6F4",
    borderWidth: 2,
    backgroundColor: "#D77D38",
    textAlign: "center",
  },
  img: {
    width: 105,
    height: 120,
    marginBottom: 200,
    marginTop: 40,
    alignSelf: "center",
    flexWrap: "wrap",
  },
  text: {
    color: "#F8F6F4",
    fontSize: 50,
    textAlign: "center",
    marginTop: 100,
    fontWeight: "bold",
    justifyContent: "center",
    alignSelf: "center",
  },
});

export default Home;
