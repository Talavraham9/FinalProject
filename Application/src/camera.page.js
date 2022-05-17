import React, { useState, useEffect } from "react";
import { StyleSheet, Text, View, Button, Image } from "react-native";
import { Camera } from "expo-camera";
import * as ImagePicker from "expo-image-picker";
import { RNCamera } from "react-native-camera";
import show_image from "./image";
import * as FileSystem from "expo-file-system";

const check_connected = async () => {
  try {
    await fetch("http://192.168.1.235:5000/connect", {
      timeout: 500,
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (json) {
        let msg = json.data;
      });
  } catch (error) {
    console.log(error);
  }
};

const check_frame_response = async () => {
  try {
    await fetch("http://192.168.1.235:5000/frame", {
      timeout: 500,
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (json) {
        let sever = json.sever;
        let obj = json.obj;
        return sever, obj;
      });
  } catch (error) {
    console.log(error);
  }
};

const severity = 1;
const object_to_send = "car";

const openCamera = ({ navigation }) => {
  const [hasCameraPermission, setHasCameraPermission] = useState(null);
  const [hasGalleryPermission, setHasGalleryPermission] = useState(null);
  const [camera, setCamera] = useState(null);
  const [image, setImage] = useState(null);
  const [type, setType] = useState(Camera.Constants.Type.back);
  // const [focus, setFocus] = useState(Camera.Constants.AutoFocus.on);

  useEffect(() => {
    (async () => {
      const cameraStatus = await Camera.requestCameraPermissionsAsync();
      setHasCameraPermission(cameraStatus.status === "granted");
      const galleryStatus =
        await ImagePicker.requestMediaLibraryPermissionsAsync();
      setHasGalleryPermission(galleryStatus.status === "granted");
      takePicture();
    })();
    // const frame = await Camera.takePictureAsync();
    // console.log(type(frame))

    check_connected();
    check_frame_response();
  }, []);

  const analyze_res = (sever, obj_res) => {
    console.log("sever", sever, "obj", obj_res);
    if (sever == 1) {
      navigation.navigate("Yellow", { obj: obj_res });
    } else if (sever == 2) {
      navigation.navigate("Orange", { obj: obj_res });
    } else if (sever == 3) {
      navigation.navigate("Red", { obj: obj_res });
    }
  };

  const stopCamera = async () => {
    navigation.navigate("HomePage");
  };

  const takePicture = async () => {
    let options = {
      quality: 0.5,
      base64: true,
      forceUpOrientation: true,
      fixOrientation: true,
    };
    if (hasCameraPermission === true || hasGalleryPermission === true) {
      if (camera) {
        const img = await camera.takePictureAsync(options);
        onPictureSaved(img);
        console.log(img);
      }
    }
  };

  const onPictureSaved = (photo) => {
    navigation.navigate("Show_image", { obj: photo });
    const Upload = async () => {
      const json_obj = {};
      json_obj["img_uri"] = photo.uri;
      let body = new FormData();
      body.append("image", {
        uri: photo.uri,
        name: "photo.jpg",
        type: "image/jpg",
      });
      body.append("Content-Type", "image/jpg");

      console.log(body);
      await fetch("http://192.168.1.235:5000/recieve_image", {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        method: "POST",
        body: body,
      })
        .then((resp) => {
          resp.json().then((data) => {
            console.log(data);
            analyze_res(data.sever, data.obj);
          });
        })
        .catch(function (err) {
          console.log("error while sending data" + err.msg);
        });
    };

    Upload();
  };

  if (hasCameraPermission === null || hasGalleryPermission === false) {
    return <View />;
  }
  if (hasCameraPermission === false || hasGalleryPermission === false) {
    return <Text>No access to camera</Text>;
  }

  return (
    <View style={styles.container}>
      <Camera
        ref={(camera) => setCamera(camera)}
        style={styles.camera}
        type={type}
      />

      <View style={styles.button}>
        <Button title="Stop" color="#F8F6F4" onPress={() => stopCamera()} />
        {image && <Image source={{ uri: image }} />}
      </View>
      {/* <View style={styles.button}>
        <Button
          title="yellow"
          color="#F8F6F4"
          onPress={() => yellow_button()}
        />
        {image && <Image source={{ uri: image }} />}
      </View>
      <View style={styles.button}>
        <Button
          title="orange"
          color="#F8F6F4"
          onPress={() => orange_button()}
        />
        {image && <Image source={{ uri: image }} />}
      </View>
      <View style={styles.button}>
        <Button title="red" color="#F8F6F4" onPress={() => red_button()} />
        {image && <Image source={{ uri: image }} />}
      </View> */}
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
    width: "100%",
  },
  camera: {
    flex: 1,
    width: "100%",
    aspectRatio: 1,
  },
  cameraContainer: {
    flex: 1,
    width: "100%",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
  },
  button: {
    marginBottom: 20,
    alignSelf: "center",
    color: "#8fbc8f",
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
