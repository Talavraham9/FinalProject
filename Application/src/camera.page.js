import React, { useState, useEffect } from "react";
import { StyleSheet, Text, View, Image } from "react-native";
import { Camera } from "expo-camera";
import { LinearGradient } from "expo-linear-gradient";
import * as ImageManipulator from "expo-image-manipulator";

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
let sever;
const OpenCamera = ({ navigation }) => {
  let [obj, setObj] = useState(null);
  const [hasCameraPermission, setHasCameraPermission] = useState(null);
  const [camera, setCamera] = useState(null);
  const [type, setType] = useState(Camera.Constants.Type.back);
  const [showYellowAlert, setshowYellowAlert] = React.useState(false);
  const [showOrangeAlert, setshowOrangeAlert] = React.useState(false);
  const [showRedAlert, setRedAlert] = React.useState(false);

  useEffect(() => {
    // ask for permissions from the camera
    permisionFunction();
    takePicture();
  }, []);

  // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  const permisionFunction = async () => {
    // here is how to get the camera permission
    const cameraPermission = await Camera.requestCameraPermissionsAsync();
    setHasCameraPermission(cameraPermission.status === "granted");
    if (cameraPermission.status !== "granted") {
      alert("Permission for media access needed.");
    }
  };

  // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  const takePicture = async () => {
    console.log("take picture function");
    // this function take a picture from the camera and move to a callback function with the frame received.
    let options = {
      quality: 1,
      skipProcessing: true,
      base64: true,
      exif: true,
      forceUpOrientation: true,
      fixOrientation: false,
    };
    if (hasCameraPermission === true) {
      let img = await camera.takePictureAsync(options);
      img = await ImageManipulator.manipulateAsync(
        img.uri,
        [{ resize: { width: 640, height: 480 } }],
        { compress: 0, format: "jpeg", base64: false }
      );
      onPictureSaved(img);
    }
  };

  // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  const onPictureSaved = (photo) => {
    // this function sent a fetch request to the server and send him the frame received from the camera, and wait for the response that contain a
    // json object with the severity of an object, and the object.
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

      await fetch("https://finalprojectwheelapp.herokuapp.com/img", {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        method: "POST",
        body: body,
      })
        .then((resp) => {
          // console.log(resp);
          resp.json().then((data) => {
            sever = data.sever;
            obj = data.obj;
            analyze_res(sever, obj);
          });
        })
        .catch(function (err) {
          console.log("error while sending data " + err.msg);
        });
    };

    Upload();
  };

  // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  const analyze_res = (sever, obj_res) => {
    // this function receives 2 variables, and decide which color of alert will be shown and the object that will be wrriten
    if (sever == 0) {
      // no alert
      setshowYellowAlert(false);
      setshowOrangeAlert(false);
      setRedAlert(false);
      setObj(null);
    } else if (sever == 1) {
      // red alert
      setshowYellowAlert(true);
      setshowOrangeAlert(false);
      setRedAlert(false);
      setObj(obj_res);
    } else if (sever == 2) {
      // orange alert
      setshowOrangeAlert(true);
      setshowYellowAlert(false);
      setRedAlert(false);
      setObj(obj_res);
    } else if (sever == 3) {
      // yellow alert
      setshowYellowAlert(false);
      setshowOrangeAlert(false);
      setRedAlert(true);
      setObj(obj_res);
    }
    takePicture();
  };

  // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  const Yellow = () => {
    //  this function return a view for a yellow alert
    return (
      <LinearGradient colors={["#FCDC00", "black"]} style={styles.yellow}>
        <View>
          <Image
            style={styles.sign}
            source={require("../assets/yellow_warning.jpg")}
          />
        </View>
        <View>
          <Text style={styles.text}> {obj} ahead </Text>
        </View>
      </LinearGradient>
    );
  };

  // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  const Orange = () => {
    //  this function return a view for a orange alert
    return (
      <LinearGradient colors={["#F57C00", "black"]} style={styles.yellow}>
        <View>
          <Image
            style={styles.sign}
            source={require("../assets/orange_warning.png")}
          />
        </View>
        <View>
          <Text style={styles.text}> {obj} ahead </Text>
        </View>
      </LinearGradient>
    );
  };

  // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  const Red = () => {
    //  this function return a view for a red alert
    return (
      <LinearGradient colors={["#931604", "black"]} style={styles.yellow}>
        <View>
          <Image style={styles.sign} source={require("../assets/hand.png")} />
        </View>
        <View>
          <Text style={styles.text}> {obj} ahead </Text>
        </View>
      </LinearGradient>
    );
  };

  // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  return (
    <View style={styles.container}>
      <Camera
        ref={(camera) => setCamera(camera)}
        style={styles.camera}
        type={type}
        zoom={0}

        // aspect={Camera.constants.Aspect.fill}
      />
      <View style={styles.alert_div}>
        {showYellowAlert ? <Yellow /> : null}
        {showOrangeAlert ? <Orange /> : null}
        {showRedAlert ? <Red /> : null}
      </View>
    </View>
  );
};

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignContent: "center",
    backgroundColor: "#EBB150",
    backgroundColor: "whitesmoke",
    flexDirection: "column",
    alignItems: "center",
  },
  camera: {
    flex: 1,
    width: 414,

    aspectRatio: 1,
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
  yellow: {
    width: 420,
    height: 200,
    justifyContent: "center",
    alignItems: "center",
    alignSelf: "center",
  },
  alert_div: {
    width: "100%",
    height: 200,
    backgroundColor: "#EBB150",
  },
  sign: {
    width: 50,
    height: 50,
    borderRadius: 25,
    marginBottom: 100,
    alignSelf: "center",
    position: "absolute",
    justifyContent: "center",
  },
  text: {
    color: "#F8F6F4",
    fontSize: 30,
    marginTop: -60,
    textAlign: "center",
  },
});

export default OpenCamera;
