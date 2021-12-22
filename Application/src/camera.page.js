import React, { useState, useEffect } from "react";
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  Button,
  Image,
} from "react-native";
import { Camera } from "expo-camera";
import * as ImagePicker from "expo-image-picker";
import react from "react";

const openCamera = ({ navigation }) => {
  const [hasCameraPermission, setHasCameraPermission] = useState(null);
  const [hasGalleryPermission, setHasGalleryPermission] = useState(null);
  const [camera, setCamera] = useState(null);
  const [image, setImage] = useState(null);
  const [type, setType] = useState(Camera.Constants.Type.back);
  useEffect(() => {
    (async () => {
      const cameraStatus = await Camera.requestCameraPermissionsAsync();
      setHasCameraPermission(cameraStatus.status === "granted");
      const galleryStatus =
        await ImagePicker.requestMediaLibraryPermissionsAsync();
      setHasGalleryPermission(galleryStatus.status === "granted");
    })();
  }, []);

  const stopCamera = async () => {
    navigation.navigate("HomePage");
  };

  if (hasCameraPermission === null || hasGalleryPermission === false) {
    return <View />;
  }
  if (hasCameraPermission === false || hasGalleryPermission === false) {
    return <Text>No access to camera</Text>;
  }
  return (
    <View style={styles.container}>
      <View style={styles.cameraContainer}>
        <Camera
          ref={(ref) => setCamera(ref)}
          style={styles.camera}
          type={type}
          ratio={"1:1"}
          useNativeZoom="true"
        />
        {/* <View style={styles.red_circle} pointerEvents={"none"}>
          <Text style={styles.text}> Danger!!!</Text>
        </View>
        <View style={styles.orange_circle} pointerEvents={"none"}>
          <Text style={styles.text}> Warning !!!</Text>
        </View>
        <View style={styles.green_circle} pointerEvents={"none"}>
          <Text style={styles.text}> All clear!!!</Text>
        </View> */}
      </View>
      <View style={styles.button}>
        <Button title="Stop" color="#F8F6F4" onPress={() => stopCamera()} />
        {image && <Image source={{ uri: image }} />}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignContent: "center",
    backgroundColor: "#EBB150",
    flexDirection: "column",
    alignItems: "center",
  },
  camera: {
    flex: 1,
    aspectRatio: 1,
  },
  cameraContainer: {
    flex: 1,
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
  },
  button: {
    marginBottom: 20,
    alignSelf: "center",
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
  red_circle: {
    borderWidth: 100,
    borderColor: "red",
    position: "absolute",
    justifyContent: "center",
    alignItems: "center",
    width: 200,
    height: 200,
    borderRadius: 100,
  },
  orange_circle: {
    borderWidth: 100,
    borderColor: "orange",
    position: "absolute",
    justifyContent: "center",
    alignItems: "center",
    width: 200,
    height: 200,
    borderRadius: 100,
  },
  green_circle: {
    borderWidth: 100,
    borderColor: "green",
    position: "absolute",
    justifyContent: "center",
    alignItems: "center",
    width: 200,
    height: 200,
    borderRadius: 100,
  },
  text: {
    position: "absolute",
    color: "#F8F6F4",
    fontSize: 30,
  },
});

export default openCamera;
